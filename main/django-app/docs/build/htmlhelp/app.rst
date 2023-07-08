===========
app package
===========

.. container:: wy-grid-for-nav

   .. container:: wy-side-scroll

      .. container:: wy-side-nav-search

         `ForensicVM <index.html>`__

         .. container::

      .. container:: wy-menu wy-menu-vertical

         .. container:: local-toc

            -  `app package <#>`__

               -  `Subpackages <#subpackages>`__
               -  `Submodules <#submodules>`__
               -  `app.admin module <#module-app.admin>`__

                  -  ```ArticleAdmin`` <#app.admin.ArticleAdmin>`__

                     -  ```ArticleAdmin.media`` <#app.admin.ArticleAdmin.media>`__

               -  `app.apps module <#module-app.apps>`__

                  -  ```AppConfig`` <#app.apps.AppConfig>`__

                     -  ```AppConfig.name`` <#app.apps.AppConfig.name>`__

               -  `app.models module <#module-app.models>`__

                  -  ```Server`` <#app.models.Server>`__

                     -  ```Server.DoesNotExist`` <#app.models.Server.DoesNotExist>`__
                     -  ```Server.MultipleObjectsReturned`` <#app.models.Server.MultipleObjectsReturned>`__
                     -  ```Server.id`` <#app.models.Server.id>`__
                     -  ```Server.name`` <#app.models.Server.name>`__
                     -  ```Server.objects`` <#app.models.Server.objects>`__
                     -  ```Server.token`` <#app.models.Server.token>`__
                     -  ```Server.vnc_password`` <#app.models.Server.vnc_password>`__

                  -  ```forensicVM`` <#app.models.forensicVM>`__

                     -  ```forensicVM.DoesNotExist`` <#app.models.forensicVM.DoesNotExist>`__
                     -  ```forensicVM.MultipleObjectsReturned`` <#app.models.forensicVM.MultipleObjectsReturned>`__
                     -  ```forensicVM.forensicImage`` <#app.models.forensicVM.forensicImage>`__
                     -  ```forensicVM.id`` <#app.models.forensicVM.id>`__
                     -  ```forensicVM.name`` <#app.models.forensicVM.name>`__
                     -  ```forensicVM.objects`` <#app.models.forensicVM.objects>`__
                     -  ```forensicVM.osDetected`` <#app.models.forensicVM.osDetected>`__
                     -  ```forensicVM.vncHost`` <#app.models.forensicVM.vncHost>`__
                     -  ```forensicVM.vncPort`` <#app.models.forensicVM.vncPort>`__

               -  `app.tests module <#module-app.tests>`__
               -  `app.views module <#module-app.views>`__

                  -  ```ProxyNetdata`` <#app.views.ProxyNetdata>`__

                     -  ```ProxyNetdata.login_url`` <#app.views.ProxyNetdata.login_url>`__
                     -  ```ProxyNetdata.redirect_field_name`` <#app.views.ProxyNetdata.redirect_field_name>`__
                     -  ```ProxyNetdata.upstream`` <#app.views.ProxyNetdata.upstream>`__

                  -  ```ProxyShellbox`` <#app.views.ProxyShellbox>`__

                     -  ```ProxyShellbox.login_url`` <#app.views.ProxyShellbox.login_url>`__
                     -  ```ProxyShellbox.redirect_field_name`` <#app.views.ProxyShellbox.redirect_field_name>`__
                     -  ```ProxyShellbox.upstream`` <#app.views.ProxyShellbox.upstream>`__

                  -  ```VMListView`` <#app.views.VMListView>`__

                     -  ```VMListView.get()`` <#app.views.VMListView.get>`__
                     -  ```VMListView.process_info_file()`` <#app.views.VMListView.process_info_file>`__

                  -  ```register()`` <#app.views.register>`__
                  -  ```vnc_proxy()`` <#app.views.vnc_proxy>`__
                  -  ```vnc_proxy_http()`` <#app.views.vnc_proxy_http>`__

               -  `Module contents <#module-app>`__

   .. container:: section wy-nav-content-wrap

      `ForensicVM <index.html>`__

      .. container:: wy-nav-content

         .. container:: rst-content

            .. container::

               -  ` <index.html>`__
               -  app package
               -  `View page source <_sources/app.rst.txt>`__

               --------------

            .. container:: document

               .. container::

                  .. container:: section
                     :name: app-package

                     .. rubric:: app package
                        :name: app-package

                     .. container:: section
                        :name: subpackages

                        .. rubric:: Subpackages
                           :name: subpackages

                        .. container:: toctree-wrapper compound

                           -  `app.migrations
                              package <app.migrations.html>`__

                              -  `Submodules <app.migrations.html#submodules>`__
                              -  `app.migrations.0001_initial
                                 module <app.migrations.html#module-app.migrations.0001_initial>`__

                                 -  ```Migration`` <app.migrations.html#app.migrations.0001_initial.Migration>`__

                                    -  ```Migration.dependencies`` <app.migrations.html#app.migrations.0001_initial.Migration.dependencies>`__
                                    -  ```Migration.initial`` <app.migrations.html#app.migrations.0001_initial.Migration.initial>`__
                                    -  ```Migration.operations`` <app.migrations.html#app.migrations.0001_initial.Migration.operations>`__

                              -  `app.migrations.0002_forensicvm
                                 module <app.migrations.html#module-app.migrations.0002_forensicvm>`__

                                 -  ```Migration`` <app.migrations.html#app.migrations.0002_forensicvm.Migration>`__

                                    -  ```Migration.dependencies`` <app.migrations.html#app.migrations.0002_forensicvm.Migration.dependencies>`__
                                    -  ```Migration.operations`` <app.migrations.html#app.migrations.0002_forensicvm.Migration.operations>`__

                              -  `Module
                                 contents <app.migrations.html#module-app.migrations>`__

                     .. container:: section
                        :name: submodules

                        .. rubric:: Submodules
                           :name: submodules

                     .. container:: section
                        :name: module-app.admin

                        .. rubric:: app.admin module
                           :name: app.admin-module

                        *class*\ ``app.admin.``\ ``ArticleAdmin``\ (\ *model*, *admin_site*\ )\ `[source] <_modules/app/admin.html#ArticleAdmin>`__
                           Bases: ``ModelAdmin``

                           *property*\ ``media``

                     .. container:: section
                        :name: module-app.apps

                        .. rubric:: app.apps module
                           :name: app.apps-module

                        *class*\ ``app.apps.``\ ``AppConfig``\ (\ *app_name*, *app_module*\ )\ `[source] <_modules/app/apps.html#AppConfig>`__
                           Bases: ``AppConfig``

                           ``name``\ *='app'*

                     .. container:: section
                        :name: module-app.models

                        .. rubric:: app.models module
                           :name: app.models-module

                        *class*\ ``app.models.``\ ``Server``\ (\ *id*, *name*, *token*, *vnc_password*\ )\ `[source] <_modules/app/models.html#Server>`__
                           Bases: ``Model``

                           *exception*\ ``DoesNotExist``
                              Bases: ``ObjectDoesNotExist``

                           *exception*\ ``MultipleObjectsReturned``
                              Bases: ``MultipleObjectsReturned``

                           ``id``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``name``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``objects``\ *=<django.db.models.manager.Manager object>*

                           ``token``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``vnc_password``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                        *class*\ ``app.models.``\ ``forensicVM``\ (\ *id*, *name*, *forensicImage*, *osDetected*, *vncHost*, *vncPort*\ )\ `[source] <_modules/app/models.html#forensicVM>`__
                           Bases: ``Model``

                           *exception*\ ``DoesNotExist``
                              Bases: ``ObjectDoesNotExist``

                           *exception*\ ``MultipleObjectsReturned``
                              Bases: ``MultipleObjectsReturned``

                           ``forensicImage``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``id``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``name``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``objects``\ *=<django.db.models.manager.Manager object>*

                           ``osDetected``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``vncHost``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                           ``vncPort``
                              A wrapper for a deferred-loading field.
                              When the value is read from this object
                              the first time, the query is executed.

                     .. container:: section
                        :name: module-app.tests

                        .. rubric:: app.tests module
                           :name: app.tests-module

                     .. container:: section
                        :name: module-app.views

                        .. rubric:: app.views module
                           :name: app.views-module

                        *class*\ ``app.views.``\ ``ProxyNetdata``\ (\ *\*args*, *\*\*kwargs*\ )\ `[source] <_modules/app/views.html#ProxyNetdata>`__
                           Bases: ``LoginRequiredMixin``, ``ProxyView``

                           ``login_url``\ *='/login/'*

                           ``redirect_field_name``\ *='next'*

                           ``upstream``\ *='http://localhost:19999'*

                        *class*\ ``app.views.``\ ``ProxyShellbox``\ (\ *\*args*, *\*\*kwargs*\ )\ `[source] <_modules/app/views.html#ProxyShellbox>`__
                           Bases: ``LoginRequiredMixin``, ``ProxyView``

                           ``login_url``\ *='/login/'*

                           ``redirect_field_name``\ *='next'*

                           ``upstream``\ *='http://localhost:4200'*

                        *class*\ ``app.views.``\ ``VMListView``\ (\ *\*\*kwargs*\ )\ `[source] <_modules/app/views.html#VMListView>`__
                           Bases: ``View``

                           ``get``\ (\ *request*\ )\ `[source] <_modules/app/views.html#VMListView.get>`__

                           ``process_info_file``\ (\ *info_file*, *uuid*\ )\ `[source] <_modules/app/views.html#VMListView.process_info_file>`__

                        ``app.views.``\ ``register``\ (\ *request*\ )\ `[source] <_modules/app/views.html#register>`__

                        ``app.views.``\ ``vnc_proxy``\ (\ *request*\ )\ `[source] <_modules/app/views.html#vnc_proxy>`__
                           VNC agente de controlo remoto

                        ``app.views.``\ ``vnc_proxy_http``\ (\ *request*\ )\ `[source] <_modules/app/views.html#vnc_proxy_http>`__
                           VNC agente de controlo remoto

                     .. container:: section
                        :name: module-app

                        .. rubric:: Module contents
                           :name: module-contents

            --------------

            .. container::

               © Copyright 2023, Nuno Mourinho.

            Built with `Sphinx <https://www.sphinx-doc.org/>`__ using a
            `theme <https://github.com/readthedocs/sphinx_rtd_theme>`__
            provided by `Read the Docs <https://readthedocs.org>`__.
