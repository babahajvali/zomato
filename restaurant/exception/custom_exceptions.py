class AlreadyExistsRestaurant(Exception):
    def __init__(self, names):
        self.names = names
        super().__init__(f"Restaurants already exist: {', '.join(names)}")


class DuplicateRestaurants(Exception):
    def __init__(self, names):
        self.names = names
        super().__init__(f"Duplicate restaurants found: {', '.join(names)}")


class OwnerNotFound(Exception):
    def __init__(self, email):
        self.email = email
        super().__init__(f"Owner not found: {email}")
