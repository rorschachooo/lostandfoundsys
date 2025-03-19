import json
from datetime import datetime

from django.apps import apps
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook
from pytz import timezone
from rest_framework import status
from rest_framework.views import APIView
from system.models import *
from system.utils.json_response import *


#role
class RoleView(APIView):

    #query
    def get(self, request, pk=None):
        if pk is None:
            roles = Role.objects.all()
            serializerList = RoleSerializer(roles, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            role = Role.objects.get(id=pk)
            serializer = RoleSerializer(role)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = RoleSerializer(data=request.data)

        permission_ids = request.data['permissionIds']
        permissions = Permission.objects.filter(id__in=permission_ids)

        if(serializer.is_valid()):
            serializer.save(permission=permissions)
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            role = Role.objects.get(pk=request.data['id'])
        except Role.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request_data = request.data.copy()
        request_data['permission'] = request_data['permissionIds']
        serializer = RoleSerializer(data=request_data)

        if(serializer.is_valid()):
            serializer.update(role,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        role = Role.objects.filter(id=pk)
        role.delete()
        return SuccessResponse(msg="Deleted successfully")

#Pagination
class RolePageView(APIView):

    # Query data
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # Constructing a query
        roles = Role.objects.all().order_by('-id')
        if name:
            roles = roles.filter(name__icontains=name)

        # Pagination
        paginator = Paginator(roles, pageSize)
        list = paginator.page(pageNum)
        serializerList = RoleSerializer(list, many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )

class RoleBatchDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data
        try:
            Role.objects.filter(id__in=ids).delete()
            return SuccessResponse(msg="Deleted successfully")
        except:
            return ErrorResponse(msg="Deletion failed")


class RoleExport(APIView):
    model = Role
    queryset = model.objects.all()
    serializer_class = RoleSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Role.xlsx"'

        # Create Excel workbooks and worksheets
        wb = Workbook()
        sheet = wb.active

        Role = apps.get_model('system','Role')
        fields = Role._meta.get_fields()
        fields = [field for field in fields if not field.is_relation]
        headers = [field.verbose_name for field in fields if field.concrete]
        sheet.append(headers)
        list = Role.objects.all()
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