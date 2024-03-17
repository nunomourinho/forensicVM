ForensicVM Administration Manual
================================

.. _forensicVM-admin-manual:

.. contents::
   :local:
   :depth: 1

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
*************

Before proceeding with the installation of `forensicVM`, it's important to understand the system requirements and dependencies. The `forensicVM` installation process is designed to be straightforward, with the `install.sh` script handling the installation of all necessary dependencies.

- **Operating System**: A Debian-based Linux distribution is recommended, with Debian 11 being the preferred choice for optimal compatibility and performance.
- **Privileges**: You will need sufficient privileges (typically root access) to execute scripts and install packages on your system.

The `install.sh` script, located in the `setup` directory of the `forensicVM` repository, automates the installation process. It installs all the required dependencies listed in both the `requirements.txt` and `installed_packages.txt` files. These dependencies include a range of Python packages and additional system libraries essential for the server's functionality.

- **Python Packages**: Key Python packages required by the server include `pycryptodome`, `matplotlib`, `pandas`, `scipy`, `statsmodels`, `python-docx`, `xlwt`, `django-excel-response`, `aiofiles`, `opencv-python` (version 4.0 or higher), `apscheduler`, `sphinx_rtd_theme`, `Django` (version 4.1.9), `djangorestframework`, among others.
- **Additional Dependencies**: The script also installs various other packages and dependencies critical for the operation of the `forensicVM` server.

By running the `install.sh` script, you can ensure that all necessary components are correctly installed and configured on your system. This simplifies the setup process, allowing you to focus on utilizing the `forensicVM` server for your forensic investigations.


.. _installation-steps:

Installation Steps
******************
The `forensicVM` software can be installed by executing the `install.sh` script located in the repository. This script automates the installation process, including the setup of necessary dependencies and configurations. Follow these steps to install `forensicVM`:

0. **Install requirements**:
   Use the following command:

   .. code-block:: bash

      apt install -y screen git mc wget curl

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

      bash ./setup/install.sh

   Note: The script may prompt for confirmation during the installation of various components.

4. **Initial Database Setup**:
   After the installation, set up the initial database for `forensicVM`. The system can use SQLite, MySQL, or PostgreSQL as the database backend. Navigate to the Django application directory and configure the database settings before running the Django management commands:

   .. code-block:: bash

      cd /forensicvm/main/django-app      

   **SQLite (Default)**:
   - SQLite is the default database and requires no additional configuration. However, if there is an existing `db.sqlite3` file (example database), it should be deleted to start fresh:

     .. code-block:: bash

        rm db.sqlite3  # Remove if exists

   - Proceed with migrations to create a new SQLite database:

     .. code-block:: bash

        python3 manage.py makemigrations
        python3 manage.py migrate

   **MySQL**:
   - For MySQL, ensure you have MySQL server installed and running.
   - Modify the `DATABASES` setting in `settings.py` to use the MySQL backend:

     .. code-block:: python

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'your_database_name',
                'USER': 'your_mysql_username',
                'PASSWORD': 'your_mysql_password',
                'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
                'PORT': '3306',
            }
        }

   - After configuring, run the migrations:

     .. code-block:: bash

        python3 manage.py makemigrations
        python3 manage.py migrate

   **PostgreSQL**:
   - For PostgreSQL, ensure you have PostgreSQL server installed and running.
   - Modify the `DATABASES` setting in `settings.py` to use the PostgreSQL backend:

     .. code-block:: python

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'your_database_name',
                'USER': 'your_postgresql_username',
                'PASSWORD': 'your_postgresql_password',
                'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
                'PORT': '5432',
            }
        }

   - After configuring, run the migrations:

     .. code-block:: bash

        python3 manage.py makemigrations
        python3 manage.py migrate

   Remember to install the necessary Python packages for MySQL or PostgreSQL if you choose to use them (e.g., `mysqlclient` for MySQL, `psycopg2` for PostgreSQL).


5. **Verify Installation**:
   After completing the installation and database setup, verify that all components of `forensicVM` are installed correctly. You can check the status of the services or attempt a test run to ensure functionality.

6. **Post-Installation Configuration** (Optional):
   Depending on your specific requirements, you may need to perform additional configuration steps, such as setting up network interfaces or customizing script parameters.

By following these steps, you should have `forensicVM` installed and ready for use on your system. The next section will guide you through the initial configuration and usage of `forensicVM`.


By following these steps, you should have `forensicVM` installed and ready for use on your system. The next section will guide you through the initial configuration and usage of `forensicVM`.


Configuration
-------------

.. _initial-configuration:

Initial Configuration
**********************

.. _django-admin-setup:

Setting Up the Master Django Admin Account
###########################################

After successfully installing the `forensicVM` server, the next crucial step is to set up the master Django admin account. This account will allow you to manage the Django application and perform administrative tasks. Follow these steps to create the initial administrator account:

1. **Navigate to the Django Application Directory**:
   Change to the directory containing the Django application:

   .. code-block:: bash

      cd main/django-app

2. **Activate the Python Virtual Environment**:
   Before running any Django management commands, activate the Python virtual environment:

   .. code-block:: bash

      #source env_linux/bin/activate

3. **Create the Master Admin Account**:
   Use Django's `manage.py` script to create a new superuser account. This account will have full access to the Django admin interface:

   .. code-block:: bash

      python3 manage.py createsuperuser

   Follow the prompts to set up the username, email, and password for the admin account.

4. **Verify the Account Creation**:
   After completing the setup, you can verify the creation of the admin account by starting the Django development server and accessing the admin panel:

   .. code-block:: bash

      python3 manage.py runserver

   Navigate to `http://<serverip>:8000/admin` in your web browser and log in with the credentials you just created.

5. **Deactivate the Virtual Environment** (Optional):
   Once you have verified that the admin account is working correctly, you can deactivate the virtual environment:

   .. code-block:: bash

      deactivate

With these steps, you have successfully set up the master Django admin account for your `forensicVM` server. This account is essential for managing the Django application and configuring various aspects of the `forensicVM` system.


Creating Additional Users and API Keys
**************************************

.. _additional-users-api-keys:

After setting up the master Django admin account, the next important step for administrators is to create additional user accounts and API keys. These accounts are essential for team members who need access to the `forensicVM` system, and API keys are required for integrating with other tools or services.

1. **Log into the Django Admin Interface**:
   Access the Django admin interface by navigating to `http://<your-server-address>/admin` in your web browser. Log in using the master admin account credentials you created earlier.

2. **Add a New User**:
   In the Django admin interface, navigate to the `Users` section. Here, you can add new users by clicking on the `Add User` button. Fill in the required details for each user, including username and password. Ensure to assign appropriate permissions based on the user's role and responsibilities.

3. **Create API Keys**:
   For each user who requires API access, create an API key. This key will be used for authentication when the user interacts with the `forensicVM` system through external tools or services.

   - In the Django admin interface, go to the `API Keys` section.
   - Select the user for whom you want to create an API key.
   - Generate a new API key and provide it to the user securely.

4. **Manage User Permissions**:
   It's important to manage user permissions carefully. Assign permissions based on the principle of least privilege, ensuring users have access only to the features and data necessary for their role.

5. **Document API Key Usage**:
   Keep a record of all issued API keys, the users they are associated with, and their intended purposes. This documentation will help in managing access and troubleshooting any issues related to API usage.

For a detailed step-by-step guide on how to add new users and create API keys, please refer to the `forensicVM Autopsy Plugin User Manual`. The manual provides comprehensive instructions on this process. You can access it here: [Adding a New User in forensicVM](https://forensicvm-autopsy-plugin-user-manual.readthedocs.io/en/latest/user/installation_and_setup.html#step-6-add-a-new-user).

.. _network-settings:

Network Settings
****************

.. _network-configuration:

Configuring the Network as a Bridge
-----------------------------------
For the `forensicVM` server to function correctly, it's essential to configure the network as a bridge. This setup allows the server to communicate efficiently with the virtualized forensic images. The bridge network will be named `br0`. Follow these steps to configure your network:

1. **Identify the Network Interface**:
   - Determine the name of the network interface you want to bridge. This is typically something like `enp2s0` or `eth0`. You can find this information using the command:

     .. code-block:: bash

        ip link show

2. **Edit Network Configuration**:
   - Open the network configuration file for editing. This file is usually located at `/etc/network/interfaces` or a similar path, depending on your Linux distribution.

     .. code-block:: bash

        sudo nano /etc/network/interfaces

   - Add the following configuration to the file, replacing `enp2s0` with your actual network interface name:

     .. code-block:: none

        # Original interface configuration
        iface enp2s0 inet manual

        # Bridge configuration
        auto br0
        iface br0 inet static
            address 192.168.1.112/24
            gateway 192.168.1.254
            bridge-ports enp2s0
            bridge-stp off
            bridge-fd 0

   - Replace `192.168.1.112/24` with the static IP address you want to assign to the bridge, and `192.168.1.254` with your network's gateway address.

3. **Restart Networking Service**:
   - After saving the changes, restart the networking service to apply the new configuration:

     .. code-block:: bash

        sudo systemctl restart networking

   - Alternatively, you can reboot the system.

4. **Verify the Configuration**:
   - Once the network service is restarted, verify that the bridge is correctly configured and operational:

     .. code-block:: bash

        ip addr show br0

By completing these steps, you will have configured a network bridge named `br0` on your `forensicVM` server. This bridge allows the server to manage network traffic to and from the virtualized forensic images effectively.



.. _running-forensicvm:

Running ForensicVM
------------------

.. _running-forensicvm:

The `forensicVM` service can be managed using the `systemctl` command, which is part of the systemd system and service manager in Linux. This section provides a guide on how to start, stop, and check the status of the `forensicVM` service.

Starting the Service
********************
To start the `forensicVM` service, use the following command:

.. code-block:: bash

    sudo systemctl start forensicvm

This command will initiate the `forensicVM` service based on the configuration specified in the `forensicvm.service` file.

Stopping the Service
********************
If you need to stop the `forensicVM` service, you can do so using the command:

.. code-block:: bash

    sudo systemctl stop forensicvm

This will halt the `forensicVM` service, stopping all its operations.

Checking the Service Status
***************************
To check the current status of the `forensicVM` service, including whether it is running or stopped, use:

.. code-block:: bash

    sudo systemctl status forensicvm

This command provides information about the service's status, along with recent log entries that can be helpful for troubleshooting.

Restarting the Service
**********************
In some cases, you might need to restart the `forensicVM` service, especially after making configuration changes. Use the following command to restart:

.. code-block:: bash

    sudo systemctl restart forensicvm

Enabling and Disabling Auto-start
*********************************
To enable the `forensicVM` service to start automatically at system boot, use:

.. code-block:: bash

    sudo systemctl enable forensicvm

Conversely, if you wish to disable the automatic start of the `forensicVM` service, use:

.. code-block:: bash

    sudo systemctl disable forensicvm

By following these instructions, you can effectively manage the `forensicVM` service on your system, ensuring that it runs as expected and is available when needed.


Updating ForensicVM Server
---------------------------

.. _updating-forensicvm-server:

Updating the `forensicVM` server involves a few key steps to ensure that both the application and its underlying system packages are up-to-date. This process is similar to the initial installation but does not involve deleting the existing database. It's important to stop the `forensicVM` service before updating.

1. **Stop the ForensicVM Service**:
   Before beginning the update process, ensure that the `forensicVM` service is stopped:

   .. code-block:: bash

      sudo systemctl stop forensicvm

2. **Update the Repository**:
   If you have cloned the `forensicVM` repository, navigate to the directory and pull the latest changes:

   .. code-block:: bash

      cd forensicVM
      git pull

3. **Run the Update Script**:
   Execute the `install.sh` script to update the `forensicVM` server. This script will update the necessary components and configurations without affecting the existing database:

   .. code-block:: bash

      sudo ./setup/install.sh

   Note: The script may prompt for confirmation during the update of various components.

4. **Update Installed Debian Packages**:
   Before restarting the `forensicVM` service, it's a good practice to update the installed Debian packages to ensure all system components are up-to-date:

   .. code-block:: bash

      sudo apt-get update
      sudo apt-get upgrade

5. **Restart the ForensicVM Service**:
   After completing the updates, restart the `forensicVM` service to apply the changes:

   .. code-block:: bash

      sudo systemctl start forensicvm

6. **Verify the Update**:
   Check the status of the `forensicVM` service to ensure that the update was successful and the service is running correctly:

   .. code-block:: bash

      sudo systemctl status forensicvm

By following these steps, you can update the `forensicVM` server while preserving your existing database and configurations. This ensures that your `forensicVM` environment remains up-to-date with the latest features, security updates, and system packages.



Advanced Topics
****************

Troubleshooting
---------------
.. _troubleshooting-forensicvm:

In this section, we'll cover some basic troubleshooting steps for the `forensicVM` service. This includes how to start and stop the service and how to use `journalctl` to view system logs, which can be crucial for diagnosing issues.

Starting and Stopping the Service
**********************************
If you encounter issues with the `forensicVM` service, the first steps are often to stop and then restart the service. This can resolve many common problems.

- **To stop the service**:

  .. code-block:: bash

      sudo systemctl stop forensicvm

- **To start the service**:

  .. code-block:: bash

      sudo systemctl start forensicvm

Viewing Logs with journalctl
*****************************
The `journalctl` command is a powerful tool for reviewing system logs, which can provide valuable insights into what's happening with the `forensicVM` service.

- **To view logs for the `forensicVM` service**:

  .. code-block:: bash

      sudo journalctl -u forensicvm

  This command displays the logs generated by the `forensicVM` service. You can use various options with `journalctl` to filter or navigate through the logs:

  - **-f**: Follows the log in real-time.
  - **--since today**: Shows logs since the start of the current day.
  - **-n**: Shows the last 'n' lines of logs.

- **To follow the latest log entries in real-time**:

  .. code-block:: bash

      sudo journalctl -u forensicvm -f

  This is particularly useful for monitoring the service's behavior after starting it or making configuration changes.

- **To view logs within a specific time frame**:

  .. code-block:: bash

      sudo journalctl -u forensicvm --since "2024-01-01 00:00:00" --until "2024-01-02 00:00:00"

  Replace the dates and times with the range relevant to your troubleshooting needs.

By using these commands, you can effectively manage and troubleshoot the `forensicVM` service. The logs provided by `journalctl` are often key to understanding and resolving any issues you may encounter.

Editing ForensicVM Machine Configuration
*****************************************

.. _editing-forensicvm-vm-config:

ForensicVM virtual machines are configured through shell scripts that specify how they should be launched and managed. These scripts include various parameters for the QEMU virtualization tool. Here's how to edit these configuration scripts:

1. **Locate the Configuration Script**:
   - The scripts are typically located in the `/forensicVM/mnt/vm/` directory, within a subdirectory named after the VM's unique identifier. For example:

     .. code-block:: bash

        cd /forensicVM/mnt/vm/d30c9683-fbe7-5f36-985d-d48ba9dbee5e

2. **Open the Script for Editing**:
   - Use a text editor to open the script file. For instance, to edit the `S0002-P0001.qcow2-vnc.sh` script:

     .. code-block:: bash

        sudo nano S0002-P0001.qcow2-vnc.sh

3. **Understand the Script Components**:
   - The script typically starts with a shebang (`#!/bin/bash`) followed by function definitions and variable assignments. For example, `find_next_available` is a function to find the next available network interface.
   - The script then sets up various QEMU parameters for the virtual machine, such as memory allocation (`-m 2048`), drive files, display settings (`-display vnc=0.0.0.0:$1,websocket=$2`), and network configurations.

4. **Edit the Configuration**:
   - Make the necessary changes to the script. You might want to adjust memory allocation, network settings, or add/remove hardware devices.
   - Be cautious with changes, as incorrect configurations can lead to VMs not functioning as expected.

5. **Save and Exit**:
   - After making your changes, save the file and exit the text editor.

6. **Test the Changes**:
   - To test your changes, you can manually run the script or use the web interface/Autopsy ForensicVM plugin to launch the VM.
   - Ensure that the VM behaves as expected with the new configuration.

By following these steps, you can customize the configuration of individual forensic virtual machines in `forensicVM`. This allows for tailored setups that meet specific investigative requirements or performance optimizations.


Adding an Extra Disk to a ForensicVM Virtual Machine
****************************************************

.. _adding-extra-disk-forensicvm-vm:

To enhance the storage capabilities of a forensic virtual machine in `forensicVM`, you can add an extra disk by modifying the QEMU launch script. This involves adding another `-drive` option to the script. Here's how to do it:

1. **Locate and Open the VM Configuration Script**:
   - Navigate to the directory containing the VM's configuration script. For example:

     .. code-block:: bash

        cd /forensicVM/mnt/vm/d30c9683-fbe7-5f36-985d-d48ba9dbee5e

   - Open the script for editing, such as `S0002-P0001.qcow2-vnc.sh`:

     .. code-block:: bash

        sudo nano S0002-P0001.qcow2-vnc.sh

2. **Identify the Current Disk Configuration**:
   - In the script, locate the existing `-drive` options. These lines define the current disks attached to the VM. For example:

     .. code-block:: none

        -drive file=/forensicVM/mnt/vm/d30c9683-fbe7-5f36-985d-d48ba9dbee5e/S0002-P0001.qcow2-sda,format=qcow2,if=virtio,index=0,media=disk

3. **Add a New `-drive` Option for the Extra Disk**:
   - Add a new line with the `-drive` option to define the extra disk. Specify the file path for the new disk image, the format (typically `qcow2`), and other relevant parameters. For example:

     .. code-block:: none

        -drive file=/path/to/your/new/disk-image.qcow2,format=qcow2,if=virtio,index=2,media=disk

   - Ensure that the `index` value is unique and not used by other drives.

4. **Save and Exit the Editor**:
   - After adding the new `-drive` line, save the changes and exit the text editor.

5. **Test the Configuration**:
   - Start the VM using the modified script or through the web interface/Autopsy ForensicVM plugin to ensure the new disk is correctly attached and recognized by the VM.

By following these steps, you can successfully add an extra disk to a forensic virtual machine in `forensicVM`. 


Index
-----

.. _index:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
