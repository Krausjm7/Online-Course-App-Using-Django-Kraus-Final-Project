from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Index/Course List View
    path(route='', view=views.CourseListView.as_view(), name='index'), 
    
    # User Registration
    path('registration/', views.registration_request, name='registration'),
    
    # User Login
    path('login/', views.login_request, name='login'),
    
    # User Logout
    path('logout/', views.logout_request, name='logout'),
    
    # Course Detail View (e.g., /onlinecourse/5/)
    path('<int:course_id>/', views.course_details, name='course_details'),

    # Enroll in Course (e.g., /onlinecourse/5/enroll/)
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),

    # Submit Exam (e.g., /onlinecourse/5/submit/) - handles POST from course_detail_bootstrap.html
    path('<int:course_id>/submit/', views.submit_exam, name="submit"), 

    # Show Exam Result (e.g., /onlinecourse/5/submission/123/result/)
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name="show_exam_result"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)