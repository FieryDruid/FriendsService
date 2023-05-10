class UserDoesNotExistsError(Exception):
    """User not found in database"""


class UserCannotBeFriendError(Exception):
    """User cannot be friend"""


class FriendshipRequestAlreadyExistsError(Exception):
    """Friendship request already exists"""


class FriendshipRequestDoesNotExistsError(Exception):
    """Friendship request does not exists"""


class SelfFriendshipRequestAcceptError(Exception):
    """Friendship request does not exists"""


class UserNotInFriendsListError(Exception):
    """User not in friends list"""


class HasActiveFriendship(Exception):
    """Has active friendship"""

    def __init__(self, friendship_status: str):
        self.friendship_status = friendship_status
