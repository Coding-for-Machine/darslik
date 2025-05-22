from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from course.models import Course, Bob, Lesson

class Command(BaseCommand):
    help = 'Create sample course data'

    def handle(self, *args, **kwargs):
        # Create sample course
        course, created = Course.objects.get_or_create(
            title="Python Dasturlash Asoslari",
            defaults={
                'body': "Python dasturlash tilini o'rganish uchun to'liq kurs",
                'slug': 'python-dasturlash-asoslari'
            }
        )
        
        if created:
            self.stdout.write(f'Course created: {course.title}')
        
        # Create sample bobs
        bob_titles = [
            "Python ga kirish",
            "O'zgaruvchilar va ma'lumot turlari", 
            "Operatorlar",
            "Shart operatorlari",
            "Tsikllar"
        ]
        
        for i, title in enumerate(bob_titles, 1):
            bob, created = Bob.objects.get_or_create(
                course=course,
                title=title,
                defaults={'order': i}
            )
            
            if created:
                self.stdout.write(f'Bob created: {bob.title}')
                
                # Create sample lessons for each bob
                for j in range(1, 4):  # 3 lessons per bob
                    lesson_content = f"""
                    <h2>{title} - Dars {j}</h2>
                    <p>Bu {title.lower()} bo'yicha {j}-darsdir.</p>
                    <p>Bu darsda siz quyidagilarni o'rganasiz:</p>
                    <ul>
                        <li>Asosiy tushunchalar</li>
                        <li>Amaliy misollar</li>
                        <li>Mashqlar</li>
                    </ul>
                    <p>Dars oxirida siz bu mavzuni to'liq tushungan bo'lasiz.</p>
                    """
                    
                    Lesson.objects.get_or_create(
                        bob=bob,
                        order=j,
                        defaults={
                            'title': f'{title} - Dars {j}',
                            'body': lesson_content,
                            'estimated_reading_time': 5 + j
                        }
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )