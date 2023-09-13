from fastapi import FastAPI
from manager import *
app = FastAPI()

@app.get("/users/{user}")
def hello(user: str):
    output_user_info_file(user)
