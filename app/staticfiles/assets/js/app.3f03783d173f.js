// Global o'zgaruvchilar
let currentCourseId = null;
let currentChapterId = null;
let currentLessonId = null;
let currentChapterLessons = [];
let courseStructure = [];

document.addEventListener('DOMContentLoaded', function() {
    // API Base URL
    const API_BASE_URL = 'http://localhost:8000/api'; // O'zgartiring
    
    // DOM Elements
    const loadingSpinner = document.getElementById('loading-spinner');
    const coursesContainer = document.getElementById('courses-container');
    const coursesSection = document.getElementById('courses-section');
    const courseDetailSection = document.getElementById('course-detail-section');
    const chapterDetailSection = document.getElementById('chapter-detail-section');
    const lessonDetailSection = document.getElementById('lesson-detail-section');
    const searchResults = document.getElementById('search-results');
    const searchResultsContent = document.getElementById('search-results-content');
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    
    // Event Listeners
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') performSearch();
    });
    
    // Dasturni ishga tushirish
    loadCourses();
    
    // Funksiyalar
    function showLoading(show) {
        loadingSpinner.classList.toggle('hidden', !show);
    }
    
    async function loadCourses() {
        showLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/courses/`);
            if (!response.ok) throw new Error('Server xatosi');
            
            const courses = await response.json();
            renderCourses(courses);
        } catch (error) {
            console.error('Kurslarni yuklashda xato:', error);
            coursesContainer.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <i class="fas fa-exclamation-triangle text-4xl text-yellow-500 mb-4"></i>
                    <p class="text-xl font-medium mb-2">Kurslarni yuklab bo'lmadi</p>
                    <p class="text-gray-600 mb-4">${error.message}</p>
                    <button onclick="loadCourses()" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                        <i class="fas fa-sync-alt mr-2"></i> Qayta urinish
                    </button>
                </div>
            `;
        } finally {
            showLoading(false);
        }
    }
    
    function renderCourses(courses) {
        coursesContainer.innerHTML = '';
        
        if (courses.length === 0) {
            coursesContainer.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <i class="far fa-folder-open text-4xl text-gray-400 mb-4"></i>
                    <p class="text-xl font-medium">Hozircha kurslar mavjud emas</p>
                </div>
            `;
            return;
        }
        
        courses.forEach(course => {
            const courseCard = document.createElement('div');
            courseCard.className = 'bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-300 transform hover:-translate-y-1';
            courseCard.innerHTML = `
                <div class="relative">
                    <img src="${course.image || 'https://via.placeholder.com/400x225?text=No+Image'}" 
                         alt="${course.title}" 
                         class="w-full h-48 object-cover">
                    <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4">
                        <h3 class="text-white font-bold text-xl">${course.title}</h3>
                    </div>
                </div>
                <div class="p-4">
                    <p class="text-gray-700 mb-4 line-clamp-3">${course.body || 'Tavsif mavjud emas'}</p>
                    <button onclick="showCourseDetail(${course.id})" 
                            class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition">
                        Ko'rish
                    </button>
                </div>
            `;
            coursesContainer.appendChild(courseCard);
        });
    }
    
    async function showCourseDetail(courseId) {
        showLoading(true);
        try {
            // Fetch course details and chapters in parallel
            const [courseResponse, bobsResponse] = await Promise.all([
                fetch(`${API_BASE_URL}/courses/${courseId}/`),
                fetch(`${API_BASE_URL}/courses/${courseId}/bobs/`)
            ]);
            
            if (!courseResponse.ok || !bobsResponse.ok) {
                throw new Error('Ma\'lumotlarni yuklab bo\'lmadi');
            }
            
            const course = await courseResponse.json();
            const bobs = await bobsResponse.json();
            
            // Update current course ID
            currentCourseId = courseId;
            
            // Update UI
            document.getElementById('course-title').textContent = course.title;
            
            const courseImage = document.getElementById('course-image');
            courseImage.src = course.image || 'https://via.placeholder.com/800x450?text=No+Image';
            courseImage.alt = course.title;
            
            document.getElementById('course-description').innerHTML = course.body || '<p class="text-gray-500">Tavsif mavjud emas</p>';
            document.getElementById('course-created').textContent = formatDate(course.created_at);
            document.getElementById('course-updated').textContent = formatDate(course.updated_at);
            
            // Render chapters
            const chaptersContainer = document.getElementById('course-chapters');
            chaptersContainer.innerHTML = '';
            
            if (bobs.length === 0) {
                chaptersContainer.innerHTML = `
                    <div class="text-center py-8 text-gray-500">
                        <i class="far fa-folder-open text-3xl mb-2"></i>
                        <p>Hozircha bo\'limlar mavjud emas</p>
                    </div>
                `;
            } else {
                bobs.forEach(bob => {
                    const chapterCard = document.createElement('div');
                    chapterCard.className = 'bg-white p-4 rounded-lg border border-gray-200 hover:border-green-300 transition';
                    chapterCard.innerHTML = `
                        <div class="flex justify-between items-center">
                            <h3 class="text-lg font-semibold">${bob.title}</h3>
                            <span class="text-sm text-gray-500">${bob.lesson_count || 0} ta dars</span>
                        </div>
                        <button onclick="showChapterDetail(${bob.id})" 
                                class="mt-3 w-full md:w-auto bg-green-100 text-green-700 py-1 px-3 rounded-md text-sm hover:bg-green-200 transition">
                            Ko'rish <i class="fas fa-arrow-right ml-1"></i>
                        </button>
                    `;
                    chaptersContainer.appendChild(chapterCard);
                });
            }
            
            // Switch sections
            hideAllSections();
            courseDetailSection.classList.remove('hidden');
        } catch (error) {
            console.error('Kurs ma\'lumotlarini yuklashda xato:', error);
            courseDetailSection.innerHTML = `
                <div class="text-center py-12">
                    <i class="fas fa-exclamation-triangle text-4xl text-yellow-500 mb-4"></i>
                    <p class="text-xl font-medium mb-2">Kurs ma\'lumotlarini yuklab bo\'lmadi</p>
                    <p class="text-gray-600 mb-4">${error.message}</p>
                    <button onclick="showCoursesSection()" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                        Kurslar ro'yxatiga qaytish
                    </button>
                </div>
            `;
            hideAllSections();
            courseDetailSection.classList.remove('hidden');
        } finally {
            showLoading(false);
        }
    }
    
    async function showChapterDetail(chapterId) {
        showLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/bobs/${chapterId}/`);
            if (!response.ok) throw new Error('Server xatosi');
            
            const chapter = await response.json();
            
            // Update current chapter ID and store lessons
            currentChapterId = chapterId;
            currentChapterLessons = chapter.lessons || [];
            
            // Update UI
            document.getElementById('chapter-title').textContent = chapter.title;
            document.getElementById('chapter-lesson-count').textContent = chapter.lessons?.length || 0;
            
            // Render lessons
            const lessonsContainer = document.getElementById('chapter-lessons');
            lessonsContainer.innerHTML = '';
            
            if (currentChapterLessons.length === 0) {
                lessonsContainer.innerHTML = `
                    <div class="text-center py-8 text-gray-500">
                        <i class="far fa-file-alt text-3xl mb-2"></i>
                        <p>Hozircha darslar mavjud emas</p>
                    </div>
                `;
            } else {
                currentChapterLessons.forEach((lesson, index) => {
                    const lessonItem = document.createElement('div');
                    lessonItem.className = 'p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition';
                    lessonItem.innerHTML = `
                        <div class="flex justify-between items-center">
                            <div>
                                <div class="flex items-center mb-1">
                                    <span class="bg-gray-100 text-gray-800 text-xs font-medium px-2 py-0.5 rounded mr-2">
                                        ${index + 1}
                                    </span>
                                    <h4 class="font-medium">${lesson.title}</h4>
                                </div>
                                <p class="text-sm text-gray-500 ml-7">
                                    <i class="far fa-clock mr-1"></i>
                                    ${lesson.estimated_reading_time || 0} daqiqa
                                </p>
                            </div>
                            <button onclick="showLessonDetail(${lesson.id})" 
                                    class="text-green-600 hover:text-green-800 text-sm font-medium">
                                O'qish <i class="fas fa-arrow-right ml-1"></i>
                            </button>
                        </div>
                    `;
                    lessonsContainer.appendChild(lessonItem);
                });
            }
            
            // Switch sections
            hideAllSections();
            chapterDetailSection.classList.remove('hidden');
        } catch (error) {
            console.error('Bo\'lim ma\'lumotlarini yuklashda xato:', error);
            chapterDetailSection.innerHTML = `
                <div class="text-center py-12">
                    <i class="fas fa-exclamation-triangle text-4xl text-yellow-500 mb-4"></i>
                    <p class="text-xl font-medium mb-2">Bo\'lim ma\'lumotlarini yuklab bo\'lmadi</p>
                    <p class="text-gray-600 mb-4">${error.message}</p>
                    <button onclick="showCourseDetail(currentCourseId)" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                        Kursga qaytish
                    </button>
                </div>
            `;
            hideAllSections();
            chapterDetailSection.classList.remove('hidden');
        } finally {
            showLoading(false);
        }
    }
    
    async function showLessonDetail(lessonId) {
        showLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/lessons/${lessonId}/`);
            if (!response.ok) throw new Error('Server xatosi');
            
            const lesson = await response.json();
            
            // Update current lesson ID
            currentLessonId = lessonId;
            
            // Update UI
            document.getElementById('lesson-title').textContent = lesson.title;
            document.getElementById('lesson-time').textContent = lesson.estimated_reading_time || 0;
            document.getElementById('lesson-updated').textContent = formatDate(lesson.updated_at);
            document.getElementById('lesson-content').innerHTML = lesson.body || '<p class="text-gray-500">Mazmuni mavjud emas</p>';
            
            // Switch sections
            hideAllSections();
            lessonDetailSection.classList.remove('hidden');
        } catch (error) {
            console.error('Darsni yuklashda xato:', error);
            lessonDetailSection.innerHTML = `
                <div class="text-center py-12">
                    <i class="fas fa-exclamation-triangle text-4xl text-yellow-500 mb-4"></i>
                    <p class="text-xl font-medium mb-2">Darsni yuklab bo\'lmadi</p>
                    <p class="text-gray-600 mb-4">${error.message}</p>
                    <button onclick="showChapterDetail(currentChapterId)" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                        Bo\'limga qaytish
                    </button>
                </div>
            `;
            hideAllSections();
            lessonDetailSection.classList.remove('hidden');
        } finally {
            showLoading(false);
        }
    }
    
    async function performSearch() {
        const query = searchInput.value.trim();
        
        if (query.length < 2) {
            alert('Iltimos, qidirish uchun kamida 2 ta belgi kiriting');
            return;
        }
        
        showLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/search/?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Server xatosi');
            
            const results = await response.json();
            
            // Display results
            searchResultsContent.innerHTML = '';
            
            if ((!results.courses || results.courses.length === 0) && 
                (!results.bobs || results.bobs.length === 0) && 
                (!results.lessons || results.lessons.length === 0)) {
                searchResultsContent.innerHTML = `
                    <div class="text-center py-8 text-gray-500">
                        <i class="fas fa-search text-3xl mb-2"></i>
                        <p>Hech qanday natija topilmadi</p>
                    </div>
                `;
                return;
            }
            
            // Display courses
            if (results.courses && results.courses.length > 0) {
                const coursesHeader = document.createElement('h3');
                coursesHeader.className = 'font-semibold text-lg mb-3 text-gray-800';
                coursesHeader.textContent = 'Kurslar';
                searchResultsContent.appendChild(coursesHeader);
                
                const coursesList = document.createElement('div');
                coursesList.className = 'space-y-2 mb-6';
                
                results.courses.forEach(course => {
                    const courseItem = document.createElement('div');
                    courseItem.className = 'p-3 hover:bg-gray-100 rounded cursor-pointer transition';
                    courseItem.innerHTML = `
                        <div onclick="showCourseDetail(${course.id})" class="flex items-center">
                            <i class="fas fa-book text-green-600 mr-3"></i>
                            <div>
                                <p class="font-medium">${course.title}</p>
                                <p class="text-sm text-gray-500">Kurs</p>
                            </div>
                        </div>
                    `;
                    coursesList.appendChild(courseItem);
                });
                
                searchResultsContent.appendChild(coursesList);
            }
            
            // Display chapters (bobs)
            if (results.bobs && results.bobs.length > 0) {
                const bobsHeader = document.createElement('h3');
                bobsHeader.className = 'font-semibold text-lg mb-3 text-gray-800';
                bobsHeader.textContent = 'Bo\'limlar';
                searchResultsContent.appendChild(bobsHeader);
                
                const bobsList = document.createElement('div');
                bobsList.className = 'space-y-2 mb-6';
                
                results.bobs.forEach(bob => {
                    const bobItem = document.createElement('div');
                    bobItem.className = 'p-3 hover:bg-gray-100 rounded cursor-pointer transition';
                    bobItem.innerHTML = `
                        <div onclick="showChapterDetail(${bob.id})" class="flex items-center">
                            <i class="fas fa-folder-open text-blue-600 mr-3"></i>
                            <div>
                                <p class="font-medium">${bob.title}</p>
                                <p class="text-sm text-gray-500">Bo\'lim</p>
                            </div>
                        </div>
                    `;
                    bobsList.appendChild(bobItem);
                });
                
                searchResultsContent.appendChild(bobsList);
            }
            
            // Display lessons
            if (results.lessons && results.lessons.length > 0) {
                const lessonsHeader = document.createElement('h3');
                lessonsHeader.className = 'font-semibold text-lg mb-3 text-gray-800';
                lessonsHeader.textContent = 'Darslar';
                searchResultsContent.appendChild(lessonsHeader);
                
                const lessonsList = document.createElement('div');
                lessonsList.className = 'space-y-2';
                
                results.lessons.forEach(lesson => {
                    const lessonItem = document.createElement('div');
                    lessonItem.className = 'p-3 hover:bg-gray-100 rounded cursor-pointer transition';
                    lessonItem.innerHTML = `
                        <div onclick="showLessonDetail(${lesson.id})" class="flex items-center">
                            <i class="fas fa-file-alt text-yellow-600 mr-3"></i>
                            <div>
                                <p class="font-medium">${lesson.title}</p>
                                <p class="text-sm text-gray-500">Dars</p>
                            </div>
                        </div>
                    `;
                    lessonsList.appendChild(lessonItem);
                });
                
                searchResultsContent.appendChild(lessonsList);
            }
            
            // Show results section
            hideAllSections();
            searchResults.classList.remove('hidden');
        } catch (error) {
            console.error('Qidiruvda xato:', error);
            searchResultsContent.innerHTML = `
                <div class="text-center py-8 text-red-500">
                    <i class="fas fa-exclamation-circle text-3xl mb-2"></i>
                    <p>Qidiruvda xatolik yuz berdi</p>
                    <p class="text-sm mt-2">${error.message}</p>
                </div>
            `;
            hideAllSections();
            searchResults.classList.remove('hidden');
        } finally {
            showLoading(false);
        }
    }
    
    function navigateToPreviousLesson() {
        if (!currentChapterLessons || currentChapterLessons.length === 0) return;
        
        const currentIndex = currentChapterLessons.findIndex(l => l.id === currentLessonId);
        if (currentIndex > 0) {
            showLessonDetail(currentChapterLessons[currentIndex - 1].id);
        } else {
            alert('Bu birinchi dars');
        }
    }
    
    function navigateToNextLesson() {
        if (!currentChapterLessons || currentChapterLessons.length === 0) return;
        
        const currentIndex = currentChapterLessons.findIndex(l => l.id === currentLessonId);
        if (currentIndex < currentChapterLessons.length - 1) {
            showLessonDetail(currentChapterLessons[currentIndex + 1].id);
        } else {
            alert('Bo\'lim yakunlandi!');
        }
    }
    
    function showCoursesSection(event) {
        if (event) event.preventDefault();
        hideAllSections();
        coursesSection.classList.remove('hidden');
        searchResults.classList.add('hidden');
        searchInput.value = '';
    }
    
    function hideAllSections() {
        coursesSection.classList.add('hidden');
        courseDetailSection.classList.add('hidden');
        chapterDetailSection.classList.add('hidden');
        lessonDetailSection.classList.add('hidden');
    }
    
    function formatDate(dateString) {
        if (!dateString) return 'Noma\'lum';
        const date = new Date(dateString);
        return date.toLocaleDateString('uz-UZ', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    
    // Global funksiyalarni o'rnatish
    window.showCourseDetail = showCourseDetail;
    window.showChapterDetail = showChapterDetail;
    window.showLessonDetail = showLessonDetail;
    window.navigateToPreviousLesson = navigateToPreviousLesson;
    window.navigateToNextLesson = navigateToNextLesson;
    window.showCoursesSection = showCoursesSection;
    window.loadCourses = loadCourses;
});