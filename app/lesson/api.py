from ninja import Router
from .models import Lessons
from ninja.schema import Schema
from datetime import datetime
from typing import List
lesson_router = Router()

class LessonsSchema(Schema):
    id: int
    body: str
    created_at: datetime
    updated_at: datetime

def absolutify_images(request, body):
    return body.replace("src=\"/", f"src=\"{request.build_absolute_uri('/')}")

@lesson_router.get("/", response=List[LessonsSchema])
def get_lessons(request):
    lessons = Lessons.objects.all()
    return [
        {
            "id": lesson.id,
            "body": absolutify_images(request, lesson.body),
            "created_at": lesson.created_at,
            "updated_at": lesson.updated_at,
        }
        for lesson in lessons
    ]

@lesson_router.get("/{lesson_id}", response=LessonsSchema)
def get_lesson(request, lesson_id: int):
    lesson = Lessons.objects.get(id=lesson_id)
    return {
        "id": lesson.id,
        "body": absolutify_images(request, lesson.body),
        "created_at": lesson.created_at,
        "updated_at": lesson.updated_at,
    }
