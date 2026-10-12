from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Student Managemnt API",
    description="crud api",
    version="1.0.0"
)

class StudentCreate(BaseModel):
    name:str
    age:int
    email:str

class StudentUpdate(BaseModel):
    name:str | None = None
    age:int | None = None
    email:str | None = None

students = {}
next_student_id = 1

@app.post("/students",status_code=201)
def create_student(student:StudentCreate):
    global next_student_id
    student_id = next_student_id
    next_student_id += 1
    student_data = student.model_dump()
    student_data["id"]= student_id
    students[student_id]= student_data
    return student_data

@app.get("/students")
def get_all_students():
    return list(students.values())

@app.get("/students/{student_id}")
def get_one_students(student_id:int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return students[student_id]


@app.patch("/students/{student_id}")
def update_students(
    student_id:int,
    studentUpdate:StudentUpdate
    ):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    update_data = studentUpdate.model_dump(exclude_unset=True)
    students[student_id].update(update_data)
    return students[student_id]

@app.get("/")
def home():
    return{
        "message":"Welcome to SM API"
    }

@app.delete("/students/{student_id}")
def delete_stu(student_id:int):
    del students[student_id]
    return {
        "message":"Student is deleted"
    }