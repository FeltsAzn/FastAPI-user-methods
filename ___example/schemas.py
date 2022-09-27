from pydantic import BaseModel, validator, Field


class Worker(BaseModel):
    first_name: str
    last_name: str
    age: int
    job_title: str
    department: str
    salary: float

    @validator('age') #Валидатор данных
    def check_age(cls, v):
        if v < 18:
            raise ValueError("Возраст работника должен быть больше 18!")
        return v


class Superiors(BaseModel):
    first_name: str
    last_name: str
    age: int = Field(..., gt=25, lt=65,
                     description='Возраст начальника должен быть больше 25 и меньше 65')
    job_title: str
    department: str
    salary: float


class Clients(BaseModel):
    first_name: str
    last_name: str
    age: int = 18
    order_count: int = 0
    amount: float = 0.0


class ClientOut(Clients):
    id: int