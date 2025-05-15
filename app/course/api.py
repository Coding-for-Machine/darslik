from ninja import NinjaAPI
from pydantic import BaseModel
from datetime import datetime

api = NinjaAPI(
    title="Course API",
    version="1.0.0",
    description="API for the Course app",
    urls_namespace="course",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    schema_generator_options={
        "title": "Course API",
        "version": "1.0.0",
        "description": "API for the Course app",
        "urls_namespace": "course",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json",
    },
)

class Course(BaseModel):
    id: int
    title: str
    description: str
    image: str
    created_at: datetime
    updated_at: datetime

class Bob(BaseModel):
    id: int
    title: str
    description: str
    image: str
    created_at: datetime
    updated_at: datetime


@api.get("/courses", response=list[Course])
def get_courses(request):
    return {"courses": "courses"}

@api.get("/courses/{course_id}", response=Course)
def get_course(request, course_id: int):
    return {"course": "course"}

@api.get("/courses/{course_id}/bobs", response=list[Bob])
def get_course_bobs(request, course_id: int):
    return {"bobs": "bobs"}

@api.get("/bobs/{bob_id}", response=Bob)
def get_bob(request, bob_id: int):
    return {"bob": "bob"}


