from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from .models import User
from .models import Blog, Comment, Tag, Profile
from .forms import BlogForm
from django.contrib import auth
from django.contrib.auth import authenticate


def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'page_obj':page_obj})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)
    tags = blog.tag.all()
    return render(request,'detail.html',{'blog':blog, 'comments':comments, 'tags': tags})

def new(request):
    tags = Tag.objects.all()
    return render(request,'new.html', {'tags': tags})

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST.get('title')
    new_blog.content = request.POST.get('content')
    new_blog.image = request.FILES.get('image')
    new_blog.author = request.user
    new_blog.save()
    #태그를 불러와 각각 id에 해당하는 태그를 불러와 추가
    tags = request.POST.get('tags')
    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        new_blog.tag.add(tag)
    return redirect('detail', new_blog.id)

def edit(request, blog_id):
    edit_blog = get_object_or_404(Blog, pk=blog_id)
    if edit_blog.author != request.user:
        return redirect('home')
    return render(request, 'edit.html', {'edit_blog':edit_blog})


def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('detail', old_blog.id)

    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.save()
        return redirect('detail', old_blog.id)

    return render(request, 'new.html', {'old_blog':old_blog})


def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    return redirect('home')

def create_comment(request, blog_id):
    comment = Comment()
    comment.content = request.POST.get('content')
    comment.blog = get_object_or_404(Blog, pk=blog_id)
    comment.author = request.user
    comment.save()

    return redirect('detail', blog_id)

def new_comment(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'new_comment.html', {'blog':blog})

def like(request, blog_id):
    #로그인 상태인지
    if request.user.is_authenticated:
        blog = get_object_or_404(Blog, pk=blog_id)
        #만약 이 블로그 좋아요 목록에 해당 유저가 존재한다면
        if blog.like_user.filter(pk=request.user.pk).exists():
            blog.like_user.remove(request.user)
        else:
            blog.like_user.add(request.user)
        return redirect('detail', blog_id)
    return redirect('login')

def signup(request):
    if request.method == "POST":
        #비밀번호 일치 확인
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username = request.POST['username'],
                password = request.POST['password1'],
                email = request.POST['email'],
                organization = request.POST['organization'])

            profile = Profile(
                user=user,
                nickname = request.POST['nickname'],
                image = request.FILES.get('profile_image'),)

            profile.save()

            auth.login(request, user)

            return redirect('home')
        #비밀번호 일치하지 않을 때
        return render(request, 'signup.html')
    #포스트 요청이 아닐 때
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        return render(request, "login.html")
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect('home')

def profile (request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'profile.html', {'user_info':user})