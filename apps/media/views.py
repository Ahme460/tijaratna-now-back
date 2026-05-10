from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import MediaFile

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        media_file = MediaFile.objects.create(
            file=file_obj,
            file_type=file_obj.content_type,
            size=file_obj.size,
            uploader=request.user
        )

        return Response({
            "id": media_file.id,
            "url": request.build_absolute_uri(media_file.file.url),
            "status": "success"
        }, status=status.HTTP_201_CREATED)
