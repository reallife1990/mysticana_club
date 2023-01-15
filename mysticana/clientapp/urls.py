from clientapp import views
from clientapp.apps import ClientappConfig
from django.urls.conf import path

app_name = ClientappConfig.name

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('services/', views.ServicesView.as_view(), name='services'),
    # path('news/', views.NewsView.as_view(), name='news'),
    # path('news/<pk>/', views.NewsDetailView.as_view(), name='news_detail'),
]