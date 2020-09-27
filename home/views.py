from django.shortcuts import render,HttpResponse,redirect
from . models import Contact 
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def home(request):
    return render(request,'home/home.html')
    

def contact(request):
    if request.method == "POST":
        
        name= request.POST['name']
        phone= request.POST['phone']
        email= request.POST['email']
        description= request.POST['desc']
        contact=Contact(name=name,phone=phone,email=email,content=description)
        contact.save()
    return render(request,'home/contact.html')
    

def about(request):
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>80:
        allposts=Post.objects.none()
    else:
        postTitle = Post.objects.filter(title__icontains=query)
        postContent = Post.objects.filter(content__icontains=query)
        allposts = postTitle.union(postContent)
    context ={'allposts':allposts,'query':query}
    return render(request,'home/search.html',context)
    
def handleSignup(request):
    if request.method =="POST":
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        phone=request.POST['phone']
        designation = request.POST['designation']
        branch = request.POST['branch']
        email=request.POST['email']
        password=request.POST['password']
        conpassword=request.POST['conpassword']
        gender=request.POST['gender']
        #checks of form'
        if username[0].isdigit():
            messages.error(request,"Username must start with a character")
            return redirect('home')
        if (len(username) >10 and len(username) < 2):
            messages.error(request,"Username must greater than 2 and shorter than 10")
            return redirect('home')
        if username.isalnum():
            messages.error(request,"Username only contain letters and numbers")
            return redirect('home')

        if password != conpassword:
            messages.error(request,"Password and Confirm password do not match please try again.")
        
        #creating user
        myuser = User.objects.create_user(username,email,password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request,"Your account has been successfully created please login")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method =="POST":
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user = authenticate(username = loginusername , password =loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"successfully logged in")
            return redirect('home')
        else:
            messages.error(request,"username password incorrect")
            return redirect('home')
    return HttpResponse('login')


def handleLogout(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect('home')
