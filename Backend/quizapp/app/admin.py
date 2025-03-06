from django.contrib import admin

# Register your models here.

from .models import QuizTopic,Question,QuizOptions,Quizattempts,Answer

admin.site.register([QuizTopic,QuizOptions,Question,Quizattempts,Answer])


