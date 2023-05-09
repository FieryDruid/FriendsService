from django.urls import path

from friendsservice.api_v1.user.views import (
    CreateUserView, AddUserView, UserSentFriendshipView, UserReceivedFriendshipView, AcceptFriendshipRequestView,
    DeclineFriendshipRequestView, UserFriendshipView, UserFriendsView
)

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('add_to_friends/', AddUserView.as_view(), name='add_to_friends'),

    path('friendship/sent/', UserSentFriendshipView.as_view(), name='sent_requests'),
    path('friendship/received/', UserReceivedFriendshipView.as_view(), name='received_requests'),

    path(
        'friendship/<int:friendship_id>/accept/',
        AcceptFriendshipRequestView.as_view(),
        name='accept_friendship_request'
    ),
    path(
        'friendship/<int:friendship_id>/decline/',
        DeclineFriendshipRequestView.as_view(),
        name='decline_friendship_request'
    ),
    path('friendship/<str:username>/', UserFriendshipView.as_view(), name='friendship'),

    path('friends/', UserFriendsView.as_view(), name='user_friends'),
]
