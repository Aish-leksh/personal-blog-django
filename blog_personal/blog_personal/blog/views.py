from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Post, Comment
from blog.models import Post

def home(request):
    posts = Post.objects.all().order_by('-created_at')[:2]
    return render(request, 'home/home.html', {'posts': posts})

# AUTHENTICATIOn

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'accounts/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            return render(request, 'accounts/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already exists'})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'accounts/register.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')



# BLOG PAGES


@login_required(login_url='login')
def blog_list(request):
    posts = Post.objects.all().order_by('-created_at')

    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        words = query.split()
        for word in words:
            posts = posts.filter(
                Q(title__icontains=word) |
                Q(content__icontains=word)
            )

    if category and category != "All":
     posts = posts.filter(category=category)


    return render(request, 'blog/blog.html', {'posts': posts})


@login_required(login_url='login')
def blog_detail(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        Comment.objects.create(
            post=post,
            user=request.user,
            text=request.POST['text']
        )
        return redirect('blog_detail', id=id)

    return render(request, 'blog/blog_detail.html', {'post': post})


@login_required(login_url='login')
def create_post(request):
    if request.method == "POST":
        Post.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            category=request.POST.get('category'),
            image=request.FILES.get('image'),
            author=request.user
        )

        return redirect('blog')

    return render(request, 'blog/create_post.html')
