from fastapi import FastAPI
from manager import *
app = FastAPI()

@app.get("/users/{user}")
def users(user: str):
    output_user_info_file(user)

@app.get("/friends/{user}")
def friends(user: str):
    output_friends_file(user)
