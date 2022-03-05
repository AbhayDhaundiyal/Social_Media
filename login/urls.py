from django.urls import  path
from . import views

app_name = 'login'

urlpatterns =[
    path('authenticate/', views.login, name = 'login'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
    path('user/', views.show, name='show'),
    path('posts/', views.Post, name='post'),
    path('posts/<int:id>/', views.posts, name='posts'),
    path('user/like/<int:id>/', views.like, name='like'),
    path('user/unlike/<int:id>/', views.unlike, name='unlike'),
    path('user/comment/<int:id>/', views.comment, name='comment'),
    path('user/all_posts/<int:id>/', views.all_posts, name='all_posts')
]