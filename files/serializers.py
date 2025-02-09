from rest_framework.serializers import Serializer, FileField, ModelSerializer
from .models import FileModel
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from rest_framework import serializers
from io import BytesIO


# Serializers define the API representation.
# class FileUploadSerializer(ModelSerializer):
#     file = FileField()
#     optimized_image = FileField(read_only=True)
#     thumbnail = FileField(read_only=True)

#     class Meta:
#         model = FileModel
#         fields = ['file', 'optimized_image', 'thumbnail', 'alt_text']
#         read_only_fields = ['stored_as', 'optimized_image', 'thumbnail']


# class FileDownloadSerializer(serializers.Serializer):
#     message = serializers.CharField(default="File retrieved successfully")
#     file_url = serializers.SerializerMethodField()
#     alt_text = serializers.CharField(required=False)
#     error = serializers.CharField(required=False)

#     def get_file_url(self, obj):
#         # Ensure obj is a model instance before accessing its attributes
#         if hasattr(obj, "file") and obj.file:
#             return obj.file.url  # Correct way to get file URL
#         return None



class FileDownloadSerializer(serializers.Serializer):
    message = serializers.CharField(default="File retrieved successfully")
    file_url = serializers.SerializerMethodField()
    optimized_image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    alt_text = serializers.CharField(required=False)
    error = serializers.CharField(required=False)

    def get_file_url(self, obj):
        """Returns the original file URL"""
        if hasattr(obj, "file") and obj.file:
            return obj.file.url  # Original file
        return None

    def get_optimized_image_url(self, obj):
        """Returns the optimized image URL if available"""
        if hasattr(obj, "optimized_image") and obj.optimized_image:
            return obj.optimized_image.url  # Optimized version
        return None

    def get_thumbnail_url(self, obj):
        """Returns the thumbnail URL if available"""
        if hasattr(obj, "thumbnail") and obj.thumbnail:
            return obj.thumbnail.url  # Thumbnail version
        return None





# class FileUploadSerializer(ModelSerializer):
#     file = FileField()

#     class Meta:
#         model = FileModel
#         fields = ['file', 'alt_text']
#         read_only_fields = ['stored_as']

#     def optimize_image(self, image):
#         img = Image.open(image)

#         # Convert RGBA to RGB
#         if img.mode in ('RGBA', 'LA'):
#             background = Image.new('RGB', img.size, (255, 255, 255))
#             background.paste(img, mask=img.split()[-1])
#             img = background

#         # Resize and compress
#         new_width = 800
#         original_width, original_height = img.size
#         new_height = int((new_width / original_width) * original_height)
#         img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

#         output = BytesIO()
#         img.save(output, format='JPEG', quality=85)
#         output.seek(0)

#         # Convert back to InMemoryUploadedFile
#         optimized_image = InMemoryUploadedFile(
#             output,
#             'ImageField',
#             f"{image.name.split('.')[0]}.jpg",
#             'image/jpeg',
#             output.getbuffer().nbytes,
#             None
#         )
#         return optimized_image

#     def create(self, validated_data):
#         file_obj = validated_data['file']

#         # Check if the file is an image before optimizing
#         if file_obj.content_type.startswith('image'):
#             optimized_file = self.optimize_image(file_obj)
#             validated_data['file'] = optimized_file  # Replace with optimized image

#         return super().create(validated_data)

class FileUploadSerializer(ModelSerializer):
    file = FileField()

    class Meta:
        model = FileModel
        fields = ['file', 'alt_text']
        read_only_fields = ['stored_as']

    # def optimize_image(self, image):
    #     img = Image.open(image)

    #     # Convert RGBA to RGB
    #     if img.mode in ('RGBA', 'LA'):
    #         background = Image.new('RGB', img.size, (255, 255, 255))
    #         background.paste(img, mask=img.split()[-1])
    #         img = background

    #     # Resize and compress
    #     new_width = 800
    #     original_width, original_height = img.size
    #     new_height = int((new_width / original_width) * original_height)
    #     img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    #     output = BytesIO()
    #     img.save(output, format='JPEG', quality=85)
    #     output.seek(0)

    #     # Convert back to InMemoryUploadedFile
    #     optimized_image = InMemoryUploadedFile(
    #         output,
    #         'ImageField',
    #         f"{image.name.split('.')[0]}.jpg",
    #         'image/jpeg',
    #         output.getbuffer().nbytes,
    #         None
    #     )
    #     return optimized_image

    # def create(self, validated_data):
        # file_obj = validated_data['file']

        # Check if the file is an image before optimizing
        # if file_obj.content_type.startswith('image'):
        #     optimized_file = self.optimize_image(file_obj)
        #     validated_data['file'] = optimized_file  # Replace with optimized image

        # return super().create(validated_data)