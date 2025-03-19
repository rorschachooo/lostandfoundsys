# Create your views here.
import hashlib

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from system.utils.permission import PermissionUtil
from system.models import *
from system.utils.json_response import SuccessResponse,ErrorResponse
import bcrypt

class PermissionSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = '__all__'

# User login
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Determine the user name
        users = User.objects.filter(username=username)

        if users.exists():
            user = users.first()
            # Determine the password

            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            hashpwd = md5.hexdigest()

            if hashpwd!=user.password:
                return ErrorResponse(msg="Wrong username or password")

            userSerializer = UserSerializer(user)
            token = AccessToken.for_user(user)
            # Get the permissions of a role
            role = Role.objects.get(flag=user.role)
            permissions = role.permission.all()
            all_permissions = list(permissions.values())
            menus = PermissionUtil.get_tree_permissions(all_permissions)
            auths = [permission for permission in all_permissions if permission['type'] == 3]
            data = {
                "user": userSerializer.data,
                "token":str(token),
                "menus":menus,
                "auths":auths
            }

            #Saving Session Data
            request.session['user'] = user

            return SuccessResponse(msg="Login successful",data=data)
        else:
            return ErrorResponse(msg="Unknown user")


# User logout
class LogoutView(APIView):
    def get(self, request, id):

        return SuccessResponse(msg="User logout")
