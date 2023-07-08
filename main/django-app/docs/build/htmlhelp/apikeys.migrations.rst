==========================
apikeys.migrations package
==========================

.. container:: wy-grid-for-nav

   .. container:: wy-side-scroll

      .. container:: wy-side-nav-search

         `ForensicVM <index.html>`__

         .. container::

      .. container:: wy-menu wy-menu-vertical

         .. container:: local-toc

            -  `apikeys.migrations package <#>`__

               -  `Submodules <#submodules>`__
               -  `apikeys.migrations.0001_initial
                  module <#module-apikeys.migrations.0001_initial>`__

                  -  ```Migration`` <#apikeys.migrations.0001_initial.Migration>`__

                     -  ```Migration.dependencies`` <#apikeys.migrations.0001_initial.Migration.dependencies>`__
                     -  ```Migration.initial`` <#apikeys.migrations.0001_initial.Migration.initial>`__
                     -  ```Migration.operations`` <#apikeys.migrations.0001_initial.Migration.operations>`__

               -  `apikeys.migrations.0002_alter_apikey_key
                  module <#module-apikeys.migrations.0002_alter_apikey_key>`__

                  -  ```Migration`` <#apikeys.migrations.0002_alter_apikey_key.Migration>`__

                     -  ```Migration.dependencies`` <#apikeys.migrations.0002_alter_apikey_key.Migration.dependencies>`__
                     -  ```Migration.operations`` <#apikeys.migrations.0002_alter_apikey_key.Migration.operations>`__

               -  `apikeys.migrations.0003_alter_apikey_key
                  module <#module-apikeys.migrations.0003_alter_apikey_key>`__

                  -  ```Migration`` <#apikeys.migrations.0003_alter_apikey_key.Migration>`__

                     -  ```Migration.dependencies`` <#apikeys.migrations.0003_alter_apikey_key.Migration.dependencies>`__
                     -  ```Migration.operations`` <#apikeys.migrations.0003_alter_apikey_key.Migration.operations>`__

               -  `apikeys.migrations.0004_alter_apikey_key
                  module <#module-apikeys.migrations.0004_alter_apikey_key>`__

                  -  ```Migration`` <#apikeys.migrations.0004_alter_apikey_key.Migration>`__

                     -  ```Migration.dependencies`` <#apikeys.migrations.0004_alter_apikey_key.Migration.dependencies>`__
                     -  ```Migration.operations`` <#apikeys.migrations.0004_alter_apikey_key.Migration.operations>`__

               -  `Module contents <#module-apikeys.migrations>`__

   .. container:: section wy-nav-content-wrap

      `ForensicVM <index.html>`__

      .. container:: wy-nav-content

         .. container:: rst-content

            .. container::

               -  ` <index.html>`__
               -  apikeys.migrations package
               -  `View page
                  source <_sources/apikeys.migrations.rst.txt>`__

               --------------

            .. container:: document

               .. container::

                  .. container:: section
                     :name: apikeys-migrations-package

                     .. rubric:: apikeys.migrations package
                        :name: apikeys.migrations-package

                     .. container:: section
                        :name: submodules

                        .. rubric:: Submodules
                           :name: submodules

                     .. container:: section
                        :name: module-apikeys.migrations.0001_initial

                        .. rubric:: apikeys.migrations.0001_initial
                           module
                           :name: apikeys.migrations.0001_initial-module

                        *class*\ ``apikeys.migrations.0001_initial.``\ ``Migration``\ (\ *name*, *app_label*\ )\ `[source] <_modules/apikeys/migrations/0001_initial.html#Migration>`__
                           Bases: ``Migration``

                           ``dependencies``\ *=[('auth', '__first__')]*

                           ``initial``\ *=True*

                           ``operations``\ *=[<CreateModel  name='ApiKey', fields=[('id', <django.db.models.fields.BigAutoField>), ('key', <django.db.models.fields.CharField>), ('created_at', <django.db.models.fields.DateTimeField>), ('user', <django.db.models.fields.related.ForeignKey>)]>]*

                     .. container:: section
                        :name: module-apikeys.migrations.0002_alter_apikey_key

                        .. rubric:: apikeys.migrations.0002_alter_apikey_key
                           module
                           :name: apikeys.migrations.0002_alter_apikey_key-module

                        *class*\ ``apikeys.migrations.0002_alter_apikey_key.``\ ``Migration``\ (\ *name*, *app_label*\ )\ `[source] <_modules/apikeys/migrations/0002_alter_apikey_key.html#Migration>`__
                           Bases: ``Migration``

                           ``dependencies``\ *=[('apikeys', '0001_initial')]*

                           ``operations``\ *=[<AlterField  model_name='apikey', name='key', field=<django.db.models.fields.UUIDField>>]*

                     .. container:: section
                        :name: module-apikeys.migrations.0003_alter_apikey_key

                        .. rubric:: apikeys.migrations.0003_alter_apikey_key
                           module
                           :name: apikeys.migrations.0003_alter_apikey_key-module

                        *class*\ ``apikeys.migrations.0003_alter_apikey_key.``\ ``Migration``\ (\ *name*, *app_label*\ )\ `[source] <_modules/apikeys/migrations/0003_alter_apikey_key.html#Migration>`__
                           Bases: ``Migration``

                           ``dependencies``\ *=[('apikeys', '0002_alter_apikey_key')]*

                           ``operations``\ *=[<AlterField  model_name='apikey', name='key', field=<django.db.models.fields.UUIDField>>]*

                     .. container:: section
                        :name: module-apikeys.migrations.0004_alter_apikey_key

                        .. rubric:: apikeys.migrations.0004_alter_apikey_key
                           module
                           :name: apikeys.migrations.0004_alter_apikey_key-module

                        *class*\ ``apikeys.migrations.0004_alter_apikey_key.``\ ``Migration``\ (\ *name*, *app_label*\ )\ `[source] <_modules/apikeys/migrations/0004_alter_apikey_key.html#Migration>`__
                           Bases: ``Migration``

                           ``dependencies``\ *=[('apikeys', '0003_alter_apikey_key')]*

                           ``operations``\ *=[<AlterField  model_name='apikey', name='key', field=<django.db.models.fields.UUIDField>>]*

                     .. container:: section
                        :name: module-apikeys.migrations

                        .. rubric:: Module contents
                           :name: module-contents

            --------------

            .. container::

               © Copyright 2023, Nuno Mourinho.

            Built with `Sphinx <https://www.sphinx-doc.org/>`__ using a
            `theme <https://github.com/readthedocs/sphinx_rtd_theme>`__
            provided by `Read the Docs <https://readthedocs.org>`__.
