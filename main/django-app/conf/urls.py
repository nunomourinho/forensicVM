"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.urls import  path, re_path, include
from django.contrib import admin
from django.views import static
import app.views
from app.views import ProxyNetdata, ProxyShellbox
from django.contrib.auth import views as auth_views
#from django_otp.admin import OTPAdminSite
#from django_otp.plugins.otp_totp.models import TOTPDevice
#from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
#from django_otp.forms import OTPAuthenticationForm


#class OTPAdmin(OTPAdminSite):
#   pass

#admin_site = OTPAdmin(name='ForensicVmOTPadmin')
#admin_site.register(User)
#admin_site.register(TOTPDevice, TOTPDeviceAdmin)

urlpatterns = [
    #re_path(r'^admin/', admin_site.urls),
    re_path(r'^admin/', admin.site.urls),
    path('forensicVM', app.views.vnc_proxy_http),
    re_path(r'^static/(?P<path>.*)$', static.serve, {
        'document_root': (settings.DEBUG and 
                          settings.STATICFILES_DIRS or 
                          settings.STATIC_ROOT)
    }),
    # Generic path
    #path('login/', app.views.LoginView.as_view(), name='login'),
    #path('logout/', app.views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('login/', LoginView.as_view(authentication_form=OTPAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('register/', app.views.register, name='register'),
    re_path(r'^netdata/(?P<path>.*)$', ProxyNetdata.as_view()),
    re_path(r'^shell/(?P<path>.*)$', ProxyShellbox.as_view()),
    path('api/', include('apikeys.urls')),
    path('screen', app.views.vnc_proxy_http),
    path('', app.views.VMListView.as_view(), name='vm_list'),
    path('vm-list', app.views.VMListView.as_view(), name='vm_list'),
]
