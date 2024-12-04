from django.shortcuts import render,redirect
from django.http import HttpResponse

from .models import Post
from .forms import PostForm, UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
# Create your views here.

@login_required(login_url="/login")
def home(request):
    if request.method=="POST":
       post_id=request.POST.get("post-id")
       post=Post.objects.filter(id=post_id).first()
       if post and post.author.id == request.user.id:
          post.delete() 
       else:
           print("Unauthorized action")
    posts=Post.objects.all()
    return render(request,"main/home.html",{'posts':posts})

@login_required(login_url="/login")
def create_post(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect("/home")
    else:
        form=PostForm()
    return render(request,"main/create_post.html",{'form':form})    

# def login(request):
#     return render(request,"main/login.html")

def sign_up(request):
    if request.method =="POST":
        form =UserRegistrationForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request,user)
            return redirect('home')
    else:
        form =UserRegistrationForm()
    return render(request,'registration/sign_up.html',{'form':form})    

