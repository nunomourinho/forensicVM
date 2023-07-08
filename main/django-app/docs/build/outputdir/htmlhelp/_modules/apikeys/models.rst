==============
apikeys.models
==============

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
               -  apikeys.models
               -  

               --------------

            .. container:: document

               .. container::

                  .. rubric:: Source code for apikeys.models
                     :name: source-code-for-apikeys.models

                  .. container:: highlight

                     ::

                        from django.db import models
                        from django.contrib.auth.models import User
                        import uuid

                        [docs]class ApiKey(models.Model):
                            """Model representing an API key associated with a user."""
                            user = models.ForeignKey(User, on_delete=models.CASCADE)
                            key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
                            created_at = models.DateTimeField(auto_now_add=True)

                        [docs]    def mask_key(self):
                                """Return a masked version of the API key."""
                                masked_key_length = 4
                                if self.key is None:
                                    masked_key = 'N/A'
                                else:
                                    masked_key = '*' * (len(str(self.key)) - masked_key_length)
                                    masked_key += str(self.key)[-masked_key_length:]
                                return masked_key

                            def __str__(self):
                                """Return the masked version of the API key when the instance is converted to a string."""
                                return self.mask_key()

            --------------

            .. container::

               © Copyright 2023, Nuno Mourinho.

            Built with `Sphinx <https://www.sphinx-doc.org/>`__ using a
            `theme <https://github.com/readthedocs/sphinx_rtd_theme>`__
            provided by `Read the Docs <https://readthedocs.org>`__.
