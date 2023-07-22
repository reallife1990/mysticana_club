from django.contrib import admin
from django.urls import path
from mainapp.apps import MainappConfig
from mainapp import views


app_name = MainappConfig.name

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('services/<pk>', views.ServiceDetailView.as_view(), name='service_detail'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/<pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('profile/', views.AddProfileView.as_view(), name='add_profile'),
    path('profile/', views.AddProfileView.as_view(), name='edit_profile'),
]