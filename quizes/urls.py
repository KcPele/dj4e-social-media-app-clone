from django.urls import path
from .views import (
    QuizListView, 
    QuizView
)

app_name = 'quizes'
urlpatterns = [
    path('', QuizListView.as_view(), name='main-view'),
    path('<pk>/', QuizView.as_view(), name='quiz-view'),
]