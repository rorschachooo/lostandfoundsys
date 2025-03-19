from datetime import datetime
from django.apps import apps
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook
from pytz import timezone
from rest_framework import status
from rest_framework.views import APIView
from business.models import *
from system.models import *
from system.utils.json_response import *
import uuid
import hashlib
from system.utils.user import UserToken

# Slideshow
class BannerView(APIView):

    # Query data
    def get(self, request , pk=None):
        if pk is None:
            list = Banner.objects.all()
            serializerList = BannerSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Banner.objects.get(id=pk)
            serializer = BannerSerializer(model)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = BannerSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            model = Banner.objects.get(pk=request.data['id'])
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        serializer = BannerSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        model = Banner.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="Deleted successfully")

# Pagination
class BannerPageView(APIView):

    # query
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        user_id = UserToken.user_id(request)
        user = User.objects.get(pk=user_id)

        # Constructing a query
        list = Banner.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)


        # Pagination
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = BannerSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )

class BannerBatchDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data
        try:
            Banner.objects.filter(id__in=ids).delete()
            return SuccessResponse(msg="Deleted successfully")
        except:
            return ErrorResponse(msg="Deletion failed")


class BannerExport(APIView):
    model = Banner
    queryset = model.objects.all()
    serializer_class = BannerSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Banner.xlsx"'

        # Create Excel workbooks and worksheets
        wb = Workbook()
        sheet = wb.active

        model = apps.get_model('business','Banner')
        fields = model._meta.get_fields()
        fields = [field for field in fields if not field.is_relation]
        headers = [field.verbose_name for field in fields if field.concrete]
        sheet.append(headers)
        list = Banner.objects.all()
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
