from django.shortcuts import render
def index(request):
    return render(request, 'home/index.html', {'show_login': True})
def about(request):
    return render(request, 'home/about.html', {'show_login': True})
def contact(request):
    return render(request, 'home/contact.html', {'show_login': True})
def blog(request): 
    return render(request, 'blog/blog.html', {'show_login': True})

