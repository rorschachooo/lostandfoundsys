from rest_framework.views import APIView
from business.models import *
from system.models import *
from django.db import connection
from system.utils.json_response import *
from rest_framework import status
from django.core.paginator import Paginator
from system.utils.user import UserToken



# user
class UserListDetail(APIView):
    # List and query a item
    def get(self, request , pk=None):
        if pk is None:
            list = User.objects.all()
            serializerList = UserSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = User.objects.get(id=pk)
            serializer = UserSerializer(model)
            return SuccessResponse(data=serializer.data)

class UserPage(APIView):

    # Pagination
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # Constructing a query
        list = User.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # Pagination
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = UserSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )
								
# Pagination
class NoticeListDetail(APIView):
    # List and query a list
    def get(self, request , pk=None):
        if pk is None:
            list = Notice.objects.all()
            serializerList = NoticeSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Notice.objects.get(id=pk)
            serializer = NoticeSerializer(model)
            return SuccessResponse(data=serializer.data)

class NoticePage(APIView):

    # Pagination
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # Constructing a query
        list = Notice.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # Pagination
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = NoticeSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )

								
# Query users by userId
class getMemberByUserId(APIView):
    def get(self, request, userId):
        model = Member.objects.filter(user_id=userId).first()
        serializer = MemberSerializer(model)
        return SuccessResponse(data=serializer.data)

class UpdateMember(APIView):
    # Add/Modify
    def put(self, request):
        if 'id' not in request.data:
            # add
            serializer = MemberSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="Added successfully")
            else:
                return ErrorResponse(msg="Data validation failed")

        try:
            model = Member.objects.get(pk=request.data['id'])
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

# Slideshow
class BannerListDetail(APIView):
    # List and query a item
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
		
class BannerPage(APIView):

    # Pagination
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

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


class UpdateBanner(APIView):
    # Revise
    def put(self, request):
        if 'id' not in request.data:
            # add
            serializer = BannerSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="Added successfully")
            else:
                return ErrorResponse(msg="Data validation failed")
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

# user
class MemberListDetail(APIView):
    # List and query a item
    def get(self, request , pk=None):
        if pk is None:
            list = Member.objects.all()
            serializerList = MemberSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Member.objects.get(id=pk)
            serializer = MemberSerializer(model)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            model = Member.objects.get(pk=request.data['id'])
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        model = Member.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="Deleted successfully")
		
class MemberPage(APIView):

    # Pagination
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # Constructing a query
        list = Member.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # Pagination
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = MemberSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateMember(APIView):
    # alter
    def put(self, request):
        if 'id' not in request.data:
            # add
            serializer = MemberSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="Added successfully")
            else:
                return ErrorResponse(msg="Data validation failed")
        try:
            model = Member.objects.get(pk=request.data['id'])
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

# Lost and Found Information
class RecruitListDetail(APIView):
    # List and query a item
    def get(self, request , pk=None):
        if pk is None:
            list = Recruit.objects.all()
            serializerList = RecruitSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Recruit.objects.get(id=pk)
            serializer = RecruitSerializer(model)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = RecruitSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            model = Recruit.objects.get(pk=request.data['id'])
        except Recruit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RecruitSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        model = Recruit.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="Deleted successfully")
		
class RecruitPage(APIView):

    # Pagination
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))
        category_id = request.query_params.get('category_id')

        # Constructing a query
        list = Recruit.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)
        if category_id:
            list = list.filter(category_id=category_id)

        # Pagination
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = RecruitSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateRecruit(APIView):
    # alter
    def put(self, request):
        if 'id' not in request.data:
            # add
            serializer = RecruitSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="Added successfully")
            else:
                return ErrorResponse(msg="Data validation failed")
        try:
            model = Recruit.objects.get(pk=request.data['id'])
        except Recruit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RecruitSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

# Lost property information
class LostListDetail(APIView):
    # List and query a item
    def get(self, request , pk=None):
        if pk is None:
            list = Lost.objects.all()
            serializerList = LostSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Lost.objects.get(id=pk)
            serializer = LostSerializer(model)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = LostSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            model = Lost.objects.get(pk=request.data['id'])
        except Lost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LostSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        model = Lost.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="Deleted successfully")
		
class LostPage(APIView):

    # Pagination
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))
        category_id = request.query_params.get('category_id')

        # Constructing a query
        list = Lost.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)
        if category_id:
            list = list.filter(category_id=category_id)

        # Pagination
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = LostSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateLost(APIView):
    # alter
    def put(self, request):
        if 'id' not in request.data:
            # add
            serializer = LostSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="Added successfully")
            else:
                return ErrorResponse(msg="Data validation failed")
        try:
            model = Lost.objects.get(pk=request.data['id'])
        except Lost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LostSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

# Item Type
class CategoryListDetail(APIView):
    #  List and query a item
    def get(self, request , pk=None):
        if pk is None:
            list = Category.objects.all()
            serializerList = CategorySerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Category.objects.get(id=pk)
            serializer = CategorySerializer(model)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            model = Category.objects.get(pk=request.data['id'])
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        model = Category.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="Deleted successfully")
		
class CategoryPage(APIView):

    # Pagination
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # Constructing a query
        list = Category.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # Pagination
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = CategorySerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateCategory(APIView):
    # alter
    def put(self, request):
        if 'id' not in request.data:
            # add
            serializer = CategorySerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="Added successfully")
            else:
                return ErrorResponse(msg="Data validation failed")
        try:
            model = Category.objects.get(pk=request.data['id'])
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

# Information to be claimed
class CartListDetail(APIView):
    #  List and query a item
    def get(self, request , pk=None):
        if pk is None:
            list = Cart.objects.all()
            serializerList = CartSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Cart.objects.get(id=pk)
            serializer = CartSerializer(model)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            model = Cart.objects.get(pk=request.data['id'])
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        model = Cart.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="Deleted successfully")
		
class CartPage(APIView):

    # Pagination
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # Constructing a query
        list = Cart.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # Pagination
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = CartSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateCart(APIView):
    # alter
    def put(self, request):
        if 'id' not in request.data:
            # add
            serializer = CartSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="Added successfully")
            else:
                return ErrorResponse(msg="Data validation failed")
        try:
            model = Cart.objects.get(pk=request.data['id'])
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

# Lost and found records
class OrdersListDetail(APIView):
    #  List and query a item
    def get(self, request , pk=None):
        if pk is None:
            list = Orders.objects.all()
            serializerList = OrdersSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Orders.objects.get(id=pk)
            serializer = OrdersSerializer(model)
            return SuccessResponse(data=serializer.data)

    # add
    def post(self, request):
        serializer = OrdersSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="Added successfully")
        else:
            return ErrorResponse(msg="Data validation failed")

    # alter
    def put(self, request):
        try:
            model = Orders.objects.get(pk=request.data['id'])
        except Orders.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrdersSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")

    # delete
    def delete(self, request, pk):
        model = Orders.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="Deleted successfully")
		
class OrdersPage(APIView):

    # Pagination
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # Constructing a query
        list = Orders.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # Pagination
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = OrdersSerializer(pageList,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )


class UpdateOrders(APIView):
    # alter
    def put(self, request):
        if 'id' not in request.data:
            # add
            serializer = OrdersSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="Added successfully")
            else:
                return ErrorResponse(msg="Data validation failed")
        try:
            model = Orders.objects.get(pk=request.data['id'])
        except Orders.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrdersSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(model,serializer.validated_data)
            return SuccessResponse(msg="Modification successful")
        else:
            return ErrorResponse(msg="Data validation failed")


# Add/Edit Cart
class UpdateCart(APIView):
    def post(self, request):
        id = None
        if 'id' in request.data:
            id = request.data['id']
        name = None
        if 'name' in request.data:
            name = request.data['name']
        img = None
        if 'img' in request.data:
            img = request.data['img']
        userId = None
        if 'userId' in request.data:
            userId = request.data['userId']
        if 'goodid' in request.data:
            goodid = request.data['goodid']
        bizUserId = None
        if 'bizUserId' in request.data:
            bizUserId = request.data['bizUserId']
		
        cart = Cart.objects.filter(name=name,user_id=userId).first()
        if cart:
            if id:
                cart.save()
            else:
                cart.save()
            return SuccessResponse(msg="Operation successful")
        else:
            Cart.objects.create(
                name=name,
                img=img,
                user_id=userId,
                goodid=goodid,
                biz_user_id=bizUserId
            )
            return SuccessResponse(msg="Added successfully")



# Add/Modify Order
class UpdateOrders(APIView):
    def post(self, request):
        id = None
        if 'id' in request.data:
            id = request.data['id']
        name = None
        if 'name' in request.data:
            name = request.data['name']
        content = None
        if 'content' in request.data:
            content = request.data['content']
        stateRadio = None
        if 'stateRadio' in request.data:
            stateRadio = request.data['stateRadio']
        userId = None
        if 'userId' in request.data:
            userId = request.data['userId']
        goodids = None
        if 'goodids' in request.data:
            goodids = request.data['goodids']
        bizUserId = None
        if 'bizUserId' in request.data:
            bizUserId = request.data['bizUserId']

        if id:
            dbOrders = Orders.objects.filter(id=id).first()
            if dbOrders:
                if name is not None:
                    dbOrders.name=name
                if content is not None:
                    dbOrders.content=content
                if stateRadio is not None:
                    dbOrders.state_radio=stateRadio
                if userId is not None:
                    dbOrders.user_id=userId
                if goodids is not None:
                    dbOrders.goodids=goodids
                if bizUserId is not None:
                    dbOrders.biz_user_id=bizUserId
                dbOrders.save()
        else:
            Orders.objects.create(
            name=name,
            content=content,
            state_radio=stateRadio,
            user_id=userId,
            goodids=goodids,
            biz_user_id=bizUserId,
            )
        return SuccessResponse(msg="Operation successful")

# Cancellation of order
class CancelOrders(APIView):
    def put(self, request, pk):
        curAddr = Orders.objects.filter(id=pk).first()
        curAddr.state_radio = 'Cancelled'
        curAddr.save()
        return SuccessResponse(msg="Cancel Success")








def to_camel_case(s):
    parts = s.split('_')
    return parts[0] + ''.join(part.title() for part in parts[1:])

def convert_props_to_camel_case(data):
    for key, value in list(data.items()):
        if isinstance(value, dict):
            convert_props_to_camel_case(value)
        elif isinstance(value, list):
            for item in value:
                convert_props_to_camel_case(item)
        camel_case_key = to_camel_case(key)
        data[camel_case_key] = data.pop(key)
