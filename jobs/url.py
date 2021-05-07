from django.conf.urls import url
from django.urls import path
from jobs import views

from django.urls import path

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    url(r"^joblist/", views.joblist, name="joblist"),
    url(r"^job/(?P<job_id>\d+)/$", views.detail, name='detail'),
    
    #提交简历
    path('resume/add/', views.ResumeCreateView.as_view(), name="resume-add"),
    path('resume/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),

    path('sentry-debug/', trigger_error),
    # ...
    path('create_hr_user/', views.create_hr_user, name='create_hr_user'),

    url(r"^$", views.joblist, name="name")

]

from django.conf import settings

if settings.DEBUG:
    urlpatterns += [url(u'^detail_resume/(?P<resume_id>\d+)/$', views.detail_resume, name='detail_resume'),]
    # urlpatterns += [url(r'^detail_resume/(?P<resume_id>\d+)/$', views.detail_resume, name='detail_resume'),]