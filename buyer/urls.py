from django.urls import path
from buyer.views import AccountView
urlpatterns = [
    path('user-profile', AccountView.as_view(), name="user-profile")
]
