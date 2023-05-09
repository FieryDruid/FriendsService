from django.urls import path

from friendsservice.api_v1.user.views import (
    UserView, AddUserView, UserSentFriendshipView
)

app_name = 'user'

urlpatterns = [
    path('', UserView.as_view(), name='user_api'),
    path('add_to_friends/', AddUserView.as_view(), name='add_to_friends'),

    path('friendship/sent/', UserSentFriendshipView.as_view(), name='sent_requests'),

]
