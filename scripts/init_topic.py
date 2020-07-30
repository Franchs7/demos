import os
import sys

import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demos.settings')
django.setup()


from api import models
for i in range(10):
    models.Topic.objects.create(title=f'手机类型{i}')