from ninja import NinjaAPI, Schema
from datetime import datetime
from typing import List, Optional
from .models import Course, Bob

api = NinjaAPI()

# === SCHEMAS ===
class CourseSchema(Schema):
    id: int
    title: str
    slug: str
    body: str
    image: Optional[str]
    created_at: datetime
    updated_at: datetime

class BobSchema(Schema):
    id: int
    title: str

# === ENDPOINTS ===

@api.get("/courses", response=List[CourseSchema])
def get_courses(request):
    courses = Course.objects.all()
    return [
        {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "body": course.body,
            "image": request.build_absolute_uri(course.image.url) if course.image else None,
            "created_at": course.created_at,
            "updated_at": course.updated_at,
        }
        for course in courses
    ]


@api.get("/courses/{course_id}", response={200: CourseSchema, 404: dict})
def get_course(request, course_id: int):
    try:
        course = Course.objects.get(id=course_id)
        return 200, {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "body": course.body,
            "image": request.build_absolute_uri(course.image.url) if course.image else None,
            "created_at": course.created_at,
            "updated_at": course.updated_at,
        }
    except Course.DoesNotExist:
        return 404, {"error": "Course not found"}


@api.get("/courses/{course_id}/bobs", response=List[BobSchema])
def get_course_bobs(request, course_id: int):
    try:
        course = Course.objects.get(id=course_id)
        bobs = course.bob.all()  # related_name='bob'
        return [
            {
                "id": bob.id,
                "title": bob.title,
            }
            for bob in bobs
        ]
    except Course.DoesNotExist:
        return []


@api.get("/bobs/{bob_id}", response={200: BobSchema, 404: dict})
def get_bob(request, bob_id: int):
    try:
        bob = Bob.objects.get(id=bob_id)
        return 200, {
            "id": bob.id,
            "title": bob.title,
        }
    except Bob.DoesNotExist:
        return 404, {"error": "Bob not found"}

