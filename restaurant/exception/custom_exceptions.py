class AlreadyExistsRestaurant(Exception):
    def __init__(self, names):
        self.names = names

    def __str__(self):
        return str(self.names)


class DuplicateRestaurants(Exception):
    def __init__(self, names):
        self.names = names

    def __str__(self):
        return str(self.names)


class OwnerNotFound(Exception):
    def __init__(self, email):
        self.email = email

    def __str__(self):
        return str(self.email)


class OpenTimeGreaterThanCloseTime(Exception):
    def __init__(self, open_time, close_time):
        self.open_time = open_time
        self.close_time = close_time

    def __str__(self):
        return f"{self.open_time} --> {self.close_time}"


class RestaurantTimingNotFound(Exception):
    def __init__(self, id: int):
        self.id = id


class UserIsNotRestaurantOwner(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __str__(self):
        return str(self.user_id)
