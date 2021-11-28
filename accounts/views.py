from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CreateUserForm
from django.http import HttpResponse
from .models import User, Follower, Friend
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView


class CheckUpdateOwner(LoginRequiredMixin, UpdateView):
    def get_queryset(self, request):
        qs = super().get_queryset()
        return qs.filter(id=request.user.id)



class RegisterUser(View):
    model = User
    template_name = 'registration/register.html'
    form = CreateUserForm
    def get(self, request):
        
        context = {
            'form':self.form()
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            return redirect(reverse_lazy('post:post'))
        return render(request, self.template_name, {'form':form})

class ProfileUser(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        context = {
            'user':user
        }
        return render(request, 'registration/profile.html', context)


class FollowUser(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        follower = get_object_or_404(User, id=request.user.id)
        obj, created = Follower.objects.get_or_create(user=user)
        obj.followers.add(follower)
        return redirect(reverse('profile', args=[pk]))

class UnFollowUser(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        followers = get_object_or_404(User, id=request.user.id)
        Follower.objects.get(user=user, followers=followers).delete()
        return redirect(reverse_lazy('profile', args=[pk]))

class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['name', 'gender', 'email', 'bio', 'avater', 'date_of_birth', 'phone_number']
    template_name = 'registration/user_form.html'


class AddFriend(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        friend = get_object_or_404(User, id=request.user.id)
        obj, created = Friend.objects.get_or_create(owner=user)
        obj.friends.add(friend)
        return redirect(reverse('profile', args=[pk]))

class AllFriends(View):
    template_name = 'registration/friends_list.html'
    def get(self, request, pk):
        
        user = get_object_or_404(User, id=pk)
        friends = user.friend.friends.all()
        context = {
            'friends':friends,
        }
        return render(request, self.template_name, context)
