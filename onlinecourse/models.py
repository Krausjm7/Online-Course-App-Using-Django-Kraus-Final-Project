import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid # This import might not be strictly needed unless you're using UUID fields, but keeping it as per your original.

# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    # total_learners should have a default or be nullable if it's not set on creation
    total_learners = models.IntegerField(default=0) # Added default

    def __str__(self):
        return self.user.username

# Learner model
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + \
               self.occupation

# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=100, default='online course') # Increased max_length
    image = models.ImageField(upload_to='course_images/', null=True, blank=True) # Added null=True, blank=True for flexibility
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    # is_enrolled is typically a property on the view or serializer, not a model field
    # is_enrolled = False # This line should be removed or commented out as it doesn't belong here

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self): # Added __str__ method for better admin display
        return f"{self.title} (Course: {self.course.name})"

# Question model
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField() # Changed to TextField for longer question content
    grade = models.IntegerField(default=1) # Default grade per question, as used in views.py

    def __str__(self):
        return "Question: " + self.content

    # method to calculate if the learner gets the score of the question
    # This method is not directly used in the current views.py logic for scoring,
    # as the scoring is done directly in the show_exam_result view.
    # However, keeping it for potential future use or if it's referenced elsewhere.
    def is_get_score(self, selected_ids):
        all_correct_answers = self.choice_set.filter(is_correct=True)
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids)
        
        # Check if all correct answers were selected AND no incorrect answers were selected
        return set(all_correct_answers.values_list('id', flat=True)) == set(selected_correct.values_list('id', flat=True))


# Choice model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField() # Changed to TextField for longer choice content
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return "Choice: " + self.content

# Enrollment model
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=10, choices=COURSE_MODES, default=AUDIT) # Increased max_length to 10 for 'honor'
    rating = models.FloatField(default=5.0)

    def __str__(self): # Added __str__ method for better admin display
        return f"{self.user.username} enrolled in {self.course.name} ({self.mode})"

# Submission model
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    # *** FIX: Added total_grade field here ***
    total_grade = models.FloatField(default=0.0)

    def __str__(self): # Added __str__ method for better admin display
        return f"Submission {self.id} by {self.enrollment.user.username} for {self.enrollment.course.name}"