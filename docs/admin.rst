ForensicVM Administration Manual
================================

.. _forensicVM-admin-manual:

.. contents::
   :local:
   :depth: 2

Introduction
------------

.. _overview:

Overview
********

**ForensicVM** is a comprehensive project designed to assist forensic investigators in the virtualization of forensic images. By utilizing advanced technologies and tools, ForensicVM simplifies the process of analyzing and examining digital evidence in a virtualized environment.

The project consists of two essential components: the ForensicVM client, which is an Autopsy plugin, and the ForensicVM server. These components work seamlessly together to provide a powerful and efficient forensic virtualization solution.

The ForensicVM server, developed using Django and Python, serves as the backbone of the system. It is recommended to install the server on Debian 11, which in turn should be set up on a dedicated bare metal server. This configuration ensures optimal performance and stability for your forensic investigations.

> **Note:** Installing the ForensicVM server on a hypervisor is not recommended. The ForensicVM server itself acts as the hypervisor, and running it within a nested setup may result in unpredictable behavior and performance issues. To maintain the integrity and reliability of your forensic analysis, it is advised to adhere to the recommended server installation setup.

To get started with ForensicVM, your first step is to install the server. For detailed instructions, please refer to the Installation section, where you'll find step-by-step guidance on setting up the server environment correctly.

Once the server is up and running, you can explore the various capabilities and features of ForensicVM by diving into the Usage Section. This section provides comprehensive information on how to make the most out of the project, including tips, best practices, and real-world scenarios.

I would like to emphasize that ForensicVM is an actively developed project. We're continuously working on enhancing its capabilities, improving performance, and adding new features. Stay tuned for updates and exciting developments as we strive to deliver the most effective and reliable forensic virtualization solution available.

Thank you for choosing ForensicVM. We are confident that it will greatly streamline your forensic investigations and contribute to the success of your work.


In the following sections, we will delve into the details of installation requirements, configuration steps, usage instructions, and advanced customization options to help you get the most out of `forensicVM`.

Installation
------------

.. _requirements:

Requirements
------------

Before proceeding with the installation of `forensicVM`, it's important to understand the system requirements and dependencies. The `forensicVM` installation process is designed to be straightforward, with the `install.sh` script handling the installation of all necessary dependencies.

- **Operating System**: A Debian-based Linux distribution is recommended, with Debian 11 being the preferred choice for optimal compatibility and performance.
- **Privileges**: You will need sufficient privileges (typically root access) to execute scripts and install packages on your system.

The `install.sh` script, located in the `setup` directory of the `forensicVM` repository, automates the installation process. It installs all the required dependencies listed in both the `requirements.txt` and `installed_packages.txt` files. These dependencies include a range of Python packages and additional system libraries essential for the server's functionality.

- **Python Packages**: Key Python packages required by the server include `pycryptodome`, `matplotlib`, `pandas`, `scipy`, `statsmodels`, `python-docx`, `xlwt`, `django-excel-response`, `aiofiles`, `opencv-python` (version 4.0 or higher), `apscheduler`, `sphinx_rtd_theme`, `Django` (version 4.1.9), `djangorestframework`, among others.
- **Additional Dependencies**: The script also installs various other packages and dependencies critical for the operation of the `forensicVM` server.

By running the `install.sh` script, you can ensure that all necessary components are correctly installed and configured on your system. This simplifies the setup process, allowing you to focus on utilizing the `forensicVM` server for your forensic investigations.


.. _installation-steps:

Installation Steps
------------------
The `forensicVM` software can be installed by executing the `install.sh` script located in the repository. This script automates the installation process, including the setup of necessary dependencies and configurations. Follow these steps to install `forensicVM`:

1. **Clone the Repository**:
   Begin by cloning the `forensicVM` repository to your local machine. Use the following command:

   .. code-block:: bash

      git clone https://github.com/nunomourinho/forensicVM.git

2. **Navigate to the Repository Directory**:
   Change to the directory where the repository has been cloned:

   .. code-block:: bash

      cd forensicVM

3. **Run the Installation Script**:
   Execute the `install.sh` script with appropriate privileges. This script will install the necessary components and configure the environment for `forensicVM`. Run the following command:

   .. code-block:: bash

      sudo ./setup/install.sh

   Note: The script may prompt for confirmation during the installation of various components.

4. **Verify Installation**:
   After the installation script completes, verify that all components of `forensicVM` are installed correctly. You can check the status of the services or attempt a test run to ensure functionality.

5. **Post-Installation Configuration** (Optional):
   Depending on your specific requirements, you may need to perform additional configuration steps, such as setting up network interfaces or customizing script parameters.

By following these steps, you should have `forensicVM` installed and ready for use on your system. The next section will guide you through the initial configuration and usage of `forensicVM`.


Configuration
**************

.. _initial-configuration:

Initial Configuration
---------------------

.. _configuring-vm:

Configuring the Virtual Machine
-------------------------------

.. _network-settings:

Network Settings
----------------

Usage
*****

.. _running-forensicvm:

Running ForensicVM
------------------

.. _using-run-or-convert:

Using run-or-convert.sh
-----------------------

.. _using-forensic2v:

Using forensic2v.sh
-------------------

.. _using-qemu-img:

Using qemu-img
--------------

Advanced Topics
****************

.. _customization:

Customization
-------------

.. _troubleshooting:

Troubleshooting
---------------

.. _faq:

Frequently Asked Questions (FAQ)
--------------------------------

Appendices
***********

.. _appendix-a:

Appendix A: Reference Material
------------------------------

.. _appendix-b:

Appendix B: Changelog
---------------------

.. _appendix-c:

Appendix C: License Information
-------------------------------

.. _contact-info:

Contact Information
-------------------

Index
******

.. _index:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


