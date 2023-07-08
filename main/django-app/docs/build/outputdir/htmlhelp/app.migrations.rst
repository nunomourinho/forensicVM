======================
app.migrations package
======================

.. container:: wy-grid-for-nav

   .. container:: wy-side-scroll

      .. container:: wy-side-nav-search

         `ForensicVM <index.html>`__

         .. container::

      .. container:: wy-menu wy-menu-vertical

         .. container:: local-toc

            -  `app.migrations package <#>`__

               -  `Submodules <#submodules>`__
               -  `app.migrations.0001_initial
                  module <#module-app.migrations.0001_initial>`__

                  -  ```Migration`` <#app.migrations.0001_initial.Migration>`__

                     -  ```Migration.dependencies`` <#app.migrations.0001_initial.Migration.dependencies>`__
                     -  ```Migration.initial`` <#app.migrations.0001_initial.Migration.initial>`__
                     -  ```Migration.operations`` <#app.migrations.0001_initial.Migration.operations>`__

               -  `app.migrations.0002_forensicvm
                  module <#module-app.migrations.0002_forensicvm>`__

                  -  ```Migration`` <#app.migrations.0002_forensicvm.Migration>`__

                     -  ```Migration.dependencies`` <#app.migrations.0002_forensicvm.Migration.dependencies>`__
                     -  ```Migration.operations`` <#app.migrations.0002_forensicvm.Migration.operations>`__

               -  `Module contents <#module-app.migrations>`__

   .. container:: section wy-nav-content-wrap

      `ForensicVM <index.html>`__

      .. container:: wy-nav-content

         .. container:: rst-content

            .. container::

               -  ` <index.html>`__
               -  app.migrations package
               -  `View page source <_sources/app.migrations.rst.txt>`__

               --------------

            .. container:: document

               .. container::

                  .. container:: section
                     :name: app-migrations-package

                     .. rubric:: app.migrations package
                        :name: app.migrations-package

                     .. container:: section
                        :name: submodules

                        .. rubric:: Submodules
                           :name: submodules

                     .. container:: section
                        :name: module-app.migrations.0001_initial

                        .. rubric:: app.migrations.0001_initial module
                           :name: app.migrations.0001_initial-module

                        *class*\ ``app.migrations.0001_initial.``\ ``Migration``\ (\ *name*, *app_label*\ )\ `[source] <_modules/app/migrations/0001_initial.html#Migration>`__
                           Bases: ``Migration``

                           ``dependencies``\ *=[]*

                           ``initial``\ *=True*

                           ``operations``\ *=[<CreateModel  name='Server', fields=[('id', <django.db.models.fields.AutoField>), ('name', <django.db.models.fields.CharField>), ('token', <django.db.models.fields.CharField>), ('vnc_password', <django.db.models.fields.CharField>)]>]*

                     .. container:: section
                        :name: module-app.migrations.0002_forensicvm

                        .. rubric:: app.migrations.0002_forensicvm
                           module
                           :name: app.migrations.0002_forensicvm-module

                        *class*\ ``app.migrations.0002_forensicvm.``\ ``Migration``\ (\ *name*, *app_label*\ )\ `[source] <_modules/app/migrations/0002_forensicvm.html#Migration>`__
                           Bases: ``Migration``

                           ``dependencies``\ *=[('app', '0001_initial')]*

                           ``operations``\ *=[<CreateModel  name='forensicVM', fields=[('id', <django.db.models.fields.AutoField>), ('name', <django.db.models.fields.CharField>), ('forensicImage', <django.db.models.fields.CharField>), ('osDetected', <django.db.models.fields.BooleanField>), ('vncHost', <django.db.models.fields.CharField>), ('vncPort', <django.db.models.fields.IntegerField>)]>]*

                     .. container:: section
                        :name: module-app.migrations

                        .. rubric:: Module contents
                           :name: module-contents

            --------------

            .. container::

               © Copyright 2023, Nuno Mourinho.

            Built with `Sphinx <https://www.sphinx-doc.org/>`__ using a
            `theme <https://github.com/readthedocs/sphinx_rtd_theme>`__
            provided by `Read the Docs <https://readthedocs.org>`__.
