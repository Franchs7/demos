from django.db import models


# Create your models here.
class UserInfo(models.Model):
    phone = models.CharField(max_length=11, verbose_name='手机号')
    token = models.CharField(max_length=64, verbose_name='用户token', null=True, blank=True)
    avatar = models.CharField(verbose_name='头像', max_length=64, null=True, blank=True)
    nickname = models.CharField(verbose_name='昵称', max_length=64, null=True, blank=True)
    balance = models.PositiveIntegerField(verbose_name='余额', default=1000)

class Topic(models.Model):
    title = models.CharField(max_length=64, verbose_name='标题')
    count = models.PositiveIntegerField(verbose_name='关注度', default=0)


class News(models.Model):
    cover = models.CharField(verbose_name='封面', max_length=128)
    content = models.CharField(verbose_name='内容', max_length=255)
    topic = models.ForeignKey(verbose_name='话题', to='Topic', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='发布者', to='UserInfo', related_name='news', on_delete=models.CASCADE)
    address = models.CharField(verbose_name='位置', max_length=128, null=True, blank=True)
    favor_count = models.PositiveIntegerField(verbose_name='赞数', default=0)
    viewer_count = models.PositiveIntegerField(verbose_name='浏览数', default=0)
    comment_count = models.PositiveIntegerField(verbose_name='评论数', default=0)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class NewsDetails(models.Model):
    key = models.CharField(verbose_name='腾讯云图片储存文件名', max_length=128, help_text='用于以后在腾讯对象存储中删除')
    cos_path = models.CharField(verbose_name='腾讯云图片存储路径', max_length=128)
    news = models.ForeignKey(to='News', verbose_name='动态', on_delete=models.CASCADE)


class ViewRecord(models.Model):
    news = models.ForeignKey(verbose_name='动态', to='News', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)


class NewsFavorRecord(models.Model):
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    news = models.ForeignKey(verbose_name='动态', to='News', on_delete=models.CASCADE)


class CommentRecord(models.Model):
    news = models.ForeignKey(verbose_name='动态', to='News', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复', to='self', null=True, blank=True, on_delete=models.CASCADE,
                              related_name='replys')
    depth = models.PositiveIntegerField(verbose_name='评论层级', default=1)
    root = models.ForeignKey(verbose_name='根评论', to='self', null=True, blank=True, on_delete=models.CASCADE,
                             related_name="roots")

    favor_count = models.PositiveIntegerField(verbose_name='赞数', default=0)


class CommentFavorRecord(models.Model):
    comment = models.ForeignKey(verbose_name='评论', to='CommentRecord', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)


class Auction(models.Model):
    status_choices = (
        (0, '未开拍'),
        (1, '预展中'),
        (2, '拍卖中'),
        (3, '已结束')
    )
    status = models.PositiveSmallIntegerField(verbose_name='拍卖状态', choices=status_choices, default=1)
    title = models.CharField(verbose_name='标题', max_length=32)
    cover = models.CharField(verbose_name='封面', max_length=128)
    video = models.CharField(verbose_name='预览视频', max_length=128, null=True, blank=True)

    preview_start_time = models.DateTimeField(verbose_name='预展开始时间')
    preview_end_time = models.DateTimeField(verbose_name='预展结束时间')

    auction_start_time = models.DateTimeField(verbose_name='专场开始时间')
    auction_end_time = models.DateTimeField(verbose_name='专场结束时间')

    deposit = models.PositiveIntegerField(verbose_name='全场保证金', default=1000)

    total_price = models.PositiveIntegerField(verbose_name='总成交额', null=True, blank=True)
    goods_count = models.PositiveIntegerField(verbose_name='拍品数量', default=0)
    bid_count = models.PositiveIntegerField(verbose_name='出价次数', default=0)
    look_count = models.PositiveIntegerField(verbose_name='围观次数', default=0)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = '拍卖系列'

    def __str__(self):
        return self.title


class AuctionItem(models.Model):
    auction = models.ForeignKey(to='Auction', verbose_name='拍卖专场', on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='图录号', max_length=12)
    status_choices = (
        (1, '待拍卖'),
        (2, '预展中'),
        (3, '拍卖中'),
        (4, '成交'),
        (5, '流拍'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    title = models.CharField(verbose_name='拍品名称', max_length=32)
    cover = models.CharField(verbose_name='拍品封面', max_length=128)

    start_price = models.PositiveIntegerField(verbose_name='起拍价')
    deal_price = models.PositiveIntegerField(verbose_name='成交价', null=True, blank=True)

    reserve_price = models.PositiveIntegerField(verbose_name='参考底价')
    highest_price = models.PositiveIntegerField(verbose_name='参考高价')

    video = models.CharField(verbose_name='预览视频', max_length=128, null=True, blank=True)
    deposit = models.PositiveIntegerField(verbose_name='单品保证金', default=100)
    unit = models.PositiveIntegerField(verbose_name='加价幅度', default=100)

    bid_count = models.PositiveIntegerField(verbose_name='出价次数', default=0)
    look_count = models.PositiveIntegerField(verbose_name='围观次数', default=0)

    class Meta:
        verbose_name_plural = '拍品'

    def __str__(self):
        return self.title

class AuctionItemImage(models.Model):
    """
    拍品相关图片
    """
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem', on_delete=models.CASCADE)
    img = models.CharField(verbose_name='详细图', max_length=64)
    carousel = models.BooleanField(verbose_name='是否在轮播中显示', default=False)
    order = models.FloatField(verbose_name="排序", default=1)

    class Meta:
        verbose_name_plural = '拍品详细图'

    def __str__(self):
        return "{}-{}".format(self.item.title, self.id, )

class AuctionItemDetail(models.Model):
    """
    拍品详细规格
    """
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem', on_delete=models.CASCADE)
    key = models.CharField(verbose_name='项', max_length=16)
    value = models.CharField(verbose_name='值', max_length=32)

    class Meta:
        verbose_name_plural = '拍品规格'

class BrowseRecord(models.Model):
    """
    浏览记录
    """
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem', on_delete=models.CASCADE)

    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)

class BidRecord(models.Model):
    """
    出价记录
    """
    status_choices = (
        (1, '竞价'),
        (2, '成交'),
        (3, '逾期未付款'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='出价人', to='UserInfo', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='出价')

class DepositRecord(models.Model):
    """ 保证金 """
    status_choices = (
        (1, '未支付'),
        (2, '支付成功')
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

    uid = models.CharField(verbose_name='流水号', max_length=64)
    deposit_type_choices = (
        (1, '单品保证金'),
        (2, '全场保证金')
    )
    deposit_type = models.SmallIntegerField(verbose_name='保证金类型', choices=deposit_type_choices)
    pay_type_choices = (
        (1, '微信'),
        (2, '余额')
    )
    pay_type = models.SmallIntegerField(verbose_name='支付方式', choices=pay_type_choices)

    amount = models.PositiveIntegerField(verbose_name='金额')

    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)

    # 单品保证金则设置值，全场保证金，则为空
    item = models.ForeignKey(verbose_name='拍品', to='AuctionItem', null=True, blank=True, on_delete=models.CASCADE)
    auction = models.ForeignKey(verbose_name='拍卖专场', to='Auction', on_delete=models.CASCADE)