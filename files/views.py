
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import FileUploadSerializer
from .spectacular_schemas import file_upload_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .models import FileModel
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework.views import APIView
import os
from django.utils.timezone import now


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

    def get(self, request, stored_as):
        file_instance = get_object_or_404(FileModel, stored_as=stored_as)
        file_path = file_instance.file.path

        if os.path.exists(file_path):
            # Determine if the file is an image or media file
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mp3']:
                # Generate a URL for viewing the file
                file_url = request.build_absolute_uri(file_instance.file.url)

                # Update last_retrieved_at and retrieval_count
                file_instance.last_retrieved_at = now()
                file_instance.retrieval_count += 1
                file_instance.save(update_fields=['last_retrieved_at', 'retrieval_count'])



                return Response({
                    "message": "File is available for viewing",
                    "file_url": file_url
                })
            else:
                # Provide a download link for non-media files
                response = FileResponse(open(file_path, 'rb'))
                response['Content-Disposition'] = f'attachment; filename="{file_instance.name}"'
                return response
        else:
            return Response({
                "message": "File not found",
                "error": "The requested file does not exist on the server."
            }, status=404)


def home(request):
    return render(request, 'home.html')
