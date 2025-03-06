
from django.db import models
from django.contrib.auth.models import User

#topic for the quiz
class QuizTopic(models.Model):
    ''' represents the topic for the questions'''
    title=models.CharField(max_length=100)
    description= models.TextField(blank=True)
    def __str__(self):
        return self.title
#questions model
    
class Question(models.Model):
    '''represents the question '''
    topic=models.ForeignKey(QuizTopic,on_delete=models.CASCADE,related_name='questions')
    question=models.TextField()
    def __str__(self):
        return self.question
    

class QuizOptions(models.Model):
    question= models.ForeignKey(Question,on_delete=models.CASCADE,related_name='options')
    option= models.CharField(max_length=200)
    is_correct=models.BooleanField(default=False)
    def __str__(self):
        return self.option
    

class Quizattempts(models.Model):
    student= models.ForeignKey(User,on_delete=models.CASCADE,related_name='quiz_attempts')
    score=models.FloatField(default=0)
    topic=models.ForeignKey(QuizTopic,on_delete=models.CASCADE,related_name='attempts')
    submitted_at= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student} attempted quiz on topic: {self.topic}"
    
    def calculate_score(self):
        correct_count=0

        for answer in self.answers.all():
            if answer.selected_option.is_correct:
                correct_count+=1
        return correct_count


class Answer(models.Model):
    quiz_attempt = models.ForeignKey(Quizattempts,on_delete=models.CASCADE,related_name='answers')
    question= models.ForeignKey(Question,on_delete=models.CASCADE)
    selected_option=models.ForeignKey(QuizOptions,on_delete=models.CASCADE)

    def __str__(self):
        return f"selected option :{self.selected_option}"
    
    



