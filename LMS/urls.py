"""
URL configuration for LMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.app, name='app')
Class-based views
    1. Add an import:  from other_app.views import app
    2. Add a URL to urlpatterns:  path('', app.as_view(), name='app')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf.urls.static import static
from django.views.static import serve
from  django.conf import settings
urlpatterns = [
    path('',home,name='home'),
    path('about/', about, name="about"),
    path('login/', login, name="login"),
    path('userlogout/',userlogout,name="logout"),
    path('admin_dash/',admin_panel,name="admin_panel"),
    path('student_dash/',student_panel, name="stdeunt_panel"),
    path('teacher_dash/',teacher_panel,name="teacher_panel"),
    path('admin_profile/',admin_profile, name="admin_profile"),
    path('student_profile/',student_profile, name="stdeunt_profile"),
    path('teacher_profile/', teacher_profile, name="teacher_profile"),
    path('add_student/', add_student, name="add_student"),
    path('add_hod/', add_hod, name="add_hod"),
    path('hod_master/', hod_master, name="hod_master"),
    path('update_hod/', update_hod, name="update_hod"),
    path('add_teacher/',add_teacher, name="add_teacher"),
    path('student_master/', student_master, name="student_master"),
    path('teacher_master/', teacher_master, name="teacher_master"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('reset/',reset,name="reset"),
    path('update_teacher_profile/', update_teacher_profile, name='update_teacher_profile'),
    path('update_student_profile/', update_student_profile, name='update_student_profile'),
    path('update_admin_profile/', update_admin_profile, name='update_admin_profile'),
    path('add_notes/',add_notes,name="add_notes"),
    path('get_subjects/', get_subjects, name='get_subjects'),
    path('teacher_note_master/',teacher_note_master,name='teacher_note_master'),
    path('student_master_cc/',student_master_cc,name="student_master_cc"),
    path('student_notes_view/',student_notes_view,name="student_notes_view"),
    path('student_video/',student_video,name='student_video'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

