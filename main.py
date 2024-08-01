#react/main.py
from fastapi import FastAPI
import uvicorn
import sqlite3
from datetime import datetime
import jwt #pip install pyjwt https://pypi.org/project/PyJWT/
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
 
SECRET_KEY = "cairocoders123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800
now = datetime.now()
dummy_user = {
    "username": "Rohan",
    "password": "Rohan@123",
}
print(type(dummy_user))
 
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET, POST, OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origins= origins)
 
class Loginclass(BaseModel):
    username: str
    password: str
@app.get("/")
def read_root():
    print('Hello : World')
    
async def load_data():
    print('Load data')

# @app.on_event("shutdown")
@app.options("/")
def read_options():
    return {"detail":"Method Not Allowed"}

@app.options("/login")
def read_options2():
    return 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await load_data()
    print('Hello')
    SQL = "SELECT username,password from Credentials"
    conn = sqlite3.connect('userlogs.db',check_same_thread=False)
    cursor = conn.cursor()
    cursor = cursor.execute(SQL)
    details = cursor.fetchall()
    lst = details
    print(lst)

    yield
    await shutdown_event()
    print('Hello 2')
    

app = FastAPI(lifespan=lifespan)


# @app.on_event("shutdown")
async def shutdown_event():
    SQL = "INSERT INTO 'Machine_Offtimes'(machineofftime) Values('{}')".format(now)
    conn = sqlite3.connect('userlogs.db',check_same_thread=False)
    cursor = conn.cursor()
    cursor = cursor.execute(SQL)
    conn.commit()
    conn.close()

@app.post("/login")
async def login_user(login_item: Loginclass):
    data = jsonable_encoder(login_item)
    SQL = "SELECT username,password from Credentials"
    conn = sqlite3.connect('userlogs.db',check_same_thread=False)
    cursor = conn.cursor()
    cursor = cursor.execute(SQL)
    details = cursor.fetchall()
    print(details)
    if dummy_user['username'] == data['username'] and dummy_user['password'] == data['password']:
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        conn = sqlite3.connect('userlogs.db',check_same_thread=False)
        # print("Current system time:", formatted_time)
        cursor = conn.cursor()
        SQL = "SELECT machineontime from Machine_Uptimes order by machineontime desc limit 1"
        cursor = cursor.execute(SQL)
        # now = datetime.now()
        ontime = cursor.fetchall()
        print(ontime)
        len_ontime = 0
        if ontime != []:
            print('Hello')
            ontime = ''.join(ontime[0])
            len_ontime = len(ontime)
            ontime = datetime.strptime(ontime, '%Y-%m-%d %H:%M:%S.%f')
        SQL2 = "SELECT machineofftime from Machine_Offtimes order by machineofftime desc limit 1"
        cursor = cursor.execute(SQL2)
        offtime = cursor.fetchall()
        if offtime != []:
            offtime = ''.join(offtime[0])
            offtime = datetime.strptime(offtime, '%Y-%m-%d %H:%M:%S.%f')
        # print(ontime)
        # print(offtime)
        print(ontime<offtime)
        if len_ontime == 0  or (ontime<offtime):
            print('Hello2')
            SQL2 = "INSERT INTO Machine_Uptimes(machineontime) Values('{}')".format(now)
            cursor = cursor.execute(SQL2)  
        else:
            SQL3 = "INSERT INTO User_Logs(username, logintime) Values('{}', '{}')".format(data['username'], now)
            cursor = cursor.execute(SQL3)
        conn.commit()
        conn.close()
        return {'token': encoded_jwt} 
        #  'uptime': now
    else:
        return {'message': 'Login failed'}
    
@app.get("/profile")
def time_left():
    conn = sqlite3.connect('userlogs.db',check_same_thread=False)
    # now = datetime.now()
    cursor = conn.cursor()
    SQL = "SELECT machineontime from Machine_Uptimes order by machineontime desc limit 1" 
    cursor = cursor.execute(SQL)
    lst = cursor.fetchall()
    # x = now.split(' ')
    # result1 = x[1]
    x = now.time()
    x= x.strftime("%H:%M:%S")
    z = ''.join(lst[0])
    z = z.split(' ')
    z = z[1].split('.')
    z = z[0]
    x =datetime.strptime(x,"%H:%M:%S")
    z =datetime.strptime(z,"%H:%M:%S")
    result = (x-z).total_seconds()
    result = result % 10800
    uptime = 10800 - result
    print(uptime)
    conn.commit()
    conn.close()
    return {'uptime': uptime}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)