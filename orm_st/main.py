class Field:
    field_type = None
    sql_type = None

    def __init__(self, required=False, default=None):
        self.required = required
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__.__get__(self.name)

    def __set__(self, instance, value):

        # Added field type validation
        if not isinstance(value, self.field_type):
            raise TypeError(
                f"{self.name} must be of type {self.field_type.__name__}"
            )
        # End: field type validation

        instance.__dict__[
            self.name] = value  # A dictionary or other mapping object used to store an object's (writable) attributes.

    def __delete__(self, instance):
        pass


class IntField(Field):
    field_type = int
    sql_type = "INTEGER"

    def __init__(self, primary_key=False, required=False, default=None):
        super().__init__(required=required, default=default)
        self.primary_key = primary_key


class FloatField(Field):
    field_type = float
    sql_type = "FLOAT"

    # def __init__(self, required=False, default=None):
    #     super().__init__(required=required, default=default)


class CharField(Field):
    field_type = str
    sql_type = "VARCHAR"

    def __init__(self, size, primary_key=False, required=False, default=None):
        super().__init__(required=required, default=default)
        self.primary_key = primary_key
        self.size = size


class BoolField(Field):
    field_type = bool
    sql_type = "BOOLEAN"

    # def __init__(self, required=False, default=None):
    #     super().__init__(required=required, default=default)


class Lightorm:
    pass
