from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as authviews
from django.urls import reverse_lazy
from .models import Relation
from django.http import  JsonResponse

class UserRegister(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            messages.success(request, 'you registered successfully!', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLogin(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')

        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)


    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, ' you logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request, 'wrong username or password', 'alert')
                return render(request, self.template_name, {'form': form})


class UserLogout(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')


class UserProfile(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request, user_id):
        is_following = False
        user = User.objects.get(pk=user_id)
        posts = user.post_set.all()
        rel = Relation.objects.filter(follow_from=request.user, follow_to=user)
        if rel.exists():
            is_following = True


        return render(request, self.template_name, {'user': user, 'posts':posts,'is_following':is_following})


class UserPasswordReset(authviews.PasswordResetView):
    template_name = 'account/passresetform.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/passwordResetEmail.html'


class UserPasswordResetDoneView(authviews.PasswordResetDoneView):
    template_name = 'account/PasswordResetDone.html'


class UserPasswordConfirmView(authviews.PasswordResetConfirmView):
    template_name = 'account/PasswordResetConfirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordCompleteView(authviews.PasswordResetCompleteView):
    template_name = "account/PasswordResetComplete.html"


class UserFollowView(LoginRequiredMixin,View):
    def get(self,request,id):
        user = User.objects.get(pk=id)
        rel = Relation.objects.filter(follow_from=request.user,follow_to=user)
        if rel.exists():
            messages.error(request, 'you already following this user ')
        else:
            rel = Relation(follow_from=request.user, follow_to=user)
            rel.save()
            messages.success(request, 'follwed succesfully ','succes')
        return JsonResponse({"valid":True}, status = 200)


class UserUnFollowView(LoginRequiredMixin,View):
    def get(self,request,id):
        user = User.objects.get(pk=id)
        rel = Relation.objects.filter(follow_from=request.user, follow_to=user)
        if rel.exists():
            rel.delete()
            messages.success(request,'unfollowed successfully')
        else:
            messages.error(request,'you are not following this user')
        return redirect('account:profile', id)

