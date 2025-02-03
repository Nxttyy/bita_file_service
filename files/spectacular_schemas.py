from django.core.files import File
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter, OpenApiResponse
from .serializers import FileUploadSerializer

file_upload_schema = extend_schema(
        request=FileUploadSerializer,
        responses={
            201: OpenApiResponse(response=FileUploadSerializer, description="File uploaded successfully"),
            400: OpenApiResponse(description="Invalid file or request"),
        },
        summary="Upload a file",
        description="Uploads a file and returns the content type of the uploaded file.",
        # parameters=[
        #     OpenApiParameter(
        #         name="file",
        #         type=OpenApiTypes.BYTE,
        #         location=OpenApiParameter.HEADER,
        #         required=True,
        #         description="File to be uploaded"
        #     )
        # ]

    )
