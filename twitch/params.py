from .exception import ValidationError


class BaseParam:

    required = False

    def __init__(
        self,
        name,
        types=None,
        required=False,
        minimum=None,
        maximum=None,
        data_format=None,
        required_set=None,
    ):
        self.name = name
        self.types = types
        self.required = required
        self.minimum = minimum
        self.maximum = maximum
        self.data_format = data_format
        self.required_set = required_set

    def validate(self, value):

        if value and not isinstance(value, getattr(self.types, "__args__", self.types)):
            raise ValidationError(message=f"{self.name} must be {self.types}")

        if self.required & (value is None):
            raise ValidationError(message=f"{self.name} is required")

        if getattr(self, "minimum", None) and (value and value < self.minimum):
            raise ValidationError(
                message=f"{self.name} must be greater than {getattr(self, 'minimum')}"
            )

        if getattr(self, "maximum", None) and (value and value > self.maximum):
            raise ValidationError(
                message=f"{self.name} must be lower than {getattr(self, 'maximum')}"
            )
