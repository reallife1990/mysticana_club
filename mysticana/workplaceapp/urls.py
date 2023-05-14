from django.urls import path
from workplaceapp.apps import WorkplaceappConfig
from workplaceapp import views


app_name = WorkplaceappConfig.name

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    # path('services/', views.ServicesView.as_view(), name='services'),
    path('clients/', views.ShowAllClientsView.as_view(), name='all_clients'),

    path('client/<uuid:pk>', views.ShowClientView.as_view(), name='client_detail'),
    path('add_client', views.AddClientView.as_view(), name='add_client'),

    path('services/', views.AllServicesView.as_view(), name='all_services'),
    path('services/<int:pk>', views.EditServicesView.as_view(), name='edit_service'),
]