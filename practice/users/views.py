from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import auth

#회원가입
def signup(request):
    if request.method == "POST":
        #비밀번호 일치 확인
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username = request.POST['username'],
                password = request.POST['password1'],
                email = request.POST['email'],)

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