from rest_framework import serializers


from .models import Answer,Question,Quizattempts,QuizOptions,QuizTopic

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','id']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuizTopic
        fields="__all__"

class QuizOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOptions
        fields = '__all__'
class QuestionSerializer(serializers.ModelSerializer):
    # If you want to display the available options for each question,
    # you can nest the QuizOptionsSerializer. The `related_name='options'`
    # in your model will be used here.
    options = QuizOptionsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = '__all__'

class QuizattemptsSerializer(serializers.ModelSerializer):
    # If you want to include the answers for each quiz attempt,
    # you can use a nested or primary key representation.
    # Here, we're simply using a primary key representation.
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Quizattempts
        fields = '__all__'                        


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Answer
        fields="__all__"



