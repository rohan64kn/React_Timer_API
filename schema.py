from pydantic import BaseModel

class Credentials(BaseModel):
    Username: str
    Password: int


class Machine_Offtimes(BaseModel):
    machineofftime: int

class Machine_Uptimes(BaseModel):
    machineontime: int

class User_Logs(BaseModel):
    username: str
    logintime: int