==========
app.models
==========

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
               -  app.models
               -  

               --------------

            .. container:: document

               .. container::

                  .. rubric:: Source code for app.models
                     :name: source-code-for-app.models

                  .. container:: highlight

                     ::

                        # coding=utf-8


                        from django.db import models


                        [docs]class Server(models.Model):
                            name = models.CharField(max_length=30)
                            token = models.CharField(max_length=30)
                            vnc_password = models.CharField(max_length=30)


                        [docs]class forensicVM(models.Model):
                            name = models.CharField(max_length=30)
                            forensicImage = models.CharField(max_length=30)
                            osDetected = models.BooleanField()
                            vncHost = models.CharField(max_length=30)
                            vncPort = models.IntegerField()

                            def __str__(self):
                                return self.name



                            

            --------------

            .. container::

               © Copyright 2023, Nuno Mourinho.

            Built with `Sphinx <https://www.sphinx-doc.org/>`__ using a
            `theme <https://github.com/readthedocs/sphinx_rtd_theme>`__
            provided by `Read the Docs <https://readthedocs.org>`__.
