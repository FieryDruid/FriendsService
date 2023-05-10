from django.contrib.auth import get_user_model

from friendsservice.friendship.exceptions import (
    FriendshipRequestAlreadyExistsError, UserDoesNotExistsError, UserCannotBeFriendError
)
from friendsservice.friendship.models import UserFriendship, FriendshipStatus
from friendsservice.friendship.services.add_to_friends import AddToFriendsService
from friendsservice.friendship.tests.base import BaseTestCase

User = get_user_model()


class AddToFriendsServiceTestCase(BaseTestCase):
    service = AddToFriendsService

    def tearDown(self) -> None:
        UserFriendship.objects.all().delete()

    @staticmethod
    def get_friendship_from(from_user: User, to_user: User) -> UserFriendship:
        return UserFriendship.objects.get(
            sender=from_user,
            recipient=to_user
        )

    def test_create_friendship(self):
        base_friendships_count = UserFriendship.objects.count()

        service = self.service(self.first_user, self.second_username)
        service()
        self.assertGreater(UserFriendship.objects.count(), base_friendships_count)

        created_friendship = self.get_friendship_from(self.first_user, self.second_user)
        self.assertEqual(created_friendship.status, FriendshipStatus.ACTIVE.value)

    def test_create_duplicate_friendship_from_one_user(self):
        service = self.service(self.first_user, self.second_username)
        service()
        after_first_service_call_friendships_count = UserFriendship.objects.count()
        with self.assertRaises(FriendshipRequestAlreadyExistsError):
            service()
        self.assertEqual(UserFriendship.objects.count(), after_first_service_call_friendships_count)

    def test_create_friendship_with_bad_username(self):
        base_friendships_count = UserFriendship.objects.count()
        service = self.service(self.first_user, self.unexpected_username)
        with self.assertRaises(UserDoesNotExistsError):
            service()
        self.assertEqual(UserFriendship.objects.count(), base_friendships_count)

    def test_create_friendship_with_same_user(self):
        base_friendships_count = UserFriendship.objects.count()
        with self.assertRaises(UserCannotBeFriendError):
            self.service(self.first_user, self.first_username)
        self.assertEqual(UserFriendship.objects.count(), base_friendships_count)

    def test_create_confirmed_friendship(self):
        base_friendships_count = UserFriendship.objects.count()
        service = self.service(self.first_user, self.second_username)
        service()
        friendships_count_after_service_call = UserFriendship.objects.count()
        self.assertGreater(friendships_count_after_service_call, base_friendships_count)

        service = self.service(self.second_user, self.first_username)
        service()
        self.assertEqual(UserFriendship.objects.count(), friendships_count_after_service_call)

        created_friendship = self.get_friendship_from(self.first_user, self.second_user)
        self.assertEqual(created_friendship.status, FriendshipStatus.CONFIRMED.value)

    def test_create_friendship_after_confirmed(self):
        base_friendships_count = UserFriendship.objects.count()
        service = self.service(self.first_user, self.second_username)
        service()
        friendships_count_after_service_call = UserFriendship.objects.count()
        self.assertGreater(friendships_count_after_service_call, base_friendships_count)

        service = self.service(self.second_user, self.first_username)
        service()
        self.assertEqual(UserFriendship.objects.count(), friendships_count_after_service_call)

        created_friendship = self.get_friendship_from(self.first_user, self.second_user)
        self.assertEqual(created_friendship.status, FriendshipStatus.CONFIRMED.value)

        service = self.service(self.second_user, self.first_username)
        service()
        self.assertEqual(UserFriendship.objects.count(), friendships_count_after_service_call)

    def test_create_friendship_after_declined(self):
        UserFriendship.objects.create(
            sender=self.first_user,
            recipient=self.second_user,
            status=FriendshipStatus.DECLINED.value
        )
        base_friendships_count = UserFriendship.objects.count()
        service = self.service(self.second_user, self.first_username)
        with self.assertRaises(UserCannotBeFriendError):
            service()

        self.assertEqual(UserFriendship.objects.count(), base_friendships_count)
