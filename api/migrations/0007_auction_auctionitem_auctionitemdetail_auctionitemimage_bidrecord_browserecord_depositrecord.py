# Generated by Django 3.0.3 on 2020-08-05 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200805_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '未开拍'), (1, '预展中'), (2, '拍卖中'), (3, '已结束')], default=1, verbose_name='拍卖状态')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('cover', models.CharField(max_length=128, verbose_name='封面')),
                ('video', models.CharField(blank=True, max_length=128, null=True, verbose_name='预览视频')),
                ('preview_start_time', models.DateTimeField(verbose_name='预展开始时间')),
                ('preview_end_time', models.DateTimeField(verbose_name='预展结束时间')),
                ('auction_start_time', models.DateTimeField(verbose_name='专场开始时间')),
                ('auction_end_time', models.DateTimeField(verbose_name='专场结束时间')),
                ('deposit', models.PositiveIntegerField(default=1000, verbose_name='全场保证金')),
                ('total_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='总成交额')),
                ('goods_count', models.PositiveIntegerField(default=0, verbose_name='拍品数量')),
                ('bid_count', models.PositiveIntegerField(default=0, verbose_name='出价次数')),
                ('look_count', models.PositiveIntegerField(default=0, verbose_name='围观次数')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '拍卖系列',
            },
        ),
        migrations.CreateModel(
            name='AuctionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=12, verbose_name='图录号')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '待拍卖'), (2, '预展中'), (3, '拍卖中'), (4, '成交'), (5, '流拍')], default=1, verbose_name='状态')),
                ('title', models.CharField(max_length=32, verbose_name='拍品名称')),
                ('cover', models.CharField(max_length=128, verbose_name='拍品封面')),
                ('start_price', models.PositiveIntegerField(verbose_name='起拍价')),
                ('deal_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='成交价')),
                ('reserve_price', models.PositiveIntegerField(verbose_name='参考底价')),
                ('highest_price', models.PositiveIntegerField(verbose_name='参考高价')),
                ('video', models.CharField(blank=True, max_length=128, null=True, verbose_name='预览视频')),
                ('deposit', models.PositiveIntegerField(default=100, verbose_name='单品保证金')),
                ('unit', models.PositiveIntegerField(default=100, verbose_name='加价幅度')),
                ('bid_count', models.PositiveIntegerField(default=0, verbose_name='出价次数')),
                ('look_count', models.PositiveIntegerField(default=0, verbose_name='围观次数')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Auction', verbose_name='拍卖专场')),
            ],
            options={
                'verbose_name_plural': '拍品',
            },
        ),
        migrations.CreateModel(
            name='DepositRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '未支付'), (2, '支付成功')], default=1, verbose_name='状态')),
                ('uid', models.CharField(max_length=64, verbose_name='流水号')),
                ('deposit_type', models.SmallIntegerField(choices=[(1, '单品保证金'), (2, '全场保证金')], verbose_name='保证金类型')),
                ('pay_type', models.SmallIntegerField(choices=[(1, '微信'), (2, '余额')], verbose_name='支付方式')),
                ('amount', models.PositiveIntegerField(verbose_name='金额')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Auction', verbose_name='拍卖专场')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.AuctionItem', verbose_name='拍品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserInfo', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='BrowseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AuctionItem', verbose_name='拍品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserInfo', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='BidRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '竞价'), (2, '成交'), (3, '逾期未付款')], default=1, verbose_name='状态')),
                ('price', models.PositiveIntegerField(verbose_name='出价')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AuctionItem', verbose_name='拍品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserInfo', verbose_name='出价人')),
            ],
        ),
        migrations.CreateModel(
            name='AuctionItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=64, verbose_name='详细图')),
                ('carousel', models.BooleanField(default=False, verbose_name='是否在轮播中显示')),
                ('order', models.FloatField(default=1, verbose_name='排序')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AuctionItem', verbose_name='拍品')),
            ],
            options={
                'verbose_name_plural': '拍品详细图',
            },
        ),
        migrations.CreateModel(
            name='AuctionItemDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=16, verbose_name='项')),
                ('value', models.CharField(max_length=32, verbose_name='值')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AuctionItem', verbose_name='拍品')),
            ],
            options={
                'verbose_name_plural': '拍品规格',
            },
        ),
    ]
