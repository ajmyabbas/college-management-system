from tkinter import Message
from urllib import request
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from universityApp.models import Student, UserMember, course
from django.contrib.auth import authenticate,login,logout



# Create your views here.

def home(request):
    return render(request,'home.html')

def loginpage(request):
    return render(request,'login.html')        


def user_signup(request):
    if request.method=='POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        passw=request.POST.get('passw')
        cpassw=request.POST.get('cpassw')
        sel1=request.POST['sel']
        course1=course.objects.get(id=sel1)
        if request.FILES.get('file') is not None:
            image = request.FILES.get('file')
        else:
            image="static/images/user.png"   
        if cpassw == passw:
            if User.objects.filter(username=uname).exists():
                messages.info(request,'username Not available')
                return redirect('user_signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'username Not available')
                return redirect('user_signup')
            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=cpassw)
                user.save()
                u=User.objects.get(id=user.id)
                member=UserMember(user_address=address,user_mobile=mobile,user_age=age,user_gender=gender,user_photo=image,course=course1,user=u)
                member.save()
                return redirect('loginpage') 
    courses=course.objects.all()
    context={'courses':courses}              
    return render(request,'user/usersignup.html',context) 

# login functionality view
def userlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        request.session["uid"]=user.id
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('load_admin_home')
            else:
                login(request,user)
                auth.login(request, user)
                messages.info(request,f'welcome {username}')
                return redirect('load_welcome_page')
        else:
            messages.info(request, 'Invalid Username or Password. Try Again.')
            return redirect('loginpage')
    else:
        return redirect('loginpage')

def usercreate(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        email=request.POST['email']

        if password==cpassword:  #  password matching......
            if User.objects.filter(username=username).exists(): #check Username Already Exists..
                messages.info(request, 'This username already exists!!!!!!')
                #print("Username already Taken..")
                return redirect('signup')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                user.save()
                #messages.info(request, 'SuccessFully completed.......')
                print("Successed...")
        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            print("Password is not Matching.. ") 
            return redirect('signup')   
        return redirect('userlogin')
    else:
        return render(request,'admin/signup.html')
   

#load user home page
@login_required(login_url='loginpage')
def load_welcome_page(request):
    if  request.user.is_staff:
        return redirect('loginpage')
    return render(request,'user/welcome.html') 


@login_required(login_url='loginpage')    
def load_admin_home(request):
    return render(request,'admin/admin_home.html')

#load course adding form
@login_required(login_url='loginpage')
def course1(request):
    if not request.user.is_staff:
        return redirect('loginpage')
    return render(request,'admin/course.html')

@login_required(login_url='loginpage')  
def add_course(request): 
    if request.method=='POST':
        cors=request.POST['cors']
        cfee=request.POST['cfee']
        crs=course() 
        crs.course_name=cors
        crs.fee=cfee
        crs.save()
        return redirect(student1) 

#load student detail enter form
@login_required(login_url='loginpage')
def student1(request):
    courses=course.objects.all()
    context={'courses':courses}
    if not request.user.is_staff:
        return redirect('loginpage')
    return render(request,'admin/student.html',context)

@login_required(login_url='loginpage')
def add_student_details(request):
    if request.method=='POST':
        sname=request.POST['student_name']
        saddress=request.POST['address']
        sage=request.POST['age']
        semail=request.POST['email']
        sjd=request.POST['joining_date']
        sel1=request.POST['sel']
        course1=course.objects.get(id=sel1)

        student=Student(std_name=sname,
                               std_address=saddress,
                               std_age=sage,
                               std_email=semail,
                               joining_date=sjd,
                               course=course1
                               )
        student.save()
        print("hii")
        return redirect('show_studentlist')

@login_required(login_url='loginpage')
def show_studentlist(request):
    students=Student.objects.all()
    courses=course.objects.all()
    con={
        'students':students,
        'courses':courses
    }
    if not request.user.is_staff:
        return redirect('loginpage')
    return render(request,'admin/showstudents.html',con)



#User logout functionality view
@login_required(login_url='loginpage')
def logout(request):
	auth.logout(request)
	return redirect('home')




@login_required(login_url='loginpage')
def show_teacher_list(request):
    teachers=UserMember.objects.all()
    courses=course.objects.all()
    u=User.objects.all()
    con={
        'teachers':teachers,
        'courses':courses,
        'u':u,
    }
    if not request.user.is_staff:
        return redirect('loginpage')
    return render(request,'admin/show_teacher.html',con)


@login_required(login_url='loginpage')
def profile(request):
    teacher=UserMember.objects.get(user=request.user)
    
    con={
        'teacher':teacher,
        
    }
    if request.user.is_staff:
        return redirect('loginpage')
    return render(request,'user/teacherprofile.html',con)

#load edit form
@login_required(login_url='loginpage')
def editprofile(request,uk):
    teacher=UserMember.objects.get(user=uk)
    courses=course.objects.all()
    con={
        'teacher':teacher,
        'courses':courses
    }
    if request.user.is_staff:
        return redirect('loginpage')
    return render(request,'user/edit.html',con)


@login_required(login_url='loginpage')
def editUser(request):
    if request.method=='POST':
        u=UserMember.objects.get(user=request.user)  
        u.user.username=request.POST.get('uname')
        u.user.email=request.POST.get('email')
        u.user_address=request.POST.get('address')
        u.user_mobile=request.POST.get('mobile')
        u.user_age=request.POST.get('age')
        u.user_gender=request.POST.get('gender')
        u.course_id=request.POST['sel']
        if len(request.FILES)!=0:
            u.user_photo =request.FILES.get('file')
        u.save()
        return redirect('profile')
    if request.user.is_staff:
        return redirect('loginpage')
    return render(request, 'user/edit.html',)
    


@login_required(login_url='loginpage')
def delete(request,uk):
    teacher=UserMember.objects.get(user_id=uk)
    u=User.objects.get(id=uk)
    teacher.delete()
    u.delete()
    return redirect('show_teacher_list')



  

