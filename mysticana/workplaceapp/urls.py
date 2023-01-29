from django.urls import path
from workplaceapp.apps import WorkplaceappConfig
from workplaceapp import views


app_name = WorkplaceappConfig.name

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    # path('services/', views.ServicesView.as_view(), name='services'),
    path('all_clients/', views.ShowAllClientsView.as_view(), name='all_clients'),
]