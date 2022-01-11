from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView
from django.views import View
# Create your views here.


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'

class QuizView(View):
    def get(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        context = {
            'obj':quiz
        }
        return render(request, 'quizes/quiz.html', context)