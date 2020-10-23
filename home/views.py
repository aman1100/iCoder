from django.shortcuts import render,HttpResponse,redirect
from . models import Contact 
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from . models import Profile

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
        extendUser =Profile(firstName=firstname,lastName=lastname,username=username,phone=phone,designation=designation,branch=branch,gender=gender,user=myuser)
        extendUser.save()
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
            userProfile = Profile.objects.filter(user=user)[0]
            print(userProfile)
            user_desigantion = userProfile.designation
            print(user_desigantion)
            # messages.success(request,"successfully logged in")
            # return redirect('home')
            if user_desigantion == 'Principal':
                return redirect('principal')
            if user_desigantion == 'Head of department(HOD)':
                return render(request,'home/hod.html')
            if user_desigantion == 'Lecturer':
                return render(request,'home/lecturer.html')
            if user_desigantion == 'Guest Lecturer':
                return render(request,'home/guestLecturer.html')
            if user_desigantion == 'Admin':
                return render(request,'home/admin.html')
            
        else:
            messages.error(request,"username password incorrect")
            return redirect('home')
    return HttpResponse('login')


def handleLogout(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect('home')

def principal(request):
    users = Profile.objects.all()
    hod = Profile.objects.filter(designation='Head of department(HOD)')
    lecturer = Profile.objects.filter(designation='Lecturer')
    guestLecturer = Profile.objects.filter(designation='Guest Lecturer')
    params = {'users':users,'hod':hod,'lecturer':lecturer,'guestLecturer':guestLecturer}
    return render(request,'home/principal.html',params)