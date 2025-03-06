from django.shortcuts import render

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import  authenticate
from rest_framework import status
from rest_framework.response import Response
from .models import Answer,Question,Quizattempts,QuizOptions,QuizTopic
from .Serializers import TopicSerializer,AnswerSerializer,QuizOptionsSerializer,QuestionSerializer,QuizattemptsSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated

# Create your views here.


#Authentication endpoints

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):

   #get the data
    username = request.data.get('username')
    password=request.data.get('password')
    email=request.data.get('email')

    #validate the data
    if not username or not password  or not email:
        return Response({
            'error':'Please provide the email ,password, and username.'
        },status=status.HTTP_400_BAD_REQUEST)
    
    #check if the user is already existed

    if User.objects.filter(username=username).exists():
        return Response({
            'error':'The username with which you are trying to signup already exists.'
        },status=status.HTTP_400_BAD_REQUEST)
    #add the instance in db
    user= User.objects.create_user(username=username,password=password,email=email)
    user.save()

    #generate token response
    refresh_token= RefreshToken.for_user(user)
    access_token= str(refresh_token.access_token)

    #return response and set token as http only
    response=Response({
        'message':'user created successfully'
    },status=status.HTTP_201_CREATED)

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=False,
        samesite='Lax'

    )

    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    #get the data
    username= request.data.get('username')
    password= request.data.get('password')


    #validate the data

    if not username or not password:
        return Response({'error':'You need to enter both username and password'},status=status.HTTP_400_BAD_REQUEST)
    
    

    #authenticate  the user
    user= authenticate(username=username,password=password)
    if user is None:
        return Response({'error':'Invalid user credentials'},status=status.HTTP_401_UNAUTHORIZED)
    
    #generate a token pair
    refresh= RefreshToken.for_user(user)
      # Add custom claim to the access token payload
    # refresh.access_token['username'] = user.username  # Add the username to the token payload

    access= str(refresh.access_token)

    response= Response({'message':'User successfully authenticated','access_token':access},status=status.HTTP_200_OK)

    response.set_cookie(
        key='access_token',
        value=access,
        httponly=True,
        secure=False,
        samesite='Lax',

    )

    #send the response
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    response= Response({'message':'User logged out successfully'},status=status.HTTP_200_OK)

    response.delete_cookie('access_token')
    return response

#Quiz topic endpoints

@api_view(['GET'])
@permission_classes([AllowAny])
def quiz_topic_list(request):
    topic_list = QuizTopic.objects.all()
    serializer= TopicSerializer(topic_list,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_topic(request):
    serializer= TopicSerializer(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def topicById(request,pk):
    try:
        topic= QuizTopic.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)    

    
    serializer= TopicSerializer(topic)
    return Response(serializer.data,status=status.HTTP_200_OK)


#Question Endpoints

@api_view(['GET'])
def get_questions(request):
    questions=Question.objects.all()
    serializer=QuestionSerializer(questions,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET','DELETE'])
def questionView(request,pk):
    try:
        question=Question.objects.get(id=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer= QuestionSerializer(question)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def questionsByTopic(request,topicId):
    try:
        topic=QuizTopic.objects.get(id=topicId)
    except QuizTopic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    questionList= Question.objects.filter(topic=topicId)
    serializer= QuestionSerializer(questionList,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)




@api_view(['POST'])
def postQuestion(request):
    serializer=TopicSerializer(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

#quiz options Endpoint

@api_view(['GET','POST'])

def OptionsView(request):
    if request.method == 'GET':
        options= QuizOptions.objects.all()
        serializer=QuizOptionsSerializer(options,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer=QuizOptionsSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','DELETE'])
def optionsById(request,pk):
    try:
        option= QuizOptions.objects.get(id=pk)
    except QuizOptions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method ==  'GET':
        serializer= QuizOptionsSerializer(option)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method ==  'DELETE':
        option.delete()
        return Response(status=status.HTTP_200_OK)    


#ENDPOINTS FOR QUIZATTEMPT 

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def quizattempts_list(request):
    if request.method == 'GET':
        attempts= Quizattempts.objects.all()
        serializer= QuizattemptsSerializer(attempts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer= QuizattemptsSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','DELETE'])
@permission_classes([AllowAny])
def attemptsbyId(request,pk):
    try:
        attempt= Quizattempts.objects.get(id=pk)
    except Quizattempts.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer= QuizattemptsSerializer(attempt)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        attempt.delete()
        return Response(status=status.HTTP_200_OK)
    
# @api_view(['PUT'])
# def finalize_score(request,pk):
#     try:
#         attempt= Quizattempts.objects.get(id=pk)
#     except Quizattempts.DoesNotExist:
#         return  Response(status=status.HTTP_400_BAD_REQUEST)

#     #calculate the score using the model method

#     attempt.score= attempt.calculate_score()
#     attempt.save()
#     serializer= QuizattemptsSerializer(attempt)
#     return Response(serializer.data,status=status.HTTP_201_CREATED)

from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quiz_submit_view(request):
    topic_id = request.data.get("topic")
    answers = request.data.get("answers")

    if not topic_id:
        return Response({"error": "topic is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        topic = QuizTopic.objects.get(id=topic_id)
    except QuizTopic.DoesNotExist:
        return Response({"error": "topic selected was invalid"}, status=status.HTTP_400_BAD_REQUEST)
        
    # At this point, request.user is guaranteed to be a valid User
    quiz_attempt = Quizattempts.objects.create(
        student=request.user,
        topic=topic
    )

    for answer_item in answers:
        question_id = answer_item.get("question_id")
        selected_option_id = answer_item.get("selected_option_id")
        if not (question_id and selected_option_id):
            return Response({"error": "each answer must include a question id and selected option"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            question = Question.objects.get(id=question_id)
            selected_option = QuizOptions.objects.get(id=selected_option_id)
        except (Question.DoesNotExist, QuizOptions.DoesNotExist):
            return Response({"error": "the question or the selected option does not exist in our database"}, status=status.HTTP_404_NOT_FOUND)
        
        Answer.objects.create(
            quiz_attempt=quiz_attempt,
            question=question,
            selected_option=selected_option
        )   

    score = quiz_attempt.calculate_score()
    quiz_attempt.score = score
    quiz_attempt.save()

    return Response({
        "message": "Quiz submitted successfully",
        "score": score
    }, status=status.HTTP_201_CREATED)

    
#ENDPOINTS FOR ANSWERS
    
@api_view(['GET','POST'])
def answerviews(request):
    if request.method == 'GET':
        answers= Answer.objects.all()
        serializer= AnswerSerializer(answers,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer= AnswerSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','DELETE'])
def answerById(request,pk):
    try:
        answer= Answer.objects.all()
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer= AnswerSerializer(answer)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        answer.delete()
        return Response(status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([AllowAny])  # You may change this to IsAuthenticated if needed
def getUserProfile(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

                





