from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase

User = get_user_model()


class BaseTestCase(TestCase):
    first_user: User
    first_username: str = 'first'

    second_user: User
    second_username: str = 'second'

    third_user: User
    third_username: str = 'third'

    unexpected_username: str = 'spy_user'

    users_count: int

    @classmethod
    def setUpClass(cls) -> None:
        cls.first_user = cls.get_or_create_user(cls.first_username, 'test_pass')
        cls.second_user = cls.get_or_create_user(cls.second_username, 'test_pass')
        cls.third_user = cls.get_or_create_user(cls.third_username, 'test_pass')
        cls.users_count = User.objects.count()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.first_user.delete()
        cls.second_user.delete()
        cls.third_user.delete()

    @classmethod
    def get_or_create_user(cls, username: str, password: str) -> User:
        user, _ = User.objects.get_or_create(
            username=username,
            password=make_password(password)
        )
        return user
