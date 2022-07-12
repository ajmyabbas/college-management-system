from unicodedata import name
from django import views
from django.urls import include, path
from.import views

urlpatterns = [
    path('',views.home,name='home'),
    path('loginpage/',views.loginpage,name='loginpage'),

    path('usercreate/',views.usercreate,name="usercreate"),
    path('user_signup/',views.user_signup,name="user_signup"),
    path('userlogin/',views.userlogin,name="userlogin"),
    path('logout/',views.logout,name="logout"),
    
    
    path('load_admin_home',views.load_admin_home,name='load_admin_home'),
    path('student1',views.student1,name='student1'),
    path('add_student_details',views.add_student_details,name='add_student_details'),
    path('course1',views.course1,name='course1'),
    path('add_course',views.add_course,name='add_course'),
    path('show_studentlist',views.show_studentlist,name='show_studentlist'),
    path('show_teacher_list/',views.show_teacher_list,name="show_teacher_list"),

    path('profile',views.profile,name='profile'),
    path('editprofile/<int:uk>',views.editprofile,name='editprofile'),
    path('editUser',views.editUser,name='editUser'),


    
    path('load_welcome_page/',views.load_welcome_page,name="load_welcome_page"),
    path('delete/<int:uk>',views.delete,name='delete'),
    
   
]
