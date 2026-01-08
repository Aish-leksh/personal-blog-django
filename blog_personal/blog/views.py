from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Post, Comment, Like


# HOME PAGE
def home(request):
    featured_posts = Post.objects.filter(is_featured=True).order_by('-created_at')[:2]
    return render(request, 'home/index.html', {
        'show_login': True,
        'featured_posts': featured_posts
    })


def about(request):
    return render(request, 'home/about.html', {'show_login': True})


def contact(request):
    from django.core.mail import send_mail
    from django.conf import settings
    
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email to admin
        full_message = f'''New Contact Form Submission

From: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from the ELEVER contact form.
'''
        send_mail(
            f'[ELEVER Contact] {subject}',
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],  # Send to admin email
            fail_silently=True,
        )
        success = True
    
    return render(request, 'home/contact.html', {'show_login': True, 'success': success})


def post_dream_life(request):
    return render(request, 'home/post_dream_life.html', {'show_login': True})


def post_productive_mornings(request):
    return render(request, 'home/post_productive_mornings.html', {'show_login': True})


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
        from django.core.mail import send_mail
        from django.conf import settings
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            return render(request, 'accounts/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already exists'})

        User.objects.create_user(username=username, email=email, password=password)
        
        # Send welcome email
        if email:
            subject = 'Welcome to ELEVER! 🎉'
            message = f'''Dear {username},

Welcome to ELEVER! We're thrilled to have you join our community.

Your account has been successfully created. You can now:
• Create and share your blog posts
• Like and comment on posts from other creators
• Build your personal profile

Start exploring and sharing your stories with the world!

Best regards,
The ELEVER Team

---
This is an automated message. Please do not reply to this email.
'''
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
        
        return redirect('login')

    return render(request, 'accounts/register.html')



@login_required(login_url='login')
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'accounts/dashboard.html', {'user_posts': user_posts})


@login_required(login_url='login')
def user_delete_post(request, id):
    """Allow user to delete their own post"""
    post = get_object_or_404(Post, id=id)
    # Only allow deletion if user owns the post
    if post.author == request.user:
        post.delete()
    return redirect('dashboard')


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
    user_has_liked = post.likes.filter(user=request.user).exists()

    if request.method == 'POST':
        Comment.objects.create(
            post=post,
            user=request.user,
            text=request.POST['text']
        )
        return redirect('blog_detail', id=id)

    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'user_has_liked': user_has_liked
    })


@login_required(login_url='login')
def create_post(request):
    if request.method == "POST":
        # Handle custom category
        category = request.POST.get('category')
        if category == 'Other':
            category = request.POST.get('custom_category', 'Other')
        
        Post.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            category=category,
            image=request.FILES.get('image'),
            author=request.user
        )

        return redirect('blog')

    return render(request, 'blog/create_post.html')


@login_required(login_url='login')
def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        # User already liked, so unlike
        like.delete()
    
    return redirect('blog_detail', id=id)


@login_required(login_url='login')
def edit_post(request, id):
    """Allow user to edit their own post"""
    post = get_object_or_404(Post, id=id)
    
    # Only allow editing if user owns the post
    if post.author != request.user:
        return redirect('dashboard')
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        category = request.POST.get('category')
        if category == 'Other':
            category = request.POST.get('custom_category', 'Other')
        post.category = category
        
        # Only update image if new one is uploaded
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        
        post.save()
        return redirect('dashboard')
    
    return render(request, 'blog/edit_post.html', {'post': post})


# ============ CUSTOM ADMIN DASHBOARD ============

def staff_required(view_func):
    """Decorator to require staff status"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@staff_required
def admin_dashboard(request):
    """Main admin dashboard with statistics"""
    stats = {
        'total_posts': Post.objects.count(),
        'total_users': User.objects.count(),
        'total_comments': Comment.objects.count(),
        'total_likes': Like.objects.count(),
    }
    recent_posts = Post.objects.order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    return render(request, 'admin/admin_dashboard.html', {
        'stats': stats,
        'recent_posts': recent_posts,
        'recent_users': recent_users,
    })


@staff_required
def admin_posts(request):
    """List all posts for admin management"""
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'admin/admin_posts.html', {'posts': posts})


@staff_required
def admin_users(request):
    """List all users"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin/admin_users.html', {'users': users})


@staff_required
def admin_delete_post(request, id):
    """Delete a post"""
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('admin_posts')


@staff_required
def admin_delete_comment(request, id):
    """Delete a comment"""
    comment = get_object_or_404(Comment, id=id)
    post_id = comment.post.id
    comment.delete()
    return redirect('blog_detail', id=post_id)


@staff_required
def admin_toggle_user_block(request, id):
    """Block or unblock a user and send email notification"""
    from django.core.mail import send_mail
    from django.conf import settings
    
    user = get_object_or_404(User, id=id)
    # Don't allow blocking yourself or superusers
    if user != request.user and not user.is_superuser:
        user.is_active = not user.is_active
        user.save()
        
        # Send email notification
        if not user.is_active:
            # User was blocked
            subject = 'Your ELEVER Account Has Been Suspended'
            message = f'''Dear {user.username},

We regret to inform you that your account on ELEVER has been suspended.

If you believe this was a mistake or would like to appeal this decision, 
please contact our support team.

Best regards,
The ELEVER Team
'''
        else:
            # User was unblocked
            subject = 'Your ELEVER Account Has Been Restored'
            message = f'''Dear {user.username},

Great news! Your account on ELEVER has been restored.

You can now log in and access all features of the platform.

Best regards,
The ELEVER Team
'''
        
        # Send the email
        if user.email:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
    
    return redirect('admin_users')

