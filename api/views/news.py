import random
import re
import uuid

from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from datetime import datetime

from api import tasks


def Sendcode(phone, code):
    # -*- coding: utf-8 -*-
    from tencentcloud.common import credential
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    # 导入对应产品模块的client models。
    from tencentcloud.sms.v20190711 import sms_client, models

    try:
        phone = f'+86{phone}'
        code = str(code)
        cred = credential.Credential("secretid", "secretkey")

        client = sms_client.SmsClient(cred, "ap-guangzhou")

        # 实例化一个请求对象，根据调用的接口和实际情况，可以进一步设置请求参数
        # 你可以直接查询SDK源码确定SendSmsRequest有哪些属性可以设置
        # 属性可能是基本类型，也可能引用了另一个数据结构
        # 推荐使用IDE进行开发，可以方便的跳转查阅各个接口和数据结构的文档说明
        req = models.SendSmsRequest()

        req.SmsSdkAppid = "1400401982"
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名，签名信息可登录 [短信控制台] 查看
        req.Sign = "franchs豪七"
        # 短信码号扩展号: 默认未开通，如需开通请联系 [sms helper]
        req.PhoneNumberSet = [phone]
        # 模板 ID: 必须填写已审核通过的模板 ID。模板ID可登录 [短信控制台] 查看
        req.TemplateID = "672604"
        # 模板参数: 若无模板参数，则设置为空
        req.TemplateParamSet = [code]

        # 通过client对象调用DescribeInstances方法发起请求。注意请求方法名与请求对象是对应的。
        # 返回的resp是一个DescribeInstancesResponse类的实例，与请求对象对应。
        resp = client.SendSms(req)

        # 输出json格式的字符串回包
        print(resp.to_json_string(indent=2))

    except TencentCloudSDKException as err:
        print(err)


def phone_validator(value):
    if not re.match(r"^(1[3|4|5|6|7|8|9])\d{9}$", value):
        return ValidationError('手机格式错误')


class MessageSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号', validators=[phone_validator, ])


class MessageView(APIView):
    def get(self, request, *args, **kwargs):
        ser = MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'status': False, 'msg':'手机格式错误'})
        phone = ser.validated_data.get('phone')
        code = random.randint(1000, 9999)
        cache.set(phone, code, 60)
        result = Sendcode(phone, code)

        return Response({'status': True, 'msg': '发送成功'})


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号', validators=[phone_validator,])
    code = serializers.CharField(label='短信验证码')

    def validate_code(self, value):
        if len(value)!=4:
            raise ValidationError('手机验证码格式不对')
        if not value.isdecimal():
            raise ValidationError('短信格式错误')
        phone = self.initial_data.get('phone')
        if not cache.get(phone):
            raise ValidationError('短信验证码过期')
        return value


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        ser  = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'status': False, 'msg': '登录失败'})
        phone = ser.validated_data.get('phone')
        user, _= models.UserInfo.objects.get_or_create(phone=phone)
        user.token = str(uuid.uuid4())
        user.save()
        return Response({'status': True, 'msg': '登录成功', 'data':{'token': user.token, 'phone':phone}})
