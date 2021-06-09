from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.urls import reverse
from decimal import Decimal as deci

# Create your views here.

def index(request):
    with connection.cursor() as cursor:
        cursor.execute('select prog_id from scheme')
        scheme=cursor.fetchall()
        cursor.execute('select dept_code from department')
        department=cursor.fetchall()
    return render(request,'control/Main.html',{"scheme":scheme,"departments":department})

def student(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from student where enroll_num=%s',[request.POST['enroll_no']])
        row=cursor.fetchall()
        if(len(row)!=0):
            message="Enrollment Number Already Exist"
            color='red'
        else:
            cursor.execute('insert into student values(%s,%s,%s,%s,%s,%s,%s,%s)',[request.POST['enroll_no'],request.POST['name'],
            request.POST['sem'],request.POST['mother_name'],request.POST['father_name'],request.POST['dept_id'],request.POST['prog_id'],
            request.POST.get('adm_yr',2018)])
            message="Student Added Successfully"
            color='green'
        cursor.execute('select prog_id from scheme')
        scheme=cursor.fetchall()
        cursor.execute('select dept_code from department')
        department=cursor.fetchall()
        
    return render(request,'control/Main.html',{"message":message,"scheme":scheme,"departments":department,"color":color})






def searchstudent(request):
    return render(request,'control/Search Student.html')


def searchstudentdata(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from student where enroll_num=%s',[request.POST['enroll_num']])
        student=cursor.fetchall()
        
        if(len(student)==0):
            message="Student Doesn\'t Exists"
            return render(request,'control/Search Student.html',{"message":message})
        sem=student[0][2]
        if sem==1 or sem==2:
            year="FIRST YEAR"
        elif sem==3 or sem==4:
            year="SECOND YEAR"
        elif sem==5 or sem==6:
            year="THIRD YEAR"
        else:
            year="FOURTH YEAR"
        return render(request,'control/Search Student.html',{"student":student,"year":year})

def searchall(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from student')
        studentall=cursor.fetchall()
    return render(request,'control/Search Student.html',{"studentall":studentall})

    
    

def searchresult(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from results where enroll_num=%s AND sem=%s',[request.POST['enroll_num'],request.POST['sem']])
        value=cursor.fetchall()
        if not value:
            return render(request,'control/Result.html',{"message":"No Result Found","searching":True,"enrolldef":request.POST['enroll_num'],"semdef":request.POST['sem']})
        cursor.execute('select dept_name from department where dept_code in(select dept_code from student where enroll_num=%s)',[request.POST['enroll_num']])
        department=cursor.fetchone()
        cursor.execute('select roll_num from results where enroll_num=%s AND sem=%s',[request.POST['enroll_num'],int(request.POST['sem'])])
        rollnum=cursor.fetchone()
        cursor.execute('select student_name,father_name,mother_name from student where enroll_num=%s',[request.POST['enroll_num']])
        student=cursor.fetchall()
        cursor.execute('select courses.course_id,courses.course_name,courses.credit_theory,courses.credit_practical,marks.marks_theory,marks.marks_practical,marks.marks_mt,marks.total,marks.credit_points,marks.grade_points from courses join marks on courses.course_id=marks.course_id and marks.enroll_num=%s and marks.sem=%s;',[request.POST['enroll_num'],request.POST['sem']])
        course=cursor.fetchall()
        cursor.execute('select sgpa,ogpa from results where sem=%s AND enroll_num=%s',[int(request.POST['sem']),request.POST['enroll_num']])
        grades=cursor.fetchall()
        sem=int(request.POST['sem'])
        if sem==1 or sem==2:
            year="FIRST YEAR"
        elif sem==3 or sem==4:
            year="SECOND YEAR"
        elif sem==5 or sem==6:
            year="THIRD YEAR"
        else:
            year="FOURTH YEAR"


    return render(request,'control/Result.html',{"department":department,"rollnum":rollnum,"student":student,"courses":course,"enroll_num":request.POST['enroll_num'],"sem":request.POST['sem'],"year":year,"grades":grades})


def result(request):
    return render(request,'control/Result.html',{"searching":True})

def updateresult(request):
    with connection.cursor() as cursor:
        # cursor.execute('select dept_code from department')
        # departments=cursor.fetchall()
        cursor.execute('select prog_id from scheme')
        scheme=cursor.fetchall()
    return render(request,'control/Updating Result.html',{"scheme":scheme})

def fetchcourses(request):
    with connection.cursor() as cursor:
        cursor.execute('select prog_id from scheme')
        scheme=cursor.fetchall()
        cursor.execute('select * from student where enroll_num=%s',[request.POST['enroll_number']])
        enrollnum=cursor.fetchall()
        if(len(enrollnum)==0):
            message='No Student With this Enrollment number exists'
            return render(request,'control/Updating Result.html',{"message":message,"scheme":scheme})
        cursor.execute('select * from results where enroll_num=%s and sem=%s',[request.POST['enroll_number'],request.POST['sem']])
        stures=cursor.fetchall()
        if stures:
            message='Marks of the student has already been Added for the semester'
            return render(request,'control/Updating Result.html',{"message":message,"scheme":scheme})
        cursor.execute('select course_id,course_name,max_theory,max_prac,max_mt from courses where sem=%s and dept_code in(select dept_code from student where enroll_num=%s)and acad_yr in (select start_yr from student where enroll_num=%s)',[request.POST['sem'],request.POST['enroll_number'],request.POST['enroll_number']])
        courses=cursor.fetchall()
        cursor.execute('select dept_code from student where enroll_num=%s',[request.POST['enroll_number']])
        deptdef=cursor.fetchall()
    if(len(courses)==0):
        value=False
        message='Courses Not Present in the DataBase!!'
    else:
        value=True
        message=''
        
    return render(request,'control/Updating Result.html',{"scheme":scheme,"courses":courses,"values":value,"progdef":request.POST['prog_id'],"message":message,"semdef":request.POST['sem'],"deptdef":deptdef[0][0],"enrolldef":request.POST['enroll_number']})

def calculateresult(request):
    with connection.cursor() as cursor:
        cursor.execute('select course_id,course_name,credit_theory,credit_practical from courses where prog_id=%s AND dept_code=%s AND sem=%s',[request.POST['prog_id_hid'],request.POST['dept_id_hid'],request.POST['sem_hid']])
        item=cursor.fetchall()
        counter=1
        total_credit_points=0
        total_credits=0
        for data in item:
            theory=int(request.POST[str(data[0])])
            practical=int(request.POST[data[1]])
            midterm=int(request.POST[str(counter)])
            total=deci(theory+practical+midterm)
            grades=total/10
            credits=grades*(data[2]+data[3])
            total_credit_points+=credits
            total_credits+=(data[2]+data[3])
            cursor.execute('insert into marks values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[request.POST['prog_id_hid'],data[0],request.POST['enroll_num'],request.POST['sem_hid'],request.POST['dept_id_hid'],theory,practical,midterm,total,credits,grades])
            counter=counter+1
        sgpa=total_credit_points/total_credits
        if(request.POST['sem_hid']==1):
            ogpa=sgpa
        else:
            cursor.execute('select ogpa from results where sem=%s AND enroll_num=%s',[int(request.POST['sem_hid'])-1,request.POST['enroll_num']])
            og=cursor.fetchall()
            if(og):
                sum=og[0][0]*(int(request.POST['sem_hid'])-1)
                sum=sum+sgpa
                ogpa=deci(sum/(int(request.POST['sem_hid'])))
                
            else:
                ogpa=sgpa
                
        cursor.execute('insert into results values(%s,%s,%s,%s,%s,%s,%s)',[request.POST['prog_id_hid'],request.POST['enroll_num'],request.POST['sem_hid'],sgpa,ogpa,request.POST['roll_num'],total_credit_points])


    return render(request,'control/Main.html')
