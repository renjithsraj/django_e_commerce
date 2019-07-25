from django.urls import path
from buyer.views import AccountView, AccountLoginView
urlpatterns = [
    path('user-profile', AccountView.as_view(), name="user-profile"),
    path('account-login', AccountLoginView.as_view(), name="account-login"),
]
