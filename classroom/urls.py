from django.urls import include, path
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('', classroom.home, name='home'),
    path('verification/', classroom.bevalide, name='bevalide'),
    path('Profile-edite/', classroom.ProfileUpdateView.as_view(), name='profile-update'),
    path('Profile', TemplateView.as_view(template_name='classroom/profile.html'), name='profile'),
    url(r'Blog/$', classroom.post_list, name='blog'),
    url(r'About/$', TemplateView.as_view(template_name='classroom/about.html'), name='about'),
    url(r'Contact/$', classroom.contact, name='contact'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'r'(?P<post>[-\w]+)/$',classroom.post_detail,name='post_detail'),
    
    path('Eleves/', include(([
        path('Dashboard/', students.viewe, name='viewe'),
        path('Examen/', students.QuizListView.as_view(), name='quiz_list'),
        path('Classes/', students.StudentClassesView.as_view(), name='student_classes'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('Examen/<int:pk>/', students.take_quiz, name='take_quiz'),
        url(r'^enroll-course/$', students.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
        url(r'^Cours/$', students.StudentCourseListView.as_view(), name='student_course_list'),
        url(r'^Cours/(?P<pk>\d+)/$', students.StudentCourseDetailView.as_view(), name='student_course_detail'),
        url(r'^Cours/(?P<pk>\d+)/(?P<module_id>\d+)/$', students.StudentCourseDetailView.as_view(), name='student_course_detail_module'),
    ], 'classroom'), namespace='students')),

    path('Kinders/', include(([
        path('Dashboard/', kinders.viewki, name='viewki'),
    ], 'classroom'), namespace='kinders')),

    path('Profs/', include(([
        path('Dashboard/', teachers.viewp, name='viewp'),
        path('Quiz/', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
