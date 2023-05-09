from django.contrib.auth import get_user_model
from django.db.models import Q

from friendsservice.friendship.exceptions import UserDoesNotExistsError, UserNotInFriendsListError
from friendsservice.friendship.models import UserFriendship, FriendshipStatus
from friendsservice.friendship.services.change_status import ChangeFriendshipStatusService

User = get_user_model()


class DeleteFromFriendsService:

    def __init__(self, sender: User, target_username: str):
        if sender.username == target_username:
            raise UserNotInFriendsListError
        self.sender = sender
        self.target_user = self._get_user(target_username)

    @staticmethod
    def _get_user(username: str) -> User:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExists as exc:
            raise UserDoesNotExistsError from exc

    def _get_active_friendship(self) -> UserFriendship | None:
        return UserFriendship.objects.filter(
            Q(recipient=self.sender, sender=self.target_user) | Q(recipient=self.target_user, sender=self.sender)
        ).first()

    def _delete_from_friends(self) -> None:
        active_friendship = self._get_active_friendship()
        if not active_friendship:
            raise UserNotInFriendsListError

        ChangeFriendshipStatusService(active_friendship, FriendshipStatus.DECLINED)()

    def __call__(self) -> None:
        self._delete_from_friends()
