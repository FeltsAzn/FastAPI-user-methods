from fastapi import FastAPI
from app.heandlers import router


app = FastAPI(title='USERS', description='CRUD methods and logining for users', version='0.0.1')
app.include_router(router=router)


