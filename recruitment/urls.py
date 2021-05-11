"""recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from jobs.models import Job
from . import views
from rest_framework import routers, serializers, viewsets

# ViewSets define the view behavior.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jobs', JobViewSet)


urlpatterns = [
    url(r"^", include("jobs.url")),
    # path('^grappelli/', include('grappelli.urls')),
    # path('^simpleui/', include('simpleui')),
    # url(r"admin/login/?$", views.login_with_captcha, name="adminlogin"),
    path('admin/', admin.site.urls),
    url('^accounts/', include('registration.backends.simple.urls')),
    # url(r'^chaining/', include('smart_selects.urls')),#智能下拉框没实现
    path('api/', include(router.urls)),
    path('i18n/', include('django.conf.urls.i18n')),
    url(r'^api-auth', include('rest_framework.urls')),

    path('captcha/', include('captcha.urls')),
    path("clogin/", views.login_with_captcha, name="clogin"),

    #django_prometheus
    url('', include('django_prometheus.urls')),
]

admin.site.site_header = "将狗科技招聘管理系统"

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#             path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns


urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
