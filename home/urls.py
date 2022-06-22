from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:post_id>/<slug:slug>', views.PostDetailView.as_view(), name='detail'),
    path('post/delete/<int:post_id>', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:post_id>', views.PostUpdateView.as_view(), name='post_update'),
    path('post/create/', views.PostcreateView.as_view(), name='post_create'),
    path('post/like/<int:post_id>', views.PostLikeView.as_view(), name='post_like'),
    path('post/unlike/<int:post_id>', views.PostUnLikeView.as_view(), name='post_unlike')

]
