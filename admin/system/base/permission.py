import hashlib
import json
import operator
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


from system.utils.permission import PermissionUtil


class PermissionView(APIView):

    #query
    def get(self, request, pk=None):
        if pk is None:
            permissions = Permission.objects.all()
            all_permissions = list(permissions.values())
            permission_list = PermissionUtil.children_tree(None, all_permissions)
            permission_list = sorted(permission_list, key=operator.itemgetter('orders'))
            return SuccessResponse(data=permission_list)
        else:
            permission = Permission.objects.get(id=pk)
            serializer = PermissionSerializer(permission)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            permission = Permission.objects.get(pk=request.data['id'])
        except Permission.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PermissionSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(permission,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        #Remove permissions
        permission = Permission.objects.filter(id=pk)
        permission.delete()

        # Delete submenu
        subPermission = Permission.objects.filter(p_id=pk)
        subPermission.delete()

        return SuccessResponse(msg="Deleted successfully")

class PermissionBatchDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data
        try:
            Permission.objects.filter(id__in=ids).delete()
            return SuccessResponse(msg="Deleted successfully")
        except:
            return ErrorResponse(msg="Deletion failed")


class PermissionExport(APIView):
    model = Permission
    queryset = model.objects.all()
    serializer_class = PermissionSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Permission.xlsx"'

        # Create Excel workbooks and worksheets
        wb = Workbook()
        sheet = wb.active

        Permission = apps.get_model('system','Permission')
        fields = Permission._meta.get_fields()
        fields = [field for field in fields if not field.is_relation]
        headers = [field.verbose_name for field in fields if field.concrete]
        sheet.append(headers)
        list = Permission.objects.all()
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