import datetime

from orm_st.main import Model, Field, IntField


class TestEntity(Model):
    #name = Field() -> without type validation (deprecated)
    id = Field(int, primary_key=True,required=True)
    name = Field(str)
    last_name = Field(str)
    birth_date = Field(datetime.date)

    def __str__(self):
        return f"{self.name}, {self.last_name} {self.birth_date}"


test1 = TestEntity(
    id = 1,
    name = "John",
    last_name = "Connor",
    birth_date = datetime.date(1985, 2, 28),
)

test2 = TestEntity(
    id = 2,
    name = "Sarah",
    last_name = "Connor",
    birth_date = datetime.date(1965, 8, 30),#"1965-08-30",
)

try:
    print(test1._state.persisted)
    #print(test2)
except TypeError:
    print ("TypeError")

