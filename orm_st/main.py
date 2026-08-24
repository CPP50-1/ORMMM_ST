class Field:
    sql_type = None

    def __init__(self, field_type, *, column = None, primary_key = False, required=False, default=None):
        self.field_type = field_type
        self.column = column
        self.primary_key = primary_key
        self.required = required
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name
        if self.column is None:     #Separating database name from class name
            self.column = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            return self.default
        return instance.__dict__[self.name]


    def __set__(self, instance, value):
        self._validate(value)       #New data validation method

        old_value = instance.__dict__.get(
            self.name,
            self.default,
        )

        instance.__dict__[self.name] = value

        if old_value != value:
            instance._state.mark_dirty(self.name)       #Usage of state instances

    #Required and right type validation
    def _validate(self, value):
        if value is None:
            if self.required:
                raise TypeError(f"Field {self.name} is required!")
            return
        if not isinstance(value, self.field_type):
            raise TypeError(f"Field {self.name} must be of type {self.field_type.__name__}!")


    def __delete__(self, instance):
        pass

# Metaclass used so the object class can discover its own attributes (fields)
# Not really necessary for a light ORM per se, but it offers scalability
class ModelMeta(type):
    def __new__(mcls, name, bases, attrs):
        fields = {}

        for base in bases:
            fields.update(
                getattr(base, "__fields__", {})
            )

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

        self._state = ModelState()  #This wil instantiate a new ModelState fore very Model instance

        for field_name, field in self.__fields__.items():
            if field_name in kwargs:
                setattr(self, field_name, kwargs[field_name]) #setattr() lets Field descriptor do validation and stuff
            elif field.default is not None:
                setattr(self, field_name, field.default)

    #This method will simulate the database success on saving the object
    def mark_persisted(self):
        values = {}

        for field_name in self.__fields__:
            values[field_name] = getattr(self, field_name)

        self._state.mark_persisted(values)


    # CRUD methods
    # When interacting with table/Model
    #         User
    #          │
    #   ┌──────┼──────┐
    #   │      │      │
    # create  get  filter

    #CREATE: insert a new record
    #Is a class method because this operation does not require an instance of the object
    @classmethod
    def create(cls, **kwargs):
        pass
    #READ: get by id, get all, get by value in field, get containing...
    #Is a class method because this operation does not require an instance of the object

    @classmethod
    def get_by_id(cls, record_id):
        pass

    #Is a class method because this operation does not require an instance of the object
    @classmethod
    def get_all(cls):
        pass

    #Is a class method because this operation does not require an instance of the object
    @classmethod
    def get_by_field(cls, record_field, value):
        pass

    #Is a class method because this operation does not require an instance of the object
    @classmethod
    def get_all_matching(cls, value):
        pass

    #Is a class method because this operation does not require an instance of the object
    @classmethod
    def get(cls, **kwargs):
        pass

    # When interacting with a specific database row : Update/Delete
    #UPDATE: ...
    #This method acts on a specific instance
    def update(self, **kwargs):
        pass

    #DELETE: ...
    #This method acts on a specific instance
    def delete(self):
        pass


#ModelState class : will keep trace of the database-state related of a model instance
class ModelState:

    def __init__(self):
        self.persisted = False
        self.original_values = {}
        self.dirty_fields = set()


    def mark_dirty(self, field_name):
        self.dirty_fields.add(field_name)


    def mark_persisted(self, values):
        self.persisted = True
        self.original_values = values.copy()
        self.dirty_fields.clear()

    def mark_deleted(self):
        self.persisted = False


#This class allows incorporate metadata onf Field properties on a class


class IntField(Field):
    sql_type = "INTEGER"

    def __init__(self, primary_key=False, required=False, default=None):
        super().__init__(required=required, default=default, column = None)
        self.primary_key = primary_key


class FloatField(Field):
    sql_type = "FLOAT"

    # def __init__(self, required=False, default=None):
    #     super().__init__(required=required, default=default)


class CharField(Field):
    sql_type = "VARCHAR"

    def __init__(self, size, primary_key=False, required=False, default=None):
        super().__init__(required=required, default=default, column = None)
        self.primary_key = primary_key
        self.size = size


class BoolField(Field):
    sql_type = "BOOLEAN"

    # def __init__(self, required=False, default=None):
    #     super().__init__(required=required, default=default)


