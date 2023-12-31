Setup Development Environment
*****************************

.. _development-environment-setup:

The development environment for the ForensicVM server is similar to the setup of the actual server. This section will guide you through the process of setting up your development environment, ensuring you have all the necessary tools and dependencies.

1. **Operating System**:
   - Use a Debian-based Linux distribution, preferably Debian 11, for compatibility with the ForensicVM server.

2. **Clone the Repository**:
   - Clone the `forensicVM` repository to your local machine using Git:

     .. code-block:: bash

        git clone https://github.com/nunomourinho/forensicVM.git

3. **Navigate to the Repository Directory**:
   - Change to the directory where the repository has been cloned:

     .. code-block:: bash

        cd forensicVM

4. **Install Dependencies**:
   - Run the `install.sh` script located in the `setup` directory. This script will install all the necessary Python packages and system dependencies:

     .. code-block:: bash

        sudo ./setup/install.sh

   - The script installs dependencies listed in `requirements.txt` and `installed_packages.txt`.

5. **Activate the Python Virtual Environment**:
   - Before starting development, activate the Python virtual environment:

     .. code-block:: bash

        source env_linux/bin/activate

6. **Database Setup**:
   - Set up the database required by the Django application. Follow the instructions in the `admin.rst` document for database initialization and migrations.

7. **Run Development Server**:
   - Start the Django development server to test and develop features:

     .. code-block:: bash

        python manage.py runserver

   - Access the server at `http://localhost:8000` to verify it's running correctly.

8. **Deactivate the Virtual Environment** (Optional):
   - Once you're done with development work, you can deactivate the virtual environment:

     .. code-block:: bash

        deactivate

By following these steps, you will have a fully functional development environment for the ForensicVM server. This environment mirrors the actual server setup, allowing you to develop, test, and contribute effectively.
