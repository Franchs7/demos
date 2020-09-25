from django.db.models import Max
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import serializers
from utils import filter, pagination
from api import models
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework import exceptions
from django.db import transaction

class AUctionModelSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    preview_start_time = serializers.DateTimeField(format='%Y-%m-%d')
    goods = serializers.SerializerMethodField()

    class Meta:
        model = models.Auction
        fields = ['id', 'status', 'title', 'cover', 'preview_start_time', 'look_count', 'goods_count', 'total_price',
                  'bid_count', 'goods']

    def get_goods(self, obj):
        queryset = models.AuctionItem.objects.filter(auction=obj)[0:5]
        return [row.cover for row in queryset]


class AuctionView(ListAPIView):
    queryset = models.Auction.objects.filter(status__gte=1).order_by('-id')
    serializer_class = AUctionModelSerializer
    filter_backends = [filter.MaxFilterBackend, filter.MinFilterBackend]
    pagination_class = pagination.LimitPagenation


class AuctionDetailItemModelSerializer(serializers.ModelSerializer):
    is_deposit = serializers.SerializerMethodField()

    class Meta:
        model = models.AuctionItem
        fields = '__all__'

    def get_is_deposit(self, obj):
        user_object = self.context['request'].user
        if not user_object:
            return False
        return models.DepositRecord.objects.filter(user=user_object, item=obj, status=2).exists()


class AuctionDetaiModelSerializer(serializers.ModelSerializer):
    goods = serializers.SerializerMethodField()
    is_deposit = serializers.SerializerMethodField()

    class Meta:
        model = models.Auction
        fields = '__all__'

    def get_goods(self, obj):
        items = models.AuctionItem.objects.filter(auction=obj)
        ser = AuctionDetailItemModelSerializer(instance=items, many=True, context=self.context)
        return ser.data

    def get_is_deposit(self, obj):
        user_object = self.context['request'].user
        if not user_object:
            return False
        return models.DepositRecord.objects.filter(user=user_object, auction=obj, status=2, item__isnull=True).exists()


class AuctionDetailView(RetrieveAPIView):
    queryset = models.Auction.objects.filter(id__gte=1)
    serializer_class = AuctionDetaiModelSerializer


class AutionItemDetailModelSerializer(serializers.ModelSerializer):
    carousel_list = serializers.SerializerMethodField()
    detail_list = serializers.SerializerMethodField()
    image_list = serializers.SerializerMethodField()
    record = serializers.SerializerMethodField()

    class Meta:
        model = models.AuctionItem
        fields = '__all__'

    def get_image_list(self, obj):
        queryset = models.AuctionItemImage.objects.filter(item=obj)
        return [row.img for row in queryset]

    def get_carousel_list(self, obj):
        queryset = models.AuctionItemImage.objects.filter(item=obj, carousel=True).order_by('-order')
        return [row.img for row in queryset]

    def get_detail_list(self, obj):
        queryset = models.AuctionItemDetail.objects.filter(item=obj)
        return [model_to_dict(row, ['key', 'value']) for row in queryset]

    def get_record(self, obj):
        queryset = models.BrowseRecord.objects.filter(item=obj)
        result = {
            'record_list': [row.user.avatar for row in queryset[0:10]],
            'record_count': queryset.count()
        }
        return result


class AuctionItemDetailView(RetrieveAPIView):
    queryset = models.AuctionItem.objects.filter(status__gt=1)
    serializer_class = AutionItemDetailModelSerializer


class DepositSerializer(serializers.ModelSerializer):
    deposit = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = models.AuctionItem
        fields = ['id', 'cover', 'reserve_price', 'highest_price', 'deposit', 'balance']

    def get_balance(self, obj):
        return self.context['request'].user.balance

    def get_deposit(self, obj):
        result = {
            'selected': 1,
            'data_list': [
                {'id': 1, 'deposit': obj.deposit, 'text': '单品保证金'},
                {'id': 2, 'deposit': obj.auction.deposit, 'text': '全场保证金'}
            ]
        }
        return result


# 保证金(提交保证金)
class DepositView(RetrieveAPIView, CreateAPIView):
    queryset = models.AuctionItem.objects.filter(status__in=[2, 3])
    serializer_class = DepositSerializer


class BidModelSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)
    user = serializers.CharField(source='user.nickname',read_only=True)
    def validate_item(self, value):
        flag = models.AuctionItem.objects.filter(id=value,status=3).exists()
        if not flag:
            raise exceptions.ValidationError('该商品没在拍卖中')
        return value
    def validate_price(self, value):
        item_id = self.initial_data.get('item')
        item_obj = models.AuctionItem.objects.filter(id=item_id).first()
        max_price = models.BidRecord.objects.filter(item_id=item_id).aggregate(max_price=Max('price'))['max_price']
        if  not max_price:
            max_price = item_obj.start_price
        if value <= max_price:
            raise exceptions.ValidationError('价格错误')
        if (value-max_price) % item_obj.unit !=0:
            raise exceptions.ValidationError('价格错误')
        return value
    class Meta:
        model = models.BidRecord
        fields = ['id', 'item', 'price', 'user', 'status']


class BidView(ListAPIView,CreateAPIView):
    queryset = models.BidRecord.objects.all().order_by('-id')
    serializer_class = BidModelSerializer

    def get_queryset(self):
        item_id = self.request.query_params.get('item_id')
        return self.queryset.filter(item_id=item_id)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        item_id = self.request.query_params.get('item_id')
        item_obj = models.AuctionItem.objects.filter(id=item_id).first()
        max_price = models.BidRecord.objects.filter(item_id=item_id).aggregate(max_price=Max('price'))['max_price']
        # max_price_obj = models.BidRecord.objects.filter(item_id=item_id).order_by('-price').first()
        # max_price = max_price_obj.values()['price']
        result = {
            'unit': item_obj.unit,
            'price': max_price or item_obj.start_price,
            'data': response.data
        }
        response.data = result
        return response
    def perform_create(self, serializer):
        with transaction.atomic():
            price = self.request.data.get('price')
            item_id = self.request.data.get('item_id')
            max_price = models.BidRecord.objects.select_for_update().filter(item_id=item_id).aggregate(max_price=Max('price'))['max_price']
            if price > max_price:
                serializer.save(user=self.request.user)
            raise exceptions.ValidationError('已经有人出价,请加价')

