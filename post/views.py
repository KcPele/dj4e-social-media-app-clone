from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ( 
    ListView, 
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
    )
from accounts.models import User
from post.models import Post, Like, Comment, CommentLike
from post.forms import CommentForm

class OwnerCreateView(LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerCreateView, self).form_valid(form)
class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
class PostListView(ListView):
    model = Post
    def get_ordering(self):
        return '-created_at'

       
        
class PostCreateView(OwnerCreateView):
    model = Post
    fields = ['title', 'body', 'image']

class PostDetailView(DetailView):
    model = Post
    def get(self, request, pk, **kwargs):
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=pk)
        comment_form =  CommentForm()
        context = {
            'post':post,
            'comments':comments,
            'comment_form':comment_form
        }
        return render(request, 'post/post_detail.html', context)

class PostUpdateView(OwnerUpdateView):
    model = Post
    fields = ['title', 'body', 'image']

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post:post')
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class LikeAddView(LoginRequiredMixin, View):
    def post(self, request):
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        user = get_object_or_404(User, id=request.user.id)
        obj, created = Like.objects.get_or_create(post=post, liker=user)
        return redirect(reverse_lazy('post:post'))

class LikeDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        user = get_object_or_404(User, id=request.user.id)
        Like.objects.filter(post=post, liker=user).delete()
        
        return redirect(reverse_lazy('post:post'))

##Comment section
class PostComment(LoginRequiredMixin, View):
    def post(self, request):
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            form = comment_form.save(commit=False)
            form.post = post
            form.comment_user = request.user
            form.save()
        
        
        return redirect(reverse('post:detail', args=[post_id]))


class DeleteComment(DeleteView):
    def post(self, request, pk):
        post_id = request.POST['post_id']
        Comment.objects.get(id=pk, comment_user=request.user).delete()
        return redirect(reverse('post:detail', args=[post_id]))

class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request):
        post_id = request.POST['post_id']
        comment_id = request.POST['comment_id']
        comment = get_object_or_404(Comment, id=comment_id)
        user = get_object_or_404(User, id=request.user.id)
        print(post_id)
        obj, created = CommentLike.objects.get_or_create(comment=comment, commenter=user)
        return redirect(reverse_lazy('post:detail', args=[post_id]))

class UnLikeCommentView(LoginRequiredMixin, View):
    def post(self, request):
        post_id = request.POST['post_id']
        comment_id = request.POST['comment_id']
        comment = get_object_or_404(Comment, id=comment_id)
        user = get_object_or_404(User, id=request.user.id)
        CommentLike.objects.filter(comment=comment, commenter=user).delete()
        
        return redirect(reverse('post:detail', args=[post_id]))
