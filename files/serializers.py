from rest_framework.serializers import Serializer, FileField, ModelSerializer
from .models import FileModel

# Serializers define the API representation.
class FileUploadSerializer(ModelSerializer):
    # file = FileField()

    class Meta:
        model = FileModel
        # fields = ['file', 'name', 'file_type', 'file_size']
        # fields = ['file', 'alt_text']
        fields = '__all__'


    def create(self, validated_data):
        # Handle file-specific fields (calculated)
        uploaded_file = validated_data.get('file')  # Extract the file
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
