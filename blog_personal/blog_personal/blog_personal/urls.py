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

    # AUTH
    path('login/', blog_views.login_view, name='login'),
    path('register/', blog_views.register_view, name='register'),
    path('dashboard/', blog_views.dashboard, name='dashboard'),
    path('logout/', blog_views.logout_view, name='logout'),

    # BLOG
    path('blog/', blog_views.blog_list, name='blog'),
    path('blog/create/', blog_views.create_post, name='create_post'),
    path('blog/<int:id>/', blog_views.blog_detail, name='blog_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
