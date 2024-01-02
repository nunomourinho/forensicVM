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
