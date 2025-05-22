from ninja import Query
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from typing import List, Optional
from ninja_extra import NinjaExtraAPI

# Modellar import qilinadi
from .models import Course, Bob, Lesson, UserProgress, Bookmark, Note

# Schemalar import qilinadi
from .schemes import (
    UserCreateSchema, UserSchema, CourseSchema, CourseDetailSchema,
    BobSchema, BobDetailSchema, LessonSchema, ProgressUpdateSchema,
    BookmarkSchema, NoteCreateSchema, NoteUpdateSchema, NoteResponseSchema
)

api = NinjaExtraAPI()

# JWT autentifikatsiyasini ro'yxatdan o'tkazish
api.register_controllers(NinjaJWTDefaultController)

@api.post("/auth/register", response=UserSchema)
def register(request, data: UserCreateSchema):
    """
    Foydalanuvchini ro'yxatdan o'tkazish.
    Yangi foydalanuvchi yaratadi va uning ma'lumotlarini qaytaradi.
    """
    if User.objects.filter(username=data.username).exists():
        return api.create_response(request, {"error": "Username already exists"}, status=400)

    if User.objects.filter(email=data.email).exists():
        return api.create_response(request, {"error": "Email already exists"}, status=400)

    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name
    )
    return user

# --- Kurslar bo'yicha endpointlar ---

@api.get("/courses", response=List[CourseSchema], auth=JWTAuth())
def list_courses(request):
    """
    Barcha faol kurslar ro'yxatini qaytaradi.
    Agar autentifikatsiya bo'lsa, foydalanuvchi progress ma'lumotlarini ham qo'shadi.
    """
    courses = Course.objects.filter(is_active=True).order_by('-created_at')
    
    # Har bir kurs uchun foydalanuvchi progressini hisoblash
    for course in courses:
        completed_lessons = UserProgress.objects.filter(
                user=request.user,
                lesson__bob__course=course,
                is_completed=True
            ).count()
        course.completed_lessons = completed_lessons
        # total_lessons Course modelidagi @property orqali olinadi
        course.progress_percentage = (completed_lessons / course.total_lessons * 100) if course.total_lessons > 0 else 0

    return courses

@api.get("/courses/{course_id}", response=CourseSchema, auth=JWTAuth())
def get_course(request, course_id: int):
    """
    Berilgan ID bo'yicha bitta kurs ma'lumotlarini qaytaradi.
    Agar autentifikatsiya bo'lsa, foydalanuvchi progress ma'lumotlarini ham qo'shadi.
    """
    course = get_object_or_404(Course, id=course_id, is_active=True)

    # Kurs uchun foydalanuvchi progressini hisoblash
    completed_lessons = UserProgress.objects.filter(
            user=request.user,
            lesson__bob__course=course,
            is_completed=True
        ).count()
    course.completed_lessons = completed_lessons
    course.progress_percentage = (completed_lessons / course.total_lessons * 100) if course.total_lessons > 0 else 0

    return course

@api.get("/courses/{course_id}/bobs", response=List[BobSchema], auth=JWTAuth())
def get_course_bobs(request, course_id: int):
    """
    Berilgan kursga tegishli barcha faol boblar ro'yxatini qaytaradi.
    Har bir bob uchun darslar sonini ham hisoblaydi.
    """
    course = get_object_or_404(Course, id=course_id, is_active=True)
    # 'bobs' related_name orqali kursga bog'langan boblarni olamiz
    bobs = course.bobs.filter(is_active=True).annotate(
        lesson_count=Count('lessons', filter=Q(lessons__is_active=True))
    ).order_by('order')
    return bobs

@api.get("/courses/{course_id}/detail", response=CourseDetailSchema, auth=JWTAuth())
def get_course_detail(request, course_id: int):
    """
    Kursning to'liq ma'lumotlarini, shu jumladan uning boblarini qaytaradi.
    Agar autentifikatsiya bo'lsa, foydalanuvchi progress ma'lumotlarini ham qo'shadi.
    """
    course = get_object_or_404(Course, id=course_id, is_active=True)

    bobs = course.bobs.filter(is_active=True).annotate(
        lesson_count=Count('lessons', filter=Q(lessons__is_active=True))
    ).order_by('order')

    # Kurs uchun foydalanuvchi progressini hisoblash
    completed_lessons = UserProgress.objects.filter(
            user=request.user,
            lesson__bob__course=course,
            is_completed=True
        ).count()
    course.completed_lessons = completed_lessons
    course.progress_percentage = (completed_lessons / course.total_lessons * 100) if course.total_lessons > 0 else 0

    # Boblarni kurs ob'ektiga List[BobSchema] formatida biriktiramiz
    course.bobs = list(bobs)
    return course

# --- Boblar bo'yicha endpointlar ---

@api.get("/bobs/{bob_id}", response=BobDetailSchema, auth=JWTAuth())
def get_bob_detail(request, bob_id: int):
    """
    Berilgan ID bo'yicha bob va uning barcha faol darslarini qaytaradi.
    Agar autentifikatsiya bo'lsa, har bir dars uchun foydalanuvchi progressi,
    xatcho'p va eslatma holatini ham qo'shadi.
    """
    bob = get_object_or_404(Bob, id=bob_id, is_active=True)
    # 'lessons' related_name orqali bobga bog'langan darslarni olamiz
    lessons = bob.lessons.filter(is_active=True).order_by('order')

    # Har bir dars uchun foydalanuvchi progressi, xatcho'p va eslatma holatini tekshirish
    for lesson in lessons:
        lesson.is_completed = UserProgress.objects.filter(
            user=request.user,
            lesson=lesson,
            is_completed=True
        ).exists()

        lesson.has_bookmark = Bookmark.objects.filter(
            user=request.user,
            lesson=lesson
        ).exists()

        lesson.has_note = Note.objects.filter(
            user=request.user,
            lesson=lesson
        ).exists()  

    # Darslarni bob ob'ektiga List[LessonSchema] formatida biriktiramiz
    bob.lessons = list(lessons)
    return bob

# --- Darslar bo'yicha endpointlar ---

@api.get("/lessons/{lesson_id}", response=LessonSchema, auth=JWTAuth())
def get_lesson(request, lesson_id: int):
    """
    Berilgan ID bo'yicha bitta dars ma'lumotlarini qaytaradi.
    Agar autentifikatsiya bo'lsa, foydalanuvchi progressi, xatcho'p va eslatma holatini ham qo'shadi.
    """
    lesson = get_object_or_404(Lesson, id=lesson_id, is_active=True)

    # Dars uchun foydalanuvchi progressi, xatcho'p va eslatma holatini tekshirish
    lesson.is_completed = UserProgress.objects.filter(
        user=request.user,
        lesson=lesson,
        is_completed=True
    ).exists()

    lesson.has_bookmark = Bookmark.objects.filter(
        user=request.user,
        lesson=lesson
    ).exists()

    lesson.has_note = Note.objects.filter(
        user=request.user,
        lesson=lesson
    ).exists()

    return lesson

# --- Progress bo'yicha endpointlar ---

@api.post("/progress/update", auth=JWTAuth())
def update_progress(request, data: ProgressUpdateSchema):
    """
    Foydalanuvchining darsdagi jarayonini yangilash.
    Darsning yakunlanganligini va sarflangan vaqtni saqlaydi.
    """
    lesson = get_object_or_404(Lesson, id=data.lesson_id, is_active=True)

    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'time_spent': data.time_spent}
    )

    progress.is_completed = data.is_completed
    # Agar yaratilmagan bo'lsa, mavjud vaqtga qo'shamiz
    if not created:
        progress.time_spent += data.time_spent

    if data.is_completed and not progress.completion_date:
        progress.completion_date = timezone.now()

    progress.save()

    return {"success": True, "message": "Progress updated successfully"}

@api.get("/progress/stats", auth=JWTAuth())
def get_progress_stats(request, course_id: Optional[int] = None):
    """
    Foydalanuvchining umumiy yoki ma'lum bir kurs bo'yicha jarayon statistikasi.
    """
    if course_id:
        course = get_object_or_404(Course, id=course_id, is_active=True)
        total_lessons = course.total_lessons
        completed_lessons = UserProgress.objects.filter(
            user=request.user,
            lesson__bob__course=course,
            is_completed=True
        ).count()
    else:
        # Barcha faol darslarni hisoblash
        total_lessons = Lesson.objects.filter(
            is_active=True,
            bob__is_active=True,
            bob__course__is_active=True
        ).count()
        # Foydalanuvchi tomonidan yakunlangan barcha darslarni hisoblash
        completed_lessons = UserProgress.objects.filter(
            user=request.user,
            is_completed=True
        ).count()

    progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percentage": round(progress_percentage, 2)
    }

# --- Xatcho'plar bo'yicha endpointlar ---

@api.post("/bookmarks/toggle", auth=JWTAuth())
def toggle_bookmark(request, data: BookmarkSchema):
    """
    Darsga xatcho'p qo'shish yoki olib tashlash.
    Agar xatcho'p mavjud bo'lsa, uni o'chiradi; aks holda, yangisini yaratadi.
    """
    lesson = get_object_or_404(Lesson, id=data.lesson_id, is_active=True)

    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    if not created:
        bookmark.delete()
        return {"success": True, "action": "removed", "message": "Bookmark removed successfully"}

    return {"success": True, "action": "added", "message": "Bookmark added successfully"}

@api.get("/bookmarks", auth=JWTAuth(), response=List[LessonSchema])
def get_bookmarks(request):
    """
    Foydalanuvchining barcha xatcho'plarini (darslarini) qaytaradi.
    Har bir dars uchun progress va eslatma holatini ham qo'shadi.
    """
    bookmarks = Bookmark.objects.filter(user=request.auth).select_related('lesson').order_by('-created_at')
    lessons = [bookmark.lesson for bookmark in bookmarks]

    for lesson in lessons:
        lesson.has_bookmark = True # Bu dars xatcho'p ekanligini belgilaymiz
        lesson.is_completed = UserProgress.objects.filter(
            user=request.user,
            lesson=lesson,
            is_completed=True
        ).exists()
        lesson.has_note = Note.objects.filter(
            user=request.user,
            lesson=lesson
        ).exists()

    return lessons

# --- Eslatmalar bo'yicha endpointlar ---

@api.post("/notes", auth=JWTAuth(), response=NoteResponseSchema)
def create_note(request, data: NoteCreateSchema):
    """
    Dars uchun yangi eslatma yaratish yoki mavjudini yangilash.
    """
    lesson = get_object_or_404(Lesson, id=data.lesson_id, is_active=True)

    note, created = Note.objects.update_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'content': data.content}
    )

    return note

@api.get("/notes/{lesson_id}", auth=JWTAuth(), response=Optional[NoteResponseSchema])
def get_note(request, lesson_id: int):
    """
    Berilgan dars uchun foydalanuvchining eslatmasini qaytaradi.
    Agar eslatma topilmasa, None qaytaradi.
    """
    try:
        note = Note.objects.get(user=request.user, lesson_id=lesson_id)
        return note
    except Note.DoesNotExist:
        return None

@api.put("/notes/{note_id}", auth=JWTAuth(), response=NoteResponseSchema)
def update_note(request, note_id: int, data: NoteUpdateSchema):
    """
    Mavjud eslatmani yangilash.
    """
    note = get_object_or_404(Note, id=note_id, user=request.auth)
    note.content = data.content
    note.save()
    return note

@api.delete("/notes/{note_id}", auth=JWTAuth())
def delete_note(request, note_id: int):
    """
    Eslatmani o'chirish.
    """
    note = get_object_or_404(Note, id=note_id, user=request.auth)
    note.delete()
    return {"success": True, "message": "Note deleted successfully"}

@api.get("/notes", auth=JWTAuth(), response=List[NoteResponseSchema])
def get_user_notes(request):
    """
    Foydalanuvchining barcha eslatmalarini qaytaradi.
    """
    notes = Note.objects.filter(user=request.auth).select_related('lesson').order_by('-updated_at')
    return notes

# --- Qidiruv endpointi ---

@api.get("/search")
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