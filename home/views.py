from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import Post, Comment,Like
from django.contrib import messages
from .forms import PostCreateUpdateForm,CommentCreate
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):

    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    form_class = CommentCreate
    def setup(self, request, *args, **kwargs):
        #print(kwargs['post_id'])
        self._post = Post.objects.get(pk=kwargs['post_id'], slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request,*args,**kwargs):
        _liked = False
        if request.user.is_authenticated:
           if Like.objects.filter(post=self._post, user=request.user).exists():
               _liked =True

        comments = self._post.pcomments.filter(is_reply=False)
        return render(request, 'home/detail.html', {'post': self._post, 'comments': comments, 'form': self.form_class,'liked':_liked})

    def post(self,request, *args, **kwargs):
        form =  self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self._post
            new_comment.save()
            messages.success(request, 'your comment submitted successfully', 'success')

            return redirect('home:detail', self._post.id, self._post.slug)


class PostDeleteView(View):

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'post deleted successfully', 'success')
            return redirect('home:home')
        else:
            messages.error(request, 'you dont have access to this action', 'danger')
            return redirect('home:home')


class PostUpdateView(View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post =  self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request,'you dont have access to  this action! ','danger')
            return redirect('home:home')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id):
        post =  self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form':form})

    def post(self, request, post_id):
        post =  self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'post updated successfully', 'success')
            return redirect('home:detail', post.id, post.slug)


class PostcreateView(View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
           new_post = form.save(commit=False)
           new_post.slug = slugify(form.cleaned_data['body'][:30])
           new_post.user = request.user
           new_post.save()
           messages.success(request, 'post created', 'succes')

        return redirect('home:home')


class PostLikeView(LoginRequiredMixin,View):

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if Like.objects.filter(user=request.user, post=post).exists():
            messages.error(request, "you already liked this post", 'success')
            return redirect('home:detail', post.id, post.slug)
        else:
            like = Like(post=post, user=request.user)
            like.save()
            return redirect('home:detail', post.id, post.slug)


class PostUnLikeView(LoginRequiredMixin,View):
    def post(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        if Like.objects.filter(user=request.user, post=post).exists():
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return redirect('home:detail', post.id, post.slug)
        else:
            return redirect('home:detail', post.id, post.slug)

