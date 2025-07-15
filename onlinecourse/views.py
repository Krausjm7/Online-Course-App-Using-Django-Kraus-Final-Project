from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Course, Enrollment, Question, Choice, Submission, Instructor, Learner
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import logging
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required 

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Registration failed. Username already exists.")
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
        
        logger.info(f"Attempting to register new user: {username}")
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        login(request, user)
        messages.success(request, "Registration successful. You are now logged in.")
        return redirect("onlinecourse:index")

def login_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("onlinecourse:index")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("onlinecourse:index")

# --- Homepage, About, Contact ---
def homepage(request):
    return render(request, 'onlinecourse/index.html')

def about(request):
    return render(request, 'onlinecourse/about.html')

def contact(request):
    return render(request, 'onlinecourse/contact.html')

# Course List View (Class-based view)
class CourseListView(generic.ListView):
    model = Course
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'
    
    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.all().order_by('name')
        
        if user.is_authenticated:
            enrolled_courses_ids = Enrollment.objects.filter(user=user).values_list('course_id', flat=True)
            for course in courses:
                course.is_enrolled = course.id in enrolled_courses_ids
        else:
            for course in courses:
                course.is_enrolled = False
        return courses

# Course Detail View (Function-based view)
@login_required # Added decorator here as well, if you intend it to be a protected view
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lesson_set.all().order_by('order')

    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'lessons': lessons,
    }
    return render(request, 'onlinecourse/course_detail_bootstrap.html', context)

@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, "You are already enrolled in this course.")
        return redirect("onlinecourse:course_details", course_id=course.id)

    enrollment = Enrollment.objects.create(user=request.user, course=course, mode='honor', date_enrolled=timezone.now()) 
    
    course.total_enrollment += 1
    course.save()
    
    messages.success(request, f"Successfully enrolled in {course.name}!")
    return redirect("onlinecourse:course_details", course_id=course.id)

@login_required
def submit_exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, "You are not enrolled in this course, so you cannot submit an exam.")
        return redirect('onlinecourse:course_details', course_id=course.id)

    if request.method == 'POST':
        user_submission = Submission.objects.create(enrollment=enrollment, total_grade=0.0)

        questions = course.question_set.all()
        calculated_total_score = 0.0

        for question in questions:
            selected_choice_ids_str = request.POST.getlist(f'question_{question.id}')
            
            selected_choice_ids = []
            for cid_str in selected_choice_ids_str:
                try:
                    selected_choice_ids.append(int(cid_str))
                except ValueError:
                    logger.warning(f"Invalid choice ID received for question {question.id}: {cid_str}")
                    continue
            
            selected_choices_for_question = Choice.objects.filter(id__in=selected_choice_ids, question=question)
            user_submission.choices.add(*selected_choices_for_question)

            correct_choices_for_question = question.choice_set.filter(is_correct=True)
            
            if set(selected_choices_for_question.values_list('id', flat=True)) == \
               set(correct_choices_for_question.values_list('id', flat=True)):
                calculated_total_score += question.grade
        
        user_submission.total_grade = calculated_total_score
        user_submission.save()

        messages.success(request, "Exam submitted successfully!")
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=user_submission.id)
    else:
        messages.info(request, "Please start the exam from the course details page.")
        return redirect('onlinecourse:course_details', course_id=course.id)

@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    
    submission = get_object_or_404(Submission, pk=submission_id, enrollment__user=request.user, enrollment__course=course)
    
    questions = course.question_set.all().order_by('id') 
    
    questions_results = []
    max_score = sum(q.grade for q in questions)
    
    total_score = submission.total_grade 

    for question in questions:
        selected_choices_for_question = submission.choices.filter(question=question)
        all_choices = question.choice_set.all()
        correct_choices_for_question = question.choice_set.filter(is_correct=True)
        
        is_question_correct = (
            set(selected_choices_for_question.values_list('id', flat=True)) == 
            set(correct_choices_for_question.values_list('id', flat=True))
        )
        
        score_earned_for_question = question.grade if is_question_correct else 0

        questions_results.append({
            'question': question,
            'selected_choices': selected_choices_for_question,
            'all_choices': all_choices, 
            'is_correct_answer': is_question_correct,
            'score_earned': score_earned_for_question,
            'correct_choices': correct_choices_for_question,
        })
    
    passing_percentage = 0.7 
    passing_threshold = max_score * passing_percentage

    context = {
        'course': course,
        'submission': submission,
        'questions_results': questions_results,
        'total_score': total_score,
        'max_score': max_score,
        'passing_threshold': passing_threshold,
    }
    return render(request, 'onlinecourse/result.html', context)