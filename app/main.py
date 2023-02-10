from fastapi import FastAPI, Response
from typing import Optional 

app = FastAPI()

students = [
    {
        "name": "Alice",
        "id": "1004803",
    },
    {
        "name": "Bob",
        "id": "1004529"
    },
    {
        "name": "Charlie",
        "id": "1004910",
        "gpa": 5.0
    },
    {
        "name": "Someone random",
        "gpa": 5.0
    }
]

@app.get("/")
def read_root():
    return "Hello World"



@app.get("/students/{student_id}")
def find_student(student_id: Optional[str], response: Response):
    global students
    for student in students:
        if "id" in student:
            if student["id"] == student_id:
                response.status_code = 200
                return student
        else:
            "One of them didn't have id"
    response.status_code = 404
    return "Not found lor"
