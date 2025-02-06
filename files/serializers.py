from rest_framework.serializers import Serializer, FileField, ModelSerializer
from .models import FileModel
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from rest_framework import serializers

# Serializers define the API representation.
class FileUploadSerializer(ModelSerializer):
    file = FileField()

    class Meta:
        model = FileModel
        fields = ['file', 'alt_text']
        read_only = ['stored_as']
        # fields = ['file', 'alt_text']
        # fields = '__all__'


    def optimize_image(self, image):
  
        img = Image.open(image)
        
       # Convert to RGB if the image is in RGBA mode
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])  # Paste the image onto the background
            img = background

        # resize and compress
        new_width = 800
        original_width, original_height = img.size
        new_height = int((new_width / original_width) * original_height)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS) # Resize to a maximum of 800x800 pixels
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)  # Save with 85% quality
        output.seek(0)

        # Convert back to InMemoryUploadedFile
        optimized_image = InMemoryUploadedFile(
            output,
            'ImageField',  # Field name
            f"{image.name.split('.')[0]}.jpg",  # New file name
            'image/jpeg',
            output.getbuffer().nbytes,
            None
        )
        return optimized_image


    def create(self, validated_data):

        file = validated_data.pop('file')
        
        # Optimize the image if it's an image file
        if file.content_type.startswith('image'):
            optimized_image = self.optimize_image(file)
            validated_data['file'] = optimized_image



        uploaded_file = validated_data.get('file')  # Extract the file


        # these assignments (atleast the 'file type') should be done after image optimization since the file type changes from ant->jpg during optimization
        file_name = uploaded_file.name
        file_size = uploaded_file.size
        file_type = uploaded_file.content_type

        # Add these values to the validated data
        validated_data['name'] = file_name
        validated_data['file_size'] = file_size
        validated_data['file_type'] = file_type.lower()



        # Create the FileModel instance using the validated data
        file_instance = FileModel.objects.create(**validated_data)

        return file_instance


class FileDownloadSerializer(serializers.Serializer):
    message = serializers.CharField()
    file_url = serializers.URLField(required=False)
    alt_text = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
