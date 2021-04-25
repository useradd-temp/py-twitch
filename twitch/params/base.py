from ..exception import ValidationError


class BaseParam:

    required = False

    def __init__(self, name, types=None, required=False, minimum=None, maximum=None, format=None):
        self.name = name
        self.types = types
        self.required = required
        self.minimum = minimum
        self.maximum = maximum
        self.format = format

    def validate(self, value):

        if value and not isinstance(value, self.types):
            raise ValidationError(message=f"{self.name} must be {self.types}")

        if self.required & (value is None):
            raise ValidationError(message=f"{self.name} is required")

        if getattr(self, "minimum", None) and (value and value < self.minimum):
            raise ValidationError(
                message=f"{self.name} must be greater than {self.minimum}"
            )

        if getattr(self, "maximum", None) and (value and value > self.maximum):
            raise ValidationError(
                message=f"{self.name} must be lower than {self.minimum}"
            )

    # @classmethod
    # def __prepare__(metacls, name, bases):
    #     pass
    #
    # def __new__(cls, *args, **kwargs):
    #     pass
