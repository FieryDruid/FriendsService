from django.contrib.auth import get_user_model
from django.db.models import Q

from friendsservice.friendship.models import UserFriendship, FriendshipStatus

User = get_user_model()


class GetFriendsListService:

    def __init__(self, user: User):
        self.user = user

    def _get_friends_usernames_list(self) -> list[str]:
        confirmed_friendships = UserFriendship.objects.filter(
            Q(recipient=self.user) | Q(sender=self.user) & Q(status=FriendshipStatus.CONFIRMED.value)
        )
        users_list = []
        for friendship in confirmed_friendships:
            users_list.append(
                friendship.sender.username if friendship.sender != self.user else friendship.username
            )
        return users_list

    def __call__(self) -> list[str]:
        return self._get_friends_usernames_list()
