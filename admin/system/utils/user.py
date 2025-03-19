from rest_framework_simplejwt.tokens import AccessToken
from system.utils.json_response import ErrorResponse

# Get user token data
class UserToken():
    def user_id(request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        try:
            access_token = AccessToken(token)
            payload = access_token.payload
        except:
            return ErrorResponse(msg="Invalid Token")
        id = payload.get('user_id')
        return id