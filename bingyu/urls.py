from django.urls import path, re_path
from bingyu import views


urlpatterns = [
    path('', views.index),
    re_path('blog/([0-9a-zA-Z]+)/', views.get_blog),
    path('time/', views.get_time),
    path('register/', views.register),
    path('signin/', views.signin),
    path('signout/', views.signout),
    path('manage/', views.manage),
    path('manage/comments/', views.manage_comments),
    path('manage/blogs/', views.manage_blogs),
    path('manage/time/', views.manage_time),
    path('manage/envelope/', views.manage_envelope),
    path('manage/blogs/create/', views.manage_create_blog),
    path('manage/time/create/', views.manage_create_time),
    path('manage/envelope/create/', views.manage_create_envelope),
    path('manage/blogs/edit/', views.manage_edit_blog),
    path('manage/time/edit/', views.manage_edit_time),
    path('manage/envelope/edit/', views.manage_edit_envelope),
    path('manage/users/', views.manage_users),
    path('api/comments/', views.api_comments),
    path('api/users/', views.api_get_users),
    path('api/blogs/', views.api_blogs),
    path('api/time/', views.api_time),
    path('api/envelope/', views.api_envelope),
    path('upload_ajax/', views.upload_ajax),
    re_path('api/blogs/([0-9a-zA-Z]+)/$', views.api_get_blog),
    re_path('api/time/([0-9a-zA-Z]+)/$', views.api_get_time),
    re_path('api/envelope/([0-9a-zA-Z]+)/$', views.api_get_envelope),
    re_path('api/blogs/([0-9a-zA-Z]+)/delete/$', views.api_delete_blog),
    re_path('api/time/([0-9a-zA-Z]+)/delete/$', views.api_delete_time),
    re_path('api/envelope/([0-9a-zA-Z]+)/delete/$', views.api_delete_envelope),
]