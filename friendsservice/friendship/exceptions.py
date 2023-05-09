class UserDoesNotExistsError(Exception):
    """User not found in database"""


class UserCannotBeFriendError(Exception):
    """Deleted friendship status"""


class FriendshipRequestAlreadyExistsError(Exception):
    """Deleted friendship status"""
