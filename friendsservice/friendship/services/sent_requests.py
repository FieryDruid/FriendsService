from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from friendsservice.friendship.models import UserFriendship, FriendshipStatus

User = get_user_model()


class GetSentFriendshipRequestsService:

    def __init__(self, user: User):
        self.user = user

    def _get_requests(self) -> QuerySet[UserFriendship]:
        return UserFriendship.objects.filter(sender=self.user, status=FriendshipStatus.ACTIVE.value)

    def __call__(self) -> QuerySet[UserFriendship]:
        return self._get_requests()
