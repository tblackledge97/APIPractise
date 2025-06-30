
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Path, Query, Body, Request
from typing import List
from pydantic import BaseModel, Field




app = FastAPI()

class Student(BaseModel):
    id: int
    name: str = Field(None, title="The description of the item", max_length=10)
    subjects: List[str] = []

templates = Jinja2Templates(directory="templates")

# path operation
# Returns a JSON response 
@app.get("/")
async def index():
    return {"message": "Hello World"}



@app.post("/students/{college}")
async def student_data(college: str, age:int, student: Student):
    retval = {"college": college, "age": age, **student.model_dump()}
    return retval

@app.get("/hello/", response_class=HTMLResponse)
async def hello(request: Request):
   return templates.TemplateResponse("hello.html", {"request": request})