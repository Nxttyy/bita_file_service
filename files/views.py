
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import FileUploadSerializer, FileDownloadSerializer
from .spectacular_schemas import file_upload_schema, file_download_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .models import FileModel
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework.views import APIView
import os


class UploadViewSet(ViewSet):
    serializer_class = FileUploadSerializer
    parser_classes = [MultiPartParser, FormParser]

    @file_upload_schema
    def create(self, request):
        my_file = FileUploadSerializer(data=request.data)
        if my_file.is_valid():
            saved_file = my_file.save()
            response = {
                "message": "File uploaded successfully",
                "stored_as": saved_file.stored_as
            }
        else:
            response = {
                "message": "Invalid request",
                "errors": my_file.errors
            }

        return Response(response)


class FileDownloadView(APIView):
    parser_classes = [MultiPartParser, FormParser]


    @file_download_schema
    def get(self, request, stored_as):
        file_instance = get_object_or_404(FileModel, stored_as=stored_as)
        file_path = file_instance.file.path
        alt_text = file_instance.alt_text

        if os.path.exists(file_path):
            # Determine if the file is an image or media file
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mp3']:
                # Generate a URL for viewing the file
                file_url = request.build_absolute_uri(file_instance.file.url)

                # Update retrieval info
                file_instance.update_retrieval_info()

                # Serialize the response
                response_data = {
                    "message": "File is available for viewing",
                    "file_url": file_url,
                    "alt_text": alt_text
                }
                serializer = FileDownloadSerializer(data=response_data)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data)
            else:
                # Provide a download link for non-media files
                response = FileResponse(open(file_path, 'rb'))
                response['Content-Disposition'] = f'attachment; filename="{file_instance.name}"'
                return response
        else:
            # Serialize the error response
            error_data = {
                "message": "File not found",
                "error": "The requested file does not exist on the server."
            }
            serializer = FileDownloadSerializer(data=error_data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=404)
def home(request):
    return render(request, 'home.html')
