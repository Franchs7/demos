import random
import uuid

from django.core.cache import cache
from django.db.models import F
from django.forms import model_to_dict

from rest_framework import serializers, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models

from api.serializers.acount import LoginSerializer, MessageSerializer
from utils.authentication import GeneralAuthentication
from utils.filter import MinFilterBackend, MaxFilterBackend
from utils.pagination import LimitPagenation
from api import tasks



class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = '__all__'

# 话题接口
class TopicView(ListAPIView):
    # authentication_classes = []
    serializer_class = TopicSerializer
    pagination_class = LimitPagenation
    filter_backends = [MinFilterBackend, MaxFilterBackend]
    queryset = models.Topic.objects.all().order_by('-id')


class NewsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()

    class Meta:
        model = models.News
        fields = ['id', 'cover', 'content', 'topic', "user", 'favor_count']

    def get_user(self, obj):
        return model_to_dict(obj.user, fields=['id', 'nickname', 'avatar'])

    def get_topic(self, obj):
        if not obj.topic:
            return
        return model_to_dict(obj.topic, fields=['id', 'title'])

# 动态列表接口
class NewsView(ListAPIView):
    serializer_class = NewsSerializer
    filter_backends = [MinFilterBackend, MaxFilterBackend]

    # The style to use for queryset pagination.
    pagination_class = LimitPagenation
    queryset = models.News.objects.all().order_by('-id')


class NewsDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format="%Y-%M-%D")
    user = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    viewer = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = models.News
        exclude = ['cover', ]

    def get_images(self, obj):
        details_queryset = models.NewsDetails.objects.filter(news=obj)
        return [model_to_dict(row, ['id', 'cos_path']) for row in details_queryset]

    def get_user(self, obj):
        user = obj.user
        return model_to_dict(user, fields=['id', 'nickname', 'avatar'])

    def get_topic(self, obj):
        return model_to_dict(obj.topic, fields=['id', 'title'])

    def get_viewer(self, obj):
        viewers = models.ViewRecord.objects.filter(news=obj).order_by('-id')[:10]
        context = {
            'count': viewers.count(),
            'result': [model_to_dict(row.user, fields=['nickname', 'avatar']) for row in viewers]
        }
        return context

    def get_comment(self, obj):
        # 获取一级评论
        first_queryset = models.CommentRecord.objects.filter(news=obj, depth=1).order_by('id')[:10].values(
            'id',
            'content',
            'depth',
            'user__nickname',
            'user__avatar',
            'create_date',
        )
        first_id_list = [item['id'] for item in first_queryset]
        from django.db.models import Max
        result = models.CommentRecord.objects.filter(news=obj, depth=2, reply_id__in=first_id_list).values(
            'reply_id').annotate(max_id=Max('id'))
        second_id_list = [item['max_id'] for item in result]
        second_queryset = models.CommentRecord.objects.filter(id__in=second_id_list).values(
            'id',
            'content',
            'depth',
            'user__nickname',
            'user__avatar',
            'create_date',
            'reply_id',
            'reply__user__nickname'
        )
        import collections
        first_dict = collections.OrderedDict() #有序字典key排序
        for item in first_queryset:
            item['create_date'] = item['create_date'].strftime('%Y-%m-%d')
            first_dict[item['id']] = item
        for node in second_queryset:
            first_dict[node['reply_id']]['child'] = [node, ]
        return first_dict.values()

# 动态详情接口
class NewsDetailView(RetrieveAPIView):
    serializer_class = NewsDetailSerializer
    queryset = models.News.objects


class CommentModelSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%M-%D')
    user__nickname = serializers.CharField(source='user.nickname')
    user__avatar = serializers.CharField(source='user.avatar')
    reply_id = serializers.CharField(source='reply.id')
    reply__user__nickname = serializers.CharField(source='reply.user.nickname')
    class Meta:
        model = models.CommentRecord
        exclude = ['news', 'user', 'reply', 'depth', 'root', 'favor_count']

class CreateCommentModelSerializer(serializers.ModelSerializer):
    """
     news.id, content, reply.id, root
    """
    class Meta:
        model = models.CommentRecord
        exclude = ['user','favor_count']

# 评论获取接口,和创建评论接口
class CommentView(APIView):
    """
     {
    "id": 5,
    "content": "1-2",
    "user__nickname": "大卫-6",
    "user__avatar": "https://mini-1251317460.cos.ap-chengdu.myqcloud.com/08a9daei1578736867828.png",
    "create_date": "2020-01-15T07:46:35.434290Z",
    "reply_id": 1,
    "reply__user__nickname": "wupeiqi"
}

    """
    def get(self, request, *args, **kwargs):
        queryset = models.CommentRecord.objects.filter(root_id=request.query_params.get('root')).order_by('id')
        ser = CommentModelSerializer(instance=queryset, many=True)
        return Response(ser.data,status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        ser = CreateCommentModelSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        ser.save(user_id=1)
        new_id = ser.data.get('news')
        models.News.objects.filter(id=new_id).update(comment_count=F('comment_count')+1)
        return Response(ser.data, status.HTTP_201_CREATED)


class FavorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewsFavorRecord
        fields = ['news']

# 新闻点赞
class FavorView(APIView):
    def post(self, request, *args, **kwargs):
        ser = FavorModelSerializer(data=request.data)
        if not ser.is_valid():
            return Response({}, status.HTTP_400_BAD_REQUEST)
        news_objects = ser.validated_data.get('news')
        print(request.user)
        queryset = models.NewsFavorRecord.objects.filter(user=request.user, news=news_objects)
        flag = queryset.exists()
        if flag:
            queryset.delete()
            return Response({}, status.HTTP_200_OK)
        models.NewsFavorRecord.objects.create(user=request.user, news=news_objects)
        return Response({}, status.HTTP_201_CREATED)