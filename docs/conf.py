import sys
import os
import django
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('../main/django-app'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings'
django.setup()


# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'ForensicVM Server'
copyright = '2023, Nuno Mourinho'
author = 'Eng. Nuno Mourinho, Eng. Mario Candeias, Dr. Rogério Bravo'

release = '1.0'
version = '1.0.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',    
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',	
    #'sphinx_autodoc_typehints',
    #'sphinxcontrib.autodocsumm',
]

templates_path = ['_templates']

html_theme_options = {    
    'authors': [
        'Eng. Nuno Mourinho',
        'Eng. Mario Candeias',
        'Dr. Rogério Matos Bravo',
    ],
}

html_static_path = ['_static']
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    'display_version': False,
}

# -- Options for EPUB output
epub_show_urls = 'footnote'

