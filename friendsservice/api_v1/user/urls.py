from django.urls import path

from friendsservice.api_v1.user.views import UserView

app_name = 'user'

urlpatterns = [
    path('', UserView.as_view(), name='user_api'),
]
