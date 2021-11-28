from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from accounts.models import User
from chat.models import ChatMessage
from chat.forms import MessageForm
from django.utils.html import escape
from django.db.models import Q
# Create your views here.



class ChatView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = MessageForm()
        chat1 = ChatMessage.objects.filter(
            Q(sender_id=request.user.id, reciever_id=pk)| 
            Q(sender=pk, reciever=request.user.id)
        ).order_by('created_at')
        context = {
            'form':form,
            'chat1':chat1,
           
        }
        return render(request, 'chat/message.html', context)

    def post(self, request, pk):
        form = MessageForm(request.POST)
        sender = get_object_or_404(User, id=request.user.id)
        reciever = get_object_or_404(User, id=pk)
        
        context = {
            'form':form,
        }
        if form.is_valid():
            obj = form.save(commit=False)
            obj.reciever = reciever
            obj.sender = sender
            obj.save()
            return redirect(reverse('chat:message', args=[pk]))
        return render(request, 'chat/message.html', context)
