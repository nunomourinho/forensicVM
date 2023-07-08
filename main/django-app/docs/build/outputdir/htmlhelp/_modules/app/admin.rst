=========
app.admin
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
               -  app.admin
               -  

               --------------

            .. container:: document

               .. container::

                  .. rubric:: Source code for app.admin
                     :name: source-code-for-app.admin

                  .. container:: highlight

                     ::

                        # coding=utf-8
                        from django.contrib import admin
                        from .models import Server

                        [docs]@admin.register(Server)
                        class ArticleAdmin(admin.ModelAdmin):
                            pass

            --------------

            .. container::

               © Copyright 2023, Nuno Mourinho.

            Built with `Sphinx <https://www.sphinx-doc.org/>`__ using a
            `theme <https://github.com/readthedocs/sphinx_rtd_theme>`__
            provided by `Read the Docs <https://readthedocs.org>`__.
