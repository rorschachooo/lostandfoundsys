import os
import uuid
import datetime
from django.apps import apps
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook
from pytz import timezone
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from system.models import *
from system.utils.file_utils import FileUtils
from system.utils.json_response import *


# File upload
class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if file_obj is None:
            return Response({'error': 'File does not exist'}, status=400)

        # Generate random file names
        file_ext = os.path.splitext(file_obj.name)[1]
        file_name = str(uuid.uuid4()) + file_ext
        file_path = os.path.join('media', file_name)

        # Save the file to the server
        with open(file_path, 'wb') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        url = 'http://localhost:9090/media/'+file_name
        return SuccessResponse(msg="Upload Successfully",data=url)

# Rich Text-File Upload
class FileUploadEditorView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if file_obj is None:
            return Response({'errno': 1}, status=400)

        # Gnerate raendom file names
        file_ext = os.path.splitext(file_obj.name)[1]
        file_name = str(uuid.uuid4()) + file_ext
        file_path = os.path.join('media', file_name)

        # Save the file to the server
        with open(file_path, 'wb') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        url = 'http://localhost:9090/media/'+file_name
        data = {
            'url': url
        }
        return Response({'errno': 0,'data': data}, status=200)
