from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.serializers.validators import phone_validator

# 自定义校验,没有和数据库对接
class MessageSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号', validators=[phone_validator, ])


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号', validators=[phone_validator, ])
    code = serializers.CharField(label='短信验证码')

    def validate_code(self, value):
        if len(value) != 4:
            raise ValidationError('手机验证码格式不对')
        if not value.isdecimal():
            raise ValidationError('短信格式错误')
        phone = self.initial_data.get('phone')
        if not cache.get(phone):
            raise ValidationError('短信验证码过期')
        return value
