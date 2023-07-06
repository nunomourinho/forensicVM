# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ForensicVM'
copyright = '2023, Nuno Mourinho'
author = 'Nuno Mourinho'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

import os
import sys
sys.path.insert(0, os.path.abspath('.'))
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

extensions = [
    'sphinx.ext.autodoc',
    # Add more extensions as needed
]

# Specify the Python modules to document
# For example, to document the module my_module.py:
# autodoc_mock_imports = ['module_name']
autodoc_modules = {
    'views': '/forensicVM/main/django-app/apikeys/views.py',
}

import os
import sys
import django
sys.path.insert(0, os.path.abspath('../main/django-app'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()
