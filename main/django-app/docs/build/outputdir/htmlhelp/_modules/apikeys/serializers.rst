===================
apikeys.serializers
===================

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
               -  apikeys.serializers
               -  

               --------------

            .. container:: document

               .. container::

                  .. rubric:: Source code for apikeys.serializers
                     :name: source-code-for-apikeys.serializers

                  .. container:: highlight

                     ::

                        """
                        This code defines a serializer class ApiKeySerializer that is used to serialize and deserialize instances of the
                        ApiKey model.

                        The ApiKeySerializer class inherits from the ModelSerializer class provided by the Django REST Framework.
                        It specifies the ApiKey model as the model attribute in the Meta class.

                        The fields attribute in the Meta class specifies the fields that should be included in the serialized representation
                        of the ApiKey model. In this case, it includes only the key field.

                        By using this serializer, one can easily convert instances of the ApiKey model to JSON format (serialization) and
                        vice versa (deserialization) when working with API requests and responses.
                        """
                        from rest_framework import serializers
                        from .models import ApiKey

                        [docs]class ApiKeySerializer(serializers.ModelSerializer):
                        [docs]    class Meta:
                                model = ApiKey
                                fields = ['key']

            --------------

            .. container::

               © Copyright 2023, Nuno Mourinho.

            Built with `Sphinx <https://www.sphinx-doc.org/>`__ using a
            `theme <https://github.com/readthedocs/sphinx_rtd_theme>`__
            provided by `Read the Docs <https://readthedocs.org>`__.
