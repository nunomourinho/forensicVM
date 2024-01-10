ForensicVM Server development manual
=====================================

.. image:: https://readthedocs.org/projects/forensicvm-server/badge/?version=latest
    :target: https://forensicvm-server.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


.. _forensicVM-server-dev-manual:

Introduction
*************

.. _development-overview:

Overview
--------
Welcome to the ForensicVM Server Development Manual. This document is intended for developers, IT professionals, and system administrators who are interested in contributing to or customizing the ForensicVM server. The `forensicVM` project is a comprehensive tool designed for the virtualization of forensic images, facilitating in-depth analysis and examination in digital forensics.

This manual provides detailed information on the server component of the `forensicVM` project, which is developed using Django and Python. The server acts as the core of the system, handling the conversion of forensic images into a format suitable for virtual machine environments and providing a web interface for interaction.

.. _development-objectives:

Objectives
----------
The primary objectives of this manual are to:

- **Familiarize Developers**: Introduce the architecture, technologies, and frameworks used in the ForensicVM server.
- **Guide Through the Codebase**: Provide insights into the server's code structure, modules, and key functionalities.
- **Enable Customization**: Offer guidance on how to customize and extend the server's capabilities to meet specific requirements.
- **Encourage Contribution**: Encourage contributions to the project by outlining coding standards, best practices, and the process for submitting changes.

.. _target-audience:

Target Audience
---------------
This manual is tailored for:

- **Developers**: Individuals looking to contribute to the ForensicVM project or understand its internal workings.
- **System Administrators**: Professionals interested in deploying, maintaining, or customizing the ForensicVM server.
- **Digital Forensic Analysts**: Experts in digital forensics who wish to extend or modify the server to suit specialized forensic analysis needs.

ForensicVM Server Contribution Learning Path
********************************************

Welcome to the ForensicVM Server Contribution Learning Path! This guide is designed to provide a comprehensive and structured approach for those interested in contributing to the ForensicVM server project. The learning path is carefully curated to cover all the essential technologies and frameworks that form the backbone of the project.

The components of this learning path include W3.CSS, HTML, CSS, JavaScript, Python, Django, and Git, among others. Each of these plays a vital role in the development and maintenance of the forensicVM server. To ensure a high-quality and accessible learning experience, all resources and tutorials recommended in this path are sourced from W3Schools, a well-known and respected online learning platform for web development and programming.

W3Schools offers clear, concise, and interactive tutorials that are perfect for beginners and experienced developers alike. By following this path, you will gain a solid foundation in each of these key areas:

- **Git**: A distributed version control system for tracking changes in source code during software development.
- **HTML**: The standard markup language for creating web pages.
- **CSS**: The language used to style HTML documents.
- **W3.CSS**: A modern CSS framework for faster and easier web development.
- **Django**: A high-level Python web framework that encourages rapid development.
- **JavaScript**: A programming language that enables interactive web pages.
- **Python**: A versatile programming language used in a wide range of applications, including web development.

Additionally, we include learning resources for secondary libraries such as NumPy, Pandas, SciPy, and general data science concepts. These are crucial for handling the advanced functionalities in the forensicVM server project.

Embark on this learning journey with us, and equip yourself with the skills needed to contribute effectively to the forensicVM server project. Let's get started!

HTML
----

Start with HTML to understand the basics of web page structure.

- Learn HTML: `W3Schools HTML Tutorial <https://www.w3schools.com/html/default.asp>`_ (https://www.w3schools.com/html/default.asp)

CSS
---

Learn CSS to style your HTML pages.

- Learn CSS: `W3Schools CSS Tutorial <https://www.w3schools.com/css/default.asp>`_ (https://www.w3schools.com/css/default.asp)

JavaScript
----------

JavaScript is essential for adding interactivity to web pages.

- Learn JavaScript: `W3Schools JavaScript Tutorial <https://www.w3schools.com/js/default.asp>`_ (https://www.w3schools.com/js/default.asp)

W3.CSS
------

W3.CSS is a modern CSS framework with built-in responsiveness.

- Learn W3.CSS: `W3Schools W3.CSS Tutorial <https://www.w3schools.com/w3css/default.asp>`_ (https://www.w3schools.com/w3css/default.asp)

Python
------

Python is the primary programming language used in the forensicVM server.

- Learn Python: `W3Schools Python Tutorial <https://www.w3schools.com/python/default.asp>`_ (https://www.w3schools.com/python/default.asp)

Django
------

Django is a high-level Python web framework that encourages rapid development.

- Learn Django: `W3Schools Django Tutorial <https://www.w3schools.com/django/index.php>`_ (https://www.w3schools.com/django/index.php)

GIT
---

Understanding GIT is crucial for version control and collaboration.

- Learn GIT: `W3Schools GIT Tutorial <https://www.w3schools.com/git/default.asp>`_ (https://www.w3schools.com/git/default.asp)

Secondary Libraries
-------------------

These libraries are used for various advanced functionalities in the project.

NUMPY
#####

NumPy is used for numerical operations in Python.

- Learn NumPy: `W3Schools NumPy Tutorial <https://www.w3schools.com/python/numpy/default.asp>`_ (https://www.w3schools.com/python/numpy/default.asp)

Pandas
######

Pandas is a library providing high-performance, easy-to-use data structures.

- Learn Pandas: `W3Schools Pandas Tutorial <https://www.w3schools.com/python/pandas/default.asp>`_ (https://www.w3schools.com/python/pandas/default.asp)

SCIPY
#####

SciPy is used for scientific and technical computing.

- Learn SciPy: `W3Schools SciPy Tutorial <https://www.w3schools.com/python/scipy/index.php>`_ (https://www.w3schools.com/python/scipy/index.php)

Data Science
#############

General data science concepts can be beneficial.

- Learn Data Science: `W3Schools Data Science Tutorial <https://www.w3schools.com/datascience/default.asp>`_ (https://www.w3schools.com/datascience/default.asp)


.. _getting-started:

Getting Started
****************
To get started with ForensicVM server development, you should have a solid understanding of Python, Django, and web development principles. Familiarity with virtualization technologies and digital forensics concepts will also be beneficial.

In the following sections, we will explore the setup of a development environment, delve into the server's architecture, and guide you through making your first contributions to the project.


.. toctree::
   :maxdepth: 3
   :caption: API Development Manual

   Setup Development Enviroment <setup-development>
   Internal Folder Structure (/forensicVM) <pages/folder_structure>

Comprehensive Overview of ForensicVM Components
************************************************
The section is divided into three key subsections, each derived from specific modules within the ForensicVM project:

The section is divided into three key subsections, each derived from specific modules within the ForensicVM project:

1. **API Keys (`apikeys.rst`)**:
   The API Keys section provides a comprehensive overview of the `apikeys` package, focusing on the server API services available for the Autopsy ForensicVM client plugin and the web client interface. It covers the administrative and operational aspects of API key management within ForensicVM, including submodules such as `apikeys.admin`, `apikeys.apps`, `apikeys.models`, `apikeys.serializers`, `apikeys.tests`, `apikeys.urls`, and `apikeys.views`. This section is essential for understanding how API keys are managed, their lifecycle, and their role in securing and facilitating access to server API services.

2. **Modules (`modules.rst`)**:
   The Modules section provides an overview of the various components that constitute the ForensicVM application. It includes a structured breakdown of the `django-app` package, highlighting its constituent modules such as `apikeys`, `app`, `conf`, and `manage`. This section is crucial for understanding the modular architecture of the ForensicVM project.

3. **Configuration (`conf.rst`)**:
   In the Configuration section, the focus is on the `conf` package, which encompasses settings, URL configurations, and WSGI-related aspects of ForensicVM. It offers a detailed look at modules like `conf.settings`, `conf.urls`, and `conf.wsgi`, essential for configuring and deploying the ForensicVM application effectively.



.. toctree::
   :maxdepth: 3
   :caption: API Development Manual

   API Keys <apikeys>
   Modules <modules>
   Configuration <conf>   
