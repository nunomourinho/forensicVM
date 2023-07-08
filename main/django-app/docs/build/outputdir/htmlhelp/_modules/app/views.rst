=========
app.views
=========

.. container:: wy-grid-for-nav

   .. container:: wy-side-scroll

      .. container:: wy-side-nav-search

         `ForensicVM <../../index.html>`__

         .. container::

      .. container:: wy-menu wy-menu-vertical

         .. container:: local-toc

   .. container:: section wy-nav-content-wrap

      `ForensicVM <../../index.html>`__

      .. container:: wy-nav-content

         .. container:: rst-content

            .. container::

               -  ` <../../index.html>`__
               -  `Module code <../index.html>`__
               -  app.views
               -  

               --------------

            .. container:: document

               .. container::

                  .. rubric:: Source code for app.views
                     :name: source-code-for-app.views

                  .. container:: highlight

                     ::

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
                        from django.utils.decorators import method_decorator
                        from django.contrib.auth.decorators import login_required, permission_required
                        from django.contrib.auth.mixins import LoginRequiredMixin
                        import os
                        import xml.etree.ElementTree as ET
                        from django.views import View


                        [docs]def register(request):
                            if request.method == 'POST':
                                form = UserCreationForm(request.POST)
                                if form.is_valid():
                                    user = form.save()
                                    login(request, user)
                                    return redirect('/') # or where you want to redirect after successful registration
                            else:
                                form = UserCreationForm()
                            return render(request, 'register.html', {'form': form})



                        [docs]def vnc_proxy(request):
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

                        [docs]@login_required
                        def vnc_proxy_http(request):
                            """VNC agente de controlo remoto"""

                            #token = request.GET.get('token')


                            #host = settings.VNC_PROXY_HOST
                            #port = settings.VNC_PROXY_PORT

                            #template = loader.get_template('novnc/vnc.html')
                            #context = {
                            #    "token": "",
                            #    "host": "localhost",
                            #    "port": 5901,        
                            #    "password": ''
                            #}


                            iso_dir = '/forensicVM/mnt/iso'

                            iso_files = []
                            for file in os.listdir(iso_dir):
                                if file.endswith('.iso'):
                                    iso_files.append(file)

                            iso_files.sort()
                            return render(request, 'novnc/vnc.html', {'iso_files': iso_files})

                            #return HttpResponse(template.render(context))



                        [docs]class ProxyNetdata(LoginRequiredMixin, ProxyView):
                            login_url = '/login/'  # Replace with your login URL
                            redirect_field_name = 'next'
                            upstream = 'http://localhost:19999'

                        [docs]class ProxyShellbox(LoginRequiredMixin, ProxyView):
                            login_url = '/login/'  # Replace with your login URL
                            redirect_field_name = 'next'
                            upstream = 'http://localhost:4200'

                        #@login_required
                        #class ProxyNetdata(ProxyView):
                        #    upstream = 'http://localhost:19999'

                        #@login_required
                        #class ProxyShellbox(ProxyView):
                        #    upstream = 'http://localhost:4200'

                        #class ProxyMeo(ProxyView):
                        #    upstream = 'https://192.168.1.254'

                        [docs]class VMListView(View):
                        [docs]    @method_decorator(login_required)
                            def get(self, request):
                                vm_path = "/forensicVM/mnt/vm/"
                                vm_exists = os.path.exists(vm_path)

                                if not vm_exists:
                                    return JsonResponse({'error': 'VM path not found'}, status=404)

                                folders = [f for f in os.listdir(vm_path) if os.path.isdir(os.path.join(vm_path, f))]
                                data = []

                                for folder in folders:
                                    try:
                                        info_name = folder + ".info"
                                        print(info_name)
                                        info_file = os.path.join(vm_path, folder, info_name)
                                        if os.path.exists(info_file):
                                           data.append(self.process_info_file(info_file, folder))
                                        else:
                                           data_item = {
                                               'uuid': folder,
                                               'distro': '---',
                                               'hostname': '---',
                                               'osinfo': '---',
                                               'product_name': '---'
                                           }
                                           data.append(data_item)
                                    except Exception as e:
                                        print(str(e))
                                        try:
                                            data_item = {
                                                'uuid': folder,
                                                'distro': '---',
                                                'hostname': '---',
                                                'osinfo': '---',
                                                'product_name': '---'
                                            }
                                            data.append(data_item)
                                        except Exception as e:
                                            print(str(e))

                                return render(request, 'vm_list.html', {'data': data})

                        [docs]    def process_info_file(self, info_file, uuid):
                                tree = ET.parse(info_file)
                                root = tree.getroot()
                                os_data = root.find('operatingsystem')

                                return {
                                    'uuid': uuid,
                                    'distro': os_data.find('distro').text,
                                    'hostname': os_data.find('hostname').text,
                                    'osinfo': os_data.find('osinfo').text,
                                    'product_name': os_data.find('product_name').text
                                }

            --------------

            .. container::

               © Copyright 2023, Nuno Mourinho.

            Built with `Sphinx <https://www.sphinx-doc.org/>`__ using a
            `theme <https://github.com/readthedocs/sphinx_rtd_theme>`__
            provided by `Read the Docs <https://readthedocs.org>`__.
