class AlreadyExistsPromoCode(Exception):
    def __init__(self, codes):
        self.codes = codes


class DuplicatePromoCodes(Exception):
    def __init__(self, codes):
        self.codes = codes

class EmptyPromoCodeFound(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidPromoCodeDateRange(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
