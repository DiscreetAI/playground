class ValidatorBase:
    """
    Validator Base Class

    Just the basic format of a data validator.

    """

    def __init__(self, data):
        self.data = data

    def validate(self):
        return self.data
