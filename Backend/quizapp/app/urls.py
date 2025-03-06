from django.urls import path
from . import views

urlpatterns = [
    #authentication urls
    path("/signup",views.signup,name="register"),
    path("/login",views.Login,name="login"),
    path("/logout",views.logout,name="logout"),
    path("/quiztopics",views.quiz_topic_list,name="allTopics"),
    path("/quiztopics/<str:pk>",views.topicById,name='topic'),
    path("/questionlist",views.get_questions,name="allquestions"),
    path("/questionlistTopic/<str:topicId>",views.questionsByTopic,name="topicQuestions"),
    path("/question/<str:pk>",views.questionView,name="questionbyId"),
    path("/addquestion",views.postQuestion,name="addQuestion"),
    path("/optionslist",views.OptionsView,name="optionsview"),
    path("/optionslist/<str:pk>",views.optionsById,name='optionsbyID'),
    path("/quizattempts",views.quizattempts_list,name="quizattempts"),
    path("/quizattemptsbyId",views.attemptsbyId,name="attemptsbyId"),
    path("/answerslist",views.answerviews,name="answers"),
    path("/answers/<str:pk>",views.answerById,name='answersbyId'),
    path("/submit",views.quiz_submit_view,name="submit_score"),
    path("/profile/<int:pk>",views.getUserProfile,name="userprofile"),
]