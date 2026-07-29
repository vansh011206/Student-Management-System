from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import root_redirect

urlpatterns = [
    path('', root_redirect, name='root_redirect'),
    path('admin/', admin.site.urls),
    path('auth/', include('apps.accounts.urls')),
    path('admin-panel/', include('apps.accounts.admin_urls')),
    path('admin-panel/students/', include('apps.students.student_urls')),
    path('admin-panel/teachers/', include('apps.students.teacher_urls')),
    path('admin-panel/academics/', include('apps.academics.urls')),
    path('teacher/', include('apps.attendance.teacher_urls')),
    path('teacher/exams/', include('apps.exams.teacher_urls')),
    path('student/', include('apps.students.student_portal_urls')),
]

# Media files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
