from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('profile/<int:user_id>', views.UserProfile.as_view(), name='profile'),
    path('reset/', views.UserPasswordReset.as_view(), name='reset_password '),
    path('reset/done', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', views.UserPasswordCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:id>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:id>/', views.UserUnFollowView.as_view(), name='user_unfollow'),
]


