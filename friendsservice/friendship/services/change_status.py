from django.contrib.auth import get_user_model

from friendsservice.friendship.exceptions import FriendshipRequestDoesNotExistsError, SelfFriendshipRequestAcceptError
from friendsservice.friendship.models import UserFriendship, FriendshipStatus

User = get_user_model()


class ChangeFriendshipStatusService:

    def __init__(self, friendship: int | UserFriendship, status: FriendshipStatus, user: User | None = None):
        self.friendship = friendship if isinstance(friendship, UserFriendship) else self._get_friendship(friendship)
        self.user = user
        self.status = status

    @staticmethod
    def _get_friendship(friendship_id: int) -> UserFriendship:
        try:
            return UserFriendship.objects.get(id=friendship_id, status=FriendshipStatus.ACTIVE.value)
        except UserFriendship.DoesNotExist as exc:
            raise FriendshipRequestDoesNotExistsError from exc

    def _change_status(self) -> None:
        if self.status == FriendshipStatus.CONFIRMED and self.user and self.friendship.sender == self.user:
            raise SelfFriendshipRequestAcceptError
        self.friendship.status = self.status.value
        self.friendship.save()

    def __call__(self) -> None:
        self._change_status()
