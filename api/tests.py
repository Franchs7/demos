import re

from django.test import TestCase

# Create your tests here.
def phone_validator(value):
    if not re.match(r"^(1[3|4|5|6|7|8|9])\d{9}$", value):
        return print('错误')



if __name__ == '__main__':
    phone = 123
    phone = f'+86{phone}'
    print(type(phone))