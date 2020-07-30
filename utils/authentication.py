from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api import models


class GeneralAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            print(1)
            return None
            # raise AuthenticationFailed('认证失败')
        user = models.UserInfo.objects.filter(token=token).first()
        if not user:
            # raise AuthenticationFailed('认证失败')
            return None
        return (user, token) # request.user/request.auth