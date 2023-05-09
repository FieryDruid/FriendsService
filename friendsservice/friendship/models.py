from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class FriendshipStatus(Enum):
    ACTIVE = 'active'
    CONFIRMED = 'confirmed'
    DECLINED = 'declined'
    DELETED = 'deleted'

    @classmethod
    def to_choices(cls) -> list[tuple[str, str]]:
        return [(item.value, item.value) for item in cls]


class UserFriendship(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_requests'
    )
    status = models.CharField(choices=FriendshipStatus.to_choices(), default=FriendshipStatus.ACTIVE.value)

    def __str__(self) -> str:
        return f'{self.status} friendship from {self.sender} to {self.recipient}'
