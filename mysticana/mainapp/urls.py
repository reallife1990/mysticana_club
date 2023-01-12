from django.urls import path
from mainapp.apps import MainappConfig
from mainapp import views


app_name = MainappConfig.name

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/<pk>/', views.NewsDetailView.as_view(), name='news_detail'),
]