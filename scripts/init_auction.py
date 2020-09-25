import os, sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demos.settings')
django.setup()
from datetime import datetime, timedelta
from api import models


def create_auction():
    current_time = datetime.now()
    auction_object = models.Auction.objects.create(
        title="第一场 烟酒",
        cover="http://fdjisfhas9ofas.cn",
        preview_start_time=current_time,
        preview_end_time=current_time + timedelta(hours=5),
        auction_start_time=current_time + timedelta(hours=5),
        auction_end_time=current_time + timedelta(hours=7),
        deposit=1200,
        goods_count=2,
    )
    item_object = models.AuctionItem.objects.create(
        auction=auction_object,
        uid="20201111111",
        title='茅台',
        cover="https://fsduisdfiusbf.cn",
        start_price=1499,
        reserve_price=1000,
        highest_price=2800,
        deposit=200,
        unit=100,
    )
    models.AuctionItemImage.objects.create(
        item=item_object,
        img="https://fsduisdfiusbf.cn",
        carousel = True,
    )
    models.AuctionItemImage.objects.create(
        item=item_object,
        img="https://fsduisdfiusbf.cn",
        carousel=True,
    )
    models.AuctionItemImage.objects.create(
        item=item_object,
        img="https://fsduisdfiusbf.cn",
        carousel=True,
    )
    models.AuctionItemDetail.objects.create(
        item = item_object,
        key = '品牌',
        value="茅台"
    )
    models.AuctionItemDetail.objects.create(
        item=item_object,
        key='年份',
        value="1800"
    )
    models.AuctionItem.objects.create(
        auction=auction_object,
        uid="20201111112",
        title='五粮液',
        cover="https://fsduisdfiusbf.cn",
        start_price=1499,
        reserve_price=1000,
        highest_price=2800,
        deposit=200,
        unit=100,
    )
def create_bid_record():
    models.BidRecord.objects.create(item_id=1, user_id=1,price=1000)
    models.BidRecord.objects.create(item_id=1, user_id=1,price=1200)
if __name__ == '__main__':
    # create_auction()
    create_bid_record()