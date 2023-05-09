from django.contrib.auth import get_user_model
from django.db.models import Q

from friendsservice.friendship.exceptions import FriendshipRequestDoesNotExistsError, HasActiveFriendship
from friendsservice.friendship.models import UserFriendship, FriendshipStatus

User = get_user_model()


class CheckFriendshipStatusService:

    def __init__(self, target_username: str):
        self.target_username = target_username

    def _get_user(self) -> User:
        try:
            return User.objects.get(username=self.target_username)
        except User.DoesNotExists as exc:
            raise FriendshipRequestDoesNotExistsError from exc

    def _check_status(self) -> None:
        target_user = self._get_user()
        friendship_with_user = (
            UserFriendship.objects.filter(Q(recipient=target_user) | Q(sender=target_user))
            .exclude(Q(status=FriendshipStatus.DECLINED.value))
            .first()
        )

        if not friendship_with_user:
            raise FriendshipRequestDoesNotExistsError

        if friendship_with_user.status == FriendshipStatus.CONFIRMED.value:
            message = 'In friends list'
        elif friendship_with_user.sender == target_user:
            message = f'You have active friends request from {self.target_username}'
        else:
            message = f'You have active friends request to {self.target_username}'

        raise HasActiveFriendship(friendship_status=message)

    def __call__(self) -> None:
        self._check_status()
