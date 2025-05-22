from ninja import Schema
from typing import List, Optional
from datetime import datetime

# Response Schemas
class LessonSchema(Schema):
    id: int
    title: str
    body: str
    order: int
    estimated_reading_time: int
    is_completed: Optional[bool] = False
    has_bookmark: Optional[bool] = False
    has_note: Optional[bool] = False
    created_at: datetime
    updated_at: datetime

class BobSchema(Schema):
    id: int
    title: str
    order: int
    lesson_count: int
    created_at: datetime
    updated_at: datetime

class BobDetailSchema(Schema):
    id: int
    title: str
    order: int
    lessons: List[LessonSchema]
    created_at: datetime
    updated_at: datetime

class CourseSchema(Schema):
    id: int
    title: str
    slug: str
    body: str
    image: str
    total_lessons: int
    completed_lessons: Optional[int] = 0
    progress_percentage: Optional[float] = 0.0
    created_at: datetime
    updated_at: datetime

class CourseDetailSchema(Schema):
    id: int
    title: str
    slug: str
    body: str
    image: str
    bobs: List[BobSchema]
    total_lessons: int
    completed_lessons: Optional[int] = 0
    progress_percentage: Optional[float] = 0.0
    created_at: datetime
    updated_at: datetime

# Request Schemas
class ProgressUpdateSchema(Schema):
    lesson_id: int
    is_completed: bool
    time_spent: Optional[int] = 0

class BookmarkSchema(Schema):
    lesson_id: int

class NoteCreateSchema(Schema):
    lesson_id: int
    content: str

class NoteUpdateSchema(Schema):
    content: str

class NoteResponseSchema(Schema):
    id: int
    lesson_id: int
    content: str
    created_at: datetime
    updated_at: datetime

# User Schemas
class UserCreateSchema(Schema):
    username: str
    email: str
    password: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""

class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    date_joined: datetime