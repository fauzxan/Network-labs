from fastapi import FastAPI, Response
from typing import Optional 
import redis



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

    return "Host is up and running"


@app.get("/students/{student_id}")
def get_student(response: Response, student_id: Optional[str] = None):
    global students
    if students:
        response.status_code = 200
        if not student_id:
            return students
        if student_id == "all":
            return students
        for student in students:
            if "id" in student and student["id"] == student_id:
                return student
        return "No such student id"
    else:
        return "Students are empty"