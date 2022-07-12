from re import A
from django.contrib import admin
from universityApp.models import Student, UserMember
from universityApp.models import course

# Register your models here.
@admin.register(Student)
class studentadmin(admin.ModelAdmin):
    list_display = ('id','std_name','std_address','std_age','std_email','joining_date')


@admin.register(course)
class courseadmin(admin.ModelAdmin):
    list_display = ('id','course_name','fee')

@admin.register(UserMember)
class courseadmin(admin.ModelAdmin):
      list_display = ('id','user_address','user_gender', 'user_mobile','user_photo')  