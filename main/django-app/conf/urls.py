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
from django.urls import path, re_path
from django.contrib import admin
from django.views import static
import app.views
from app.views import ProxyNetdata

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('forensicVM', app.views.vnc_proxy_http),
    re_path(r'^static/(?P<path>.*)$', static.serve, {
        'document_root': (settings.DEBUG and 
                          settings.STATICFILES_DIRS or 
                          settings.STATIC_ROOT)
    }),
    # Generic path
    #path('netdata', ProxyNetdata.as_view(upstream='http://192.168.1.112:4200/')),
    re_path(r'(?P<path>.*)', ProxyNetdata.as_view(upstream='http://localhost:19999/')),
    path('', app.views.vnc_proxy_http),
]
