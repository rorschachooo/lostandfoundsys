import hashlib
import json
import string
import uuid
import random
from datetime import datetime

import bcrypt
from django.apps import apps
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook
from pytz import timezone
from rest_framework import status
from rest_framework.views import APIView
from system.models import *
from system.utils.json_response import *

#Data dictionary
class DictView(APIView):

    #Query
    def get(self, request, pk=None):
        if pk is None:
            dicts = SysDict.objects.all()
            serializerList = SysDictSerializer(dicts, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            dict = SysDict.objects.get(id=pk)
            serializer = SysDictSerializer(dict)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = SysDictSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            dict = SysDict.objects.get(pk=request.data['id'])
        except SysDict.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SysDictSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(dict,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        dict = SysDict.objects.filter(id=pk)
        dict.delete()
        return SuccessResponse(msg="Deleted successfully")

# Pagination
class DictPageView(APIView):

    # Query data
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # Constructing a query
        dicts = SysDict.objects.all().order_by('-id')
        if name:
            dicts = dicts.filter(name__icontains=name)

        # Pagination
        paginator = Paginator(dicts, pageSize)
        list = paginator.page(pageNum)
        serializerList = SysDictSerializer(list,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )

class DictBatchDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data
        try:
            # Deleting Users in Bulk
            SysDict.objects.filter(id__in=ids).delete()
            return SuccessResponse(msg="Deleted successfully")
        except:
            return ErrorResponse(msg="Deletion failed")


class DictExport(APIView):
    model = SysDict
    queryset = model.objects.all()
    serializer_class = SysDictSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Dict.xlsx"'

        # Create Excel workbooks and worksheets
        wb = Workbook()
        sheet = wb.active

        SysDict = apps.get_model('system','SysDict')
        fields = SysDict._meta.get_fields()
        fields = [field for field in fields if not field.is_relation]
        headers = [field.verbose_name for field in fields if field.concrete]
        sheet.append(headers)
        list = SysDict.objects.all()
        for data in list:
            sheet_data = []
            for field in fields:
                if field.concrete:
                    value = getattr(data, field.name)
                    if isinstance(value, datetime) and value.tzinfo:
                        value = value.astimezone(timezone('UTC'))
                        value = value.replace(tzinfo=None)
                    sheet_data.append(value)
            sheet.append(sheet_data)
        wb.save(response)
        return response