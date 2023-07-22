from django.urls import path
from workplaceapp.apps import WorkplaceappConfig
from workplaceapp import views


app_name = WorkplaceappConfig.name

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    # path('services/', views.ServicesView.as_view(), name='services'),
    path('clients/', views.ShowAllClientsView.as_view(), name='all_clients'),

    path('client/<uuid:pk>', views.ShowClientView.as_view(), name='client_detail'),
    path('client/add', views.AddClientView.as_view(), name='add_client'),

    path('services/', views.AllServicesView.as_view(), name='all_services'),
    path('services/add', views.AddServiceView.as_view(), name='add_services'),
    path('services/history/', views.HistoryServicesView.as_view(), name='history_services'),
    path('services/<int:pk>', views.EditServicesView.as_view(), name='edit_service'),


    path('news/', views.AllNewsView.as_view(), name='all_news'),
    path('news/<int:pk>', views.EditNewsView.as_view(), name='edit_news'),
    path('news/add', views.AddNewsView.as_view(), name='add_news'),

    path('express/', views.ExpressCalcChangeView.as_view(), name='express_begin'),
]