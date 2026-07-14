from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog'),
    
    path('create/', views.create_post, name='create_post'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),

]
