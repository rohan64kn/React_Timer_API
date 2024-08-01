from fastapi import APIRouter
from config.db import conn
from model import users
user = APIRouter

@user.get("/{username}")
async def read_data(username: str):
    return conn.execute(users.select().where(users.c.username == username)).fetchall()

@user.post("/")
async def write_data(user: user):
    conn.execute(users.insert().values(
        username = user.username,
        password = user.password
    )).fetchall()
    return conn.execute(users.select()).fetchall()
