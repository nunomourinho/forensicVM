.. _ForensicVM-folder-structure:

ForensicVM Folder Structure
===========================

The ``/ForensicVM`` directory in Debian 11 encompasses a structured organization of folders that facilitate the ForensicVM project's workflow. Each folder within this directory serves a specific purpose, as elaborated below:

``bin``
-------
This folder is the designated location for **bash scripts** and **external executable files**. Any shell script or binary that the ForensicVM project requires for its functioning is placed here.

Inside the bin folder, there are two main scripts:

``run-or-convert.sh``: This script is dedicated to either running a preexisting forensic image created by snapshotting the original forensic image, or converting a remote, reverse SSH Samba share-based image.

.. image:: run-or-convert.svg
   :alt: Run or convert a forensic image
   :width: 100%
   :align: center

``forensic.sh``: This script detects the format of the original forensic image, chooses the appropriate conversion tool, and then converts the forensic image into a format suitable for forensicVM.

.. image:: forerensic.sh.svg
   :alt: Detects the forensic image format, chooses the appropriate conversion tool, and converts it to a forensicVM format.
   :width: 100%
   :align: center


``branding``
------------
The **branding** directory holds the official branding elements for the ForensicVM project. This includes **logos** and their **source files**. It ensures easy access and uniformity in branding across the project.

``docs``
-------
The **docs** directory is dedicated to **ReadTheDocs documentation**. It contains detailed information on both the API and server aspects of ForensicVM, providing an extensive reference for users and developers.

``etc``
------
In the **etc** directory, you'll find **configuration files** pertinent to the ForensicVM project. These files hold settings and parameters that influence the behavior of various components.

``main``
-------
This folder houses the **Django application** that powers the ForensicVM project. Django is a high-level Python web framework that allows for rapid development and clean design.

``mnt``
------
The **mnt** folder contains **converted ForensicVM** and **ISO files**. These are typically disk image files or optical disc images that have undergone conversion or processing within the ForensicVM environment.

``plugins``
-----------
**plugins** is a dedicated directory for the community-contributed **plugins project for Autopsy ForensicVM**. These plugins extend the functionality and features of the Autopsy platform within the ForensicVM ecosystem.

``setup``
--------
The **setup** directory is populated with **install helpers** and **setup scripts**. These facilitate the installation and configuration process for users setting up the ForensicVM environment.

``src``
------
This folder, **src**, is where **third-party external source code projects** reside. Any external software or library source code that the ForensicVM project depends on or integrates with can be found here.

``tmp``
------
As the name suggests, the **tmp** directory is a temporary storage location. Any **temporary files** created during the execution or processing by ForensicVM are placed here.

``usr``
------
The **usr** directory contains **helper files** that are intended to be copied over to the system's ``/usr`` directory. This ensures seamless integration and functioning of the ForensicVM project within the Debian environment.

``vmTemplates``
---------------
In the experimental realm, the **vmTemplates** directory holds **templates for forensic images** that don’t possess any partitions. These templates aid in the forensic examination of unique or non-standard disk images.

This structured folder organization ensures efficient workflow, easy maintenance, and clarity in the ForensicVM project's operations.
