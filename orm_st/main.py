# Metaclass used so the object class can discover its own attributes (fields)
# Not really necessary for a light ORM per se, but it offers scalability
class ModelMeta(type):
    def __new__(mcls, name, bases, attrs):
        fields = {}

        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key]=value
        cls = super().__new__(mcls, name, bases, attrs)
        cls.__fields__ = fields

        return cls

# Model class will be an ORM operations provider get_by_id, get_all, delete, save, etc...
class Model(metaclass=ModelMeta):

    # Should allow us to create an object instance
    def __init__(self, **kwargs):
        pass

    #CRUD methods

    #CREATE: insert a new record
    def create(self):
        pass
    #READ: get by id, get all, get by value in field, get containing...
    def get_by_id(self, record_id):
        pass

    def get_all(self):
        pass

    def get_by_field(self, record_field, value):
        pass

    def get_all_matching(self, value):
        pass
    #UPDATE: ...
    def update(self, **kwargs):
        pass
    #DELETE: ...
    def delete(self):
        pass
    pass

class Field:
    field_type = None
    sql_type = None

    def __init__(self, required=False, default=None, column = None):
        self.required = required
        self.default = default
        self.column = column

    def __set_name__(self, owner, name):
        self.name = name
        if self.column is None:     #Separating database name from class name
            self.column = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__.__get__(self.name)

    def __set__(self, instance, value):
        # Check if accepts nullable (None -> required)
        if value is None and self.required:
            raise TypeError(f"Field is required. <{self.name}> cannot be None")

        # Field type validation -> Python side
        if not isinstance(value, self.field_type):
            raise TypeError(
                f"{self.name} must be of type {self.field_type.__name__}"
            )
        # End: field type validation

        # A dictionary or other mapping object used to store an object's (writable) attributes.
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        pass


class IntField(Field):
    field_type = int
    sql_type = "INTEGER"

    def __init__(self, primary_key=False, required=False, default=None):
        super().__init__(required=required, default=default, column = None)
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
        super().__init__(required=required, default=default, column = None)
        self.primary_key = primary_key
        self.size = size


class BoolField(Field):
    field_type = bool
    sql_type = "BOOLEAN"

    # def __init__(self, required=False, default=None):
    #     super().__init__(required=required, default=default)


