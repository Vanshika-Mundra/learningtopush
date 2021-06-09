from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('student/',views.student,name='student'),
    path('searchstudent/',views.searchstudent,name='searchstudent'),
    path('searchstudentdata/',views.searchstudentdata,name='searchstudentdata'),
    path('serachall/',views.searchall,name='searchall'),
    path('searchresult/',views.searchresult,name='searchresult'),
    path('result/',views.result,name='result'),
    path('updateresult/',views.updateresult,name='updateresult'),
    path('fetchcourse/',views.fetchcourses,name='fetchcourses'),
    path('store/',views.calculateresult,name='store')
]