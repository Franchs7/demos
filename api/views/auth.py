import random
import uuid

from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models
from api.serializers.acount import MessageSerializer, LoginSerializer
from utils.tencent.messagesend import Sendcode


class MessageView(APIView):
    # authentication_classes = []
    def get(self, request, *args, **kwargs):
        ser = MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'status': False, 'msg': '手机格式错误'})
        phone = ser.validated_data.get('phone')
        code = random.randint(1000, 9999)
        cache.set(phone, code, 60)
        Sendcode(phone, code)

        return Response({'status': True, 'msg': '发送成功'})


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'status': False, 'msg': '登录失败'})
        phone = ser.validated_data.get('phone')
        user, _ = models.UserInfo.objects.get_or_create(phone=phone)
        user.token = str(uuid.uuid4())
        user.save()
        return Response({'status': True, 'msg': '登录成功', 'data': {'token': user.token, 'phone': phone}})

