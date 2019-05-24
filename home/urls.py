from django.urls import path
from home.views import home, register, account_activation_sent, activate

urlpatterns = [
    path('',home , name='home'),
    path('register', register, name='register'),
    path('account_activation_sent',account_activation_sent,name='account_activation_sent'),
    path('activate/<uidb64>/<token>',activate, name='activate')

]
