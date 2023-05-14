# coding=utf-8
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template import loader, Context
from django.core.exceptions import ValidationError
from revproxy.views import ProxyView
from .models import Server
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/') # or where you want to redirect after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



def vnc_proxy(request):
    """VNC agente de controlo remoto"""

    token = request.GET.get('token')
    try:
        obj = Server.objects.get(pk=token)

    except Server.DoesNotExist:
        raise ValidationError('identificador errado', code=404)

    except Exception as e:
        raise ValidationError(str(e), code=500)

    host = settings.VNC_PROXY_HOST
    port = settings.VNC_PROXY_PORT
    # password = obj.vnc_password

    return JsonResponse({
        'token': token,
        'host': host,
        'port': port,
        # 'password': password,
        'password': 'os9527'
    })

def vnc_proxy_http(request):
    """VNC agente de controlo remoto"""

    token = request.GET.get('token')
    #assert False
    #try:
    #    obj = Server.objects.get(token=token)

    #except Server.DoesNotExist:
    #    return HttpResponse('Token missing or incorrect.', status=404)

    #except Exception as e:
    #    return HttpResponse(str(e), status=500)

    host = settings.VNC_PROXY_HOST
    port = settings.VNC_PROXY_PORT
    #assert False
    # password = obj.vnc_password

    template = loader.get_template('novnc/vnc.html')
    context = {
        "token": "",
        "host": "localhost",
        "port": 5901,        
        "password": ''
    }
    #context = {

    #}
    #return HttpResponse(template.render())
    return HttpResponse(template.render(context))




class ProxyNetdata(ProxyView):
    upstream = 'http://localhost:19999'

class ProxyShellbox(ProxyView):
    upstream = 'http://localhost:4200'

#class ProxyMeo(ProxyView):
#    upstream = 'https://192.168.1.254'
