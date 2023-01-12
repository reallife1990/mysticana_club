from django.urls import path
from workplaceapp.apps import WorkplaceappConfig
from workplaceapp import views


app_name = WorkplaceappConfig.name

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    # path('services/', views.ServicesView.as_view(), name='services'),
    # path('news/', views.NewsView.as_view(), name='news'),
]