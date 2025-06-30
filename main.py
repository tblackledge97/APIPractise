
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Path, Query, Body, Request, Form, Cookie
from typing import List
from pydantic import BaseModel, Field
import uvicorn
import shutil
import datetime


app = FastAPI()


templates = Jinja2Templates(directory="templates")


class Student(BaseModel):
    id: int
    name: str = Field(None, title="The description of the item", max_length=10)
    subjects: List[str] = []


class User(BaseModel):
    username: str
    password: str

# path operation
# Returns a JSON response 
@app.get("/")
async def index():
    return {"message": "Hello World"}



@app.post("/student/{college}")
async def student_data(college: str, age:int, student: Student):
    retval = {"college": college, "age": age, **student.model_dump()}
    return retval


@app.get("/hello/", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse("hello.html", {"request": request})


@app.post("/submit/", response_model=User)
async def submit(nm: str = Form(...), pwd: str = Form(...)):
    return User(username=nm, password=pwd)


@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
    return templates.TemplateResponse("uploadfile.html", {"request": request})

@app.post("/cookie/")
def create_cookie():
    content = {"message": "cookie set"}
    response = JSONResponse(content=content)
    response.set_cookie(key="username", value="admin")
    return response


@app.get("/readcookie/")
async def read_cookie(username: str = Cookie(None)):
    return {"username": username}


@app.on_event("startup")
async def startup_event():
    print('Server started: ', datetime.datetime.now())

@app.on_event("shutdown")
async def shutdown_event():
    print('Server shutdown: ', datetime.datetime.now())
