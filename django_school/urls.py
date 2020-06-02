from django.urls import include, path, re_path
from django.contrib import admin
from classroom.views import classroom, students, teachers, kinders

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path(r'admin/', admin.site.urls),
    path('', include('classroom.urls')),
    path('Course/', include('course.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
    path('accounts/signup/kinder/', kinders.KinderSignUpView.as_view(), name='kinder_signup'),
]


admin.site.site_header = "Administration de L'institu.."
admin.site.site_title = "Institu.."
admin.site.index_title = "Bienvenue Admin"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
