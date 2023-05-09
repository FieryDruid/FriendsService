from django.contrib.auth import get_user_model
from django.db.models import Q

from friendsservice.friendship.exceptions import (
    UserDoesNotExistsError, UserCannotBeFriendError, FriendshipRequestAlreadyExistsError
)
from friendsservice.friendship.models import UserFriendship, FriendshipStatus

User = get_user_model()


class AddToFriendsService:

    def __init__(self, sender: User, recipient_username: str):
        self.sender = sender
        if self.sender.username == recipient_username:
            raise UserCannotBeFriendError
        self.recipient_username = recipient_username
        self.recipient: User | None = None

    def _get_recipient(self) -> None:
        try:
            self.recipient = User.objects.get(username=self.recipient_username)
        except User.DoesNotExist as exc:
            raise UserDoesNotExistsError from exc

    @property
    def _exist_request(self) -> UserFriendship | None:
        return UserFriendship.objects.filter(
            (Q(recipient=self.sender, sender=self.recipient) | Q(recipient=self.recipient, sender=self.sender))
        ).first()

    @property
    def _deleted_friendship_status(self) -> UserFriendship | None:
        return UserFriendship.objects.filter(
            (Q(recipient=self.sender, sender=self.recipient) | Q(recipient=self.recipient, sender=self.sender))
            & Q(status=FriendshipStatus.DELETED.value)
        ).first()

    def _create_friendship(self) -> None:
        exist_request = self._exist_request

        if not exist_request or (exist_request and exist_request.status == FriendshipStatus.DECLINED.value):
            UserFriendship.objects.create(
                sender=self.sender,
                recipient=self.recipient,
            )
            return

        if exist_request.status == FriendshipStatus.DELETED.value:
            raise UserCannotBeFriendError

        if exist_request.status == FriendshipStatus.CONFIRMED.value:
            return
        
        if exist_request.status == FriendshipStatus.ACTIVE.value and exist_request.recipient == self.sender:
            exist_request.status = FriendshipStatus.CONFIRMED.value
            exist_request.save()
            return

        raise FriendshipRequestAlreadyExistsError

    def __call__(self) -> None:
        self._get_recipient()
        self._create_friendship()
