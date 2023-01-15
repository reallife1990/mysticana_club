from django.contrib.auth.views import PasswordChangeView

from authapp.apps import AuthappConfig
from django.urls import path
from authapp.views import CustomLoginView, CustomLogoutView, RegisterView, CustomEditView,ConfirmEmailView

app_name = AuthappConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit/', CustomEditView.as_view(), name='edit'),
    path('confirm/', ConfirmEmailView.as_view(), name='confirm'),
    #path('password/', PasswordChangeView.as_view(), name='password_change'),
]