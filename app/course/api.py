from ninja import Query
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from typing import List, Optional
from ninja_extra import NinjaExtraAPI
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# Modellar import qilinadi
from .models import Course, Bob, Lesson

# Schemalar import qilinadi
from .schemes import (
    CourseSchema,
    BobSchema, BobDetailSchema, LessonSchema
)

api = NinjaExtraAPI()

# JWT autentifikatsiyasini ro'yxatdan o'tkazish
api.register_controllers(NinjaJWTDefaultController)


# --- Kurslar bo'yicha endpointlar ---
class LessonSchema(BaseModel):
    id: int
    title: str
    body: str
    estimated_reading_time: int
    pdf_url: Optional[str]=None # O'zgargan nom
    is_active: bool
    created_at: datetime
    updated_at: datetime


class BobDetailSchema(BaseModel):
    id: int
    title: str
    lessons: List[LessonSchema]
class CourseDetailSchema(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    image: str
    bobs: List[BobDetailSchema]
"""
class CourseSchema(Schema):
    id: int
    title: str
    slug: str
    body: str
    image: str
    created_at: datetime
    updated_at: datetime
"""
@api.get("/courses/", response=List[CourseSchema])
def list_courses(request):
    return [
        {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "body": course.body,
            "image": request.build_absolute_uri(course.image.url) if course.image else None,
            "created_at": course.created_at,
            "updated_at": course.updated_at
        }
        for course in Course.objects.filter(is_active=True).order_by('-created_at')
    ]

@api.get("/courses/{course_id}/", response=CourseSchema)
def get_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    return {
        "id": course.id,
        "title": course.title,
        "slug": course.slug,
        "body": course.body,
        "image": request.build_absolute_uri(course.image.url) if course.image else None,
        "created_at": course.created_at,
        "updated_at": course.updated_at
    }

@api.get("/courses/{course_id}/bobs/", response=List[BobSchema])
def get_course_bobs(request, course_id: int):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    bobs = course.bobs.filter(is_active=True).annotate(
        lesson_count=Count('lessons', filter=Q(lessons__is_active=True))
    ).order_by('order')
    return bobs


class LessonSchema(BaseModel):
    id: int
    title: str
    body: str
    estimated_reading_time: int
    pdf_url: Optional[str]=None # O'zgargan nom
    is_active: bool
    created_at: datetime
    updated_at: datetime

class BobDetailSchema(BaseModel):
    id: int
    title: str
    lessons: List[LessonSchema]

class CourseDetailSchema(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    image: str
    bobs: List[BobDetailSchema]

@api.get("/courses/{course_id}/detail/", response=CourseDetailSchema)
def get_course_detail(request, course_id: int):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    return {
        "id": course.id,
        "title": course.title,
        "slug": course.slug,
        "body": course.body,
        "image": request.build_absolute_uri(course.image.url) if course.image else None,
        "bobs": [
            {
                "id": bob.id,
                "title": bob.title,
                "lessons": [
                    {
                        "id": lesson.id,
                        "title": lesson.title,
                        "body": lesson.body,
                        "estimated_reading_time": lesson.estimated_reading_time,
                        "pdf_url": request.build_absolute_uri(lesson.pdf_fayl.url) if lesson.pdf_fayl else None, # O'zgargan qator
                        "is_active": lesson.is_active,
                        "created_at": lesson.created_at,
                        "updated_at": lesson.updated_at
                    }
                    for lesson in bob.lessons.filter(is_active=True).order_by('order')
                ]
            }
            for bob in course.bobs.filter(is_active=True).order_by('order')
        ]
    }

@api.get("/bobs/{bob_id}/", response=BobDetailSchema)
def get_bob_detail(request, bob_id: int):
    bob = get_object_or_404(Bob, id=bob_id, is_active=True)
    lessons = bob.lessons.filter(is_active=True).order_by('order')
    return {
        "id": bob.id,
        "title": bob.title,
        "lessons": [
            {
                "id": lesson.id,
                "title": lesson.title,
                "body": lesson.body,
                "estimated_reading_time": lesson.estimated_reading_time,
                "pdf_url": request.build_absolute_uri(lesson.pdf_fayl.url) if lesson.pdf_fayl else None, # O'zgargan qator
                "is_active": lesson.is_active,
                "created_at": lesson.created_at,
                "updated_at": lesson.updated_at
            }
            for lesson in lessons
        ]
    }

# --- Darslar bo'yicha endpointlar ---
def absolutify_images(request, body):
    return body.replace("src=\"/", f"src=\"{request.build_absolute_uri('/')}")

@api.get("/lessons/{lesson_id}/", response=LessonSchema)
def get_lesson(request, lesson_id: int):
    lesson = get_object_or_404(Lesson, id=lesson_id, is_active=True)

    pdf_url = None
    if lesson.pdf_fayl and hasattr(lesson.pdf_fayl, 'url'):
        pdf_url = request.build_absolute_uri(lesson.pdf_fayl.url)

    return {
        "id": lesson.id,
        "title": lesson.title,
        "body": absolutify_images(request, lesson.body),
        "estimated_reading_time": lesson.estimated_reading_time,
        "pdf_url": pdf_url, # Bu yerda .url atributini ishlating va absolutify_images kabi absolutify qiling
        "is_active": lesson.is_active,
        "created_at": lesson.created_at,
        "updated_at": lesson.updated_at
    }

@api.get("/search/", response=List[CourseSchema])
def search(request, q: str = Query(..., min_length=2)):
    """
    Kurslar, boblar va darslar bo'yicha qidiruvni amalga oshiradi.
    `q` parametri orqali qidiruv so'rovini qabul qiladi.
    """
    # Faqat faol elementlarni qidirish
    courses = Course.objects.filter(
        Q(title__icontains=q) | Q(body__icontains=q),
        is_active=True
    ).order_by('-created_at')[:5] # Eng ko'pi 5 ta kurs

    bobs = Bob.objects.filter(
        Q(title__icontains=q),
        is_active=True,
        course__is_active=True # Faqat faol kurslarga tegishli boblar
    ).order_by('order')[:10] # Eng ko'pi 10 ta bob

    lessons = Lesson.objects.filter(
        Q(title__icontains=q) | Q(body__icontains=q),
        is_active=True,
        bob__is_active=True, # Faqat faol boblarga tegishli darslar
        bob__course__is_active=True # Faqat faol kurslarga tegishli darslar
    ).order_by('order')[:10] # Eng ko'pi 10 ta dars

    return {
        "courses": [{"id": c.id, "title": c.title, "type": "course"} for c in courses],
        "bobs": [{"id": b.id, "title": b.title, "course_id": b.course.id, "type": "bob"} for b in bobs],
        "lessons": [{"id": l.id, "title": l.title, "bob_id": l.bob.id, "type": "lesson"} for l in lessons]
    }