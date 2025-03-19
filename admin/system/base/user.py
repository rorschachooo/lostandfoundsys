import hashlib
import json
import string
import traceback
import uuid
import random
from datetime import datetime
from pytz import timezone

from django.apps import apps
import bcrypt
from django.core.paginator import Paginator
from django.http import HttpResponse
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.views import APIView
from openpyxl import Workbook
from system.models import *
from system.utils.json_response import *

#user
class UserView(RetrieveModelMixin,APIView):

    #query
    def get(self, request, pk=None):
        if pk is None:
            # Constructing a query
            users = User.objects.all()
            serializerList = UserSerializer(users, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if(serializer.is_valid()):
            if(User.objects.filter(username=request.data['username']).exists()):
                return ErrorResponse(msg="User already exists")

            # Set Nickname
            if request.data['name'] is None:
                name = 'System Users'+''.join(random.sample(string.ascii_letters + string.digits, 6))
            else:
                name = request.data['name']
            # Generate UUID
            uid = uuid.uuid1()
            password = '123'
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            hashed_password = md5.hexdigest()
            serializer.save(name=name, uid=uid, password=hashed_password)
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            user = User.objects.get(pk=request.data['id'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(user,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        user = User.objects.filter(id=pk)
        user.delete()
        return SuccessResponse(msg="Deleted successfully")

# Pagination
class UserPageView(APIView):
    # Query data
    def get(self, request):
        name = request.query_params.get('name')
        address = request.query_params.get('address')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # Constructing a query
        users = User.objects.all().order_by('-id')
        if name:
            users = users.filter(username__icontains=name)
        if address:
            users = users.filter(address__icontains=address)

        # Pagination
        paginator = Paginator(users, pageSize)
        list = paginator.page(pageNum)
        serializerList = UserSerializer(list, many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )

class UserBatchDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data
        try:
            # Deleting Users in Bulk
            User.objects.filter(id__in=ids).delete()
            return SuccessResponse(msg="Deleted successfully")
        except:
            return ErrorResponse(msg="Deletion failed")

class UserExport(APIView):
    use_model = User
    queryset = use_model.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="User.xlsx"'

        # Create Excel workbooks and worksheets
        wb = Workbook()
        sheet = wb.active

        User = apps.get_model('system','User')
        fields = User._meta.get_fields()
        fields = [field for field in fields if not field.is_relation]
        headers = [field.verbose_name for field in fields if field.concrete]
        sheet.append(headers)
        users = User.objects.all()
        for user in users:
            user_data = []
            for field in fields:
                if field.concrete:
                    value = getattr(user, field.name)
                    if isinstance(value, datetime) and value.tzinfo:
                        # Convert timezone-aware datetime to the desired timezone or set timezone to None
                        value = value.astimezone(timezone('UTC'))  # Replace 'UTC' with your desired timezone
                        value = value.replace(tzinfo=None)
                    user_data.append(value)
            sheet.append(user_data)
        wb.save(response)
        return response

# Modify personal information
class UserInfoUpdate(APIView):
    # alter
    def put(self, request):
        try:
            user = User.objects.get(pk=request.data['id'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(user,serializer.validated_data)
            return SuccessResponse(msg="Modification successful",data=serializer.data)
        else:
            return ErrorResponse(msg="Data validation failed")

# Change Password
class UserUpdatePwd(APIView):
    # alter
    def post(self, request):
        try:
            user = User.objects.get(uid=request.data['uid'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        old_pwd = request.data['password']
        md5 = hashlib.md5()
        md5.update(old_pwd.encode('utf-8'))
        hashpwd = md5.hexdigest()

        if hashpwd != user.password:
            return ErrorResponse(msg="The original password is incorrect")

        new_pwd = request.data['newPassword']
        md5 = hashlib.md5()
        md5.update(new_pwd.encode('utf-8'))
        hashnewpwd = md5.hexdigest()

        user.password = hashnewpwd
        user.save()
        return SuccessResponse(msg="Modification successful")

