from friendsservice.friendship.exceptions import FriendshipRequestDoesNotExistsError
from friendsservice.friendship.models import UserFriendship, FriendshipStatus


class ChangeFriendshipStatusService:

    def __init__(self, friendship: int | UserFriendship, status: FriendshipStatus):
        self.friendship = friendship if isinstance(friendship, UserFriendship) else self._get_friendship(friendship)
        self.status = status

    @staticmethod
    def _get_friendship(friendship_id: int) -> UserFriendship:
        try:
            return UserFriendship.objects.get(id=friendship_id, status=FriendshipStatus.ACTIVE.value)
        except UserFriendship.DoesNotExist as exc:
            raise FriendshipRequestDoesNotExistsError from exc

    def _change_status(self) -> None:
        self.friendship.status = self.status.value
        self.friendship.save()

    def __call__(self) -> None:
        self._change_status()
