ForensicVM Server development manual
=====================================

.. image:: https://readthedocs.org/projects/forensicvm-server/badge/?version=latest
    :target: https://forensicvm-server.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. toctree::
   :maxdepth: 3
   :caption: API Development Manual
   
   Internal Folder Structure (/forensicVM) <pages/folder_structure>
   API Keys <apikeys>
   Modules <modules>
   Configuration <conf>   

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
---------------
To get started with ForensicVM server development, you should have a solid understanding of Python, Django, and web development principles. Familiarity with virtualization technologies and digital forensics concepts will also be beneficial.

In the following sections, we will explore the setup of a development environment, delve into the server's architecture, and guide you through making your first contributions to the project.

