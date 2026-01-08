"""
URL configuration for blog_personal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # HOME
    path('', blog_views.home, name='home'),
    path('about/', blog_views.about, name='about'),
    path('contact/', blog_views.contact, name='contact'),
    path('post/dream-life/', blog_views.post_dream_life, name='post_dream_life'),
    path('post/productive-mornings/', blog_views.post_productive_mornings, name='post_productive_mornings'),

    # AUTH
    path('login/', blog_views.login_view, name='login'),
    path('register/', blog_views.register_view, name='register'),
    path('dashboard/', blog_views.dashboard, name='dashboard'),
    path('dashboard/post/<int:id>/delete/', blog_views.user_delete_post, name='user_delete_post'),
    path('logout/', blog_views.logout_view, name='logout'),

    # BLOG
    path('blog/', blog_views.blog_list, name='blog'),
    path('blog/create/', blog_views.create_post, name='create_post'),
    path('blog/<int:id>/', blog_views.blog_detail, name='blog_detail'),
    path('blog/<int:id>/like/', blog_views.like_post, name='like_post'),
    path('blog/<int:id>/edit/', blog_views.edit_post, name='edit_post'),

    # CUSTOM ADMIN DASHBOARD
    path('admin-dashboard/', blog_views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/posts/', blog_views.admin_posts, name='admin_posts'),
    path('admin-dashboard/users/', blog_views.admin_users, name='admin_users'),
    path('admin-dashboard/post/<int:id>/delete/', blog_views.admin_delete_post, name='admin_delete_post'),
    path('admin-dashboard/comment/<int:id>/delete/', blog_views.admin_delete_comment, name='admin_delete_comment'),
    path('admin-dashboard/user/<int:id>/toggle-block/', blog_views.admin_toggle_user_block, name='admin_toggle_user_block'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
