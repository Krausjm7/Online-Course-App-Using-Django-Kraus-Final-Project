from django.contrib import admin
#Import any new Models here
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission #New Question, Choice, Submission model imports

#Register QuestionInline and ChoiceInline classes here
class ChoiceInline(admin.StackedInline): #ChoiceInline for managing choices within a question
    model = Choice
    extra = 2

class QuestionInline(admin.StackedInline): #QuestionInline for managing questions within a course
    model = Question
    extra = 2

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline] #Added QuestionInline to CourseAdmin
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

class QuestionAdmin(admin.ModelAdmin): #QuestionAdmin to customize Question display and add ChoiceInline
    inlines = [ChoiceInline]
    list_display = ['content']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

#Register Question and Choice models here
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin) 
admin.site.register(Choice) 
admin.site.register(Submission)