Setup Development Environment
=============================

.. _development-environment-setup:

Setting up your development environment for the ForensicVM server involves forking the repository, cloning your fork, and preparing your local environment for development. This section guides you through these steps.

1. **Fork the Repository**:
   - Visit the `forensicVM` repository on GitHub: https://github.com/nunomourinho/forensicVM
   - Click on the "Fork" button at the top right corner to create a fork of the repository under your GitHub account.

2. **Clone Your Fork**:
   - Clone your forked repository to your local machine using Git. Replace `your-username` with your GitHub username:

     .. code-block:: bash

        git clone https://github.com/your-username/forensicVM.git

3. **Navigate to the Repository Directory**:
   - Change to the directory where the repository has been cloned:

     .. code-block:: bash

        cd forensicVM

4. **Install Dependencies**:
   - Run the `install.sh` script located in the `setup` directory to install all necessary dependencies:

     .. code-block:: bash

        sudo ./setup/install.sh

5. **Activate the Python Virtual Environment**:
   - Activate the Python virtual environment for a contained development environment:

     .. code-block:: bash

        source env_linux/bin/activate

6. **Database Setup**:
   - Initialize and migrate the database as per the instructions in the `admin.rst` document.

7. **Run Development Server**:
   - Start the Django development server for testing:

     .. code-block:: bash

        python manage.py runserver

8. **Deactivate the Virtual Environment** (Optional):
   - Deactivate the virtual environment when done:

     .. code-block:: bash

        deactivate

9. **Proposing Changes**:
   - After making changes or adding new features, commit your changes to your fork.
   - Push the changes to your GitHub fork.
   - Create a pull request from your fork to the original `forensicVM` repository.
   - Provide a clear description of your changes and why they are beneficial.
   - Wait for the repository maintainers to review your pull request. They may request changes or additional information.

By following these steps, you will set up a development environment that allows you to contribute effectively to the ForensicVM project. Remember to keep your fork synchronized with the original repository to incorporate any updates or changes.
