from django.urls import path

from api.views.news import MessageView,LoginView

urlpatterns = [
    path('code/', MessageView.as_view()),
    path('login/', LoginView.as_view())
]