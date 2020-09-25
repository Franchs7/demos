from django.conf.urls import url
from django.urls import path, re_path
from api.views import auth, news, auction

urlpatterns = [
    path('code/', auth.MessageView.as_view()),
    path('login/', auth.LoginView.as_view()),
    path('topic/', news.TopicView.as_view()),
    # url(r'^news/$', NewsView.as_view()),
    # url(r'^news/(?P<pk>\d+)/$', NewsDetailView.as_view()),
    path('news/', news.NewsView.as_view()),
    path('news/<int:pk>/', news.NewsDetailView.as_view()),
    path('comment/', news.CommentView.as_view()),
    path('favor/', news.FavorView.as_view()),

    path('auction/', auction.AuctionView.as_view()),
    path('auction/<int:pk>/', auction.AuctionDetailView.as_view()),
    path('auction/item/<int:pk>/', auction.AuctionItemDetailView.as_view()),
    path('auction/deposit/<int:pk>/', auction.DepositView.as_view()),
    path('auction/bid/', auction.BidView.as_view()),
]