from django.urls import path
from . import views


app_name = 'myblog'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_regist, name='register'),
    path('<str:username>/', views.user_index, name='userindex'),
    path('<str:username>/blogs/', views.user_blogs, name='userblogs'),
    path('<str:username>/blogs/posts/', views.user_posts, name='userposts'),
    path('<str:username>/blogs/drafts/', views.user_drafts, name='userdrafts'),
    path('<str:username>/blogs/newblog/', views.user_newblog, name='newblog'),
    path('<str:username>/logout/', views.user_logout, name='userlogout'),
    path('blogs/detail/<int:id>/', views.blog_detail, name='blogdetail'),
]