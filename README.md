# Dr's Lab
Update: January 27, 2023

A medical chatbot web application capable of giving possible diagnosis based on both personal info and inquiries.

Requirements:
- Python 3.10
- Make sure Python and pip is recognized in the terminal:
    - Open cmd in start
    - type "python"
    - type "pip"
    - Make sure both is recognized, if not, Google how to add them in the environment variables

Setup / Installation:
- Download the latest project branch from Github
- Open in a text editor (VScode recommended)
- Open a new command prompt or shell terminal in VSCode
- Type "pip install pipenv", inside the main project directory (where pipfile.lock is located), pipenv is the package and environment manager.
- Type "pipenv install", this will read the pipfile.lock and install the required dependencies. Note: This may take a while.
- Type "pipenv shell" to activate the environment 
- Type "cd dhiLab" to proceed to the dhilab folder where "manage.py" file is located
- Type "python manage.py runserver" to activate the server. This will provide a localhost link which indicates that the application is installed correctly.

Database Setup:
- Complete the installation step
- In the directory where manage.py is located, type "python manage.py makemigrations". This will set the database architecture of the application (SQLite3)
- Type "python manage.py migrate" to apply the architecture and build the initial database. 
- Create an Admin user by typing "python manage.py createsuperuser". Follow the terminal instructions after. 
- Recommended credentials to input for the admin for simplicity
    - User name: admin
    - User email: admin@gmail.com
    - Password: testing321

Tips and notes:
- Always type "ls" to output the current directory of the terminal before you execute a command.
- Make sure you have sufficient storage for the application. Atleast 10Gb is recommended

Deployment details:
- The application is deployed in Pythonanywhere which provides deployment for Django application 
- Uses the free tier subscription where it only allows 500mb storage for the application.
- Does not use a virtual environment and only installed minor packages as Pythonanywhere already provides major packages (ex. NLTK, Tensorflow, Sckitlearn etc.)
- Account details can be requested from the developer

Relevant urls:
Deployed Site: https://drslab2.pythonanywhere.com/
Admin Page: https://drslab2.pythonanywhere.com/admin
Access Log: drslab2.pythonanywhere.com.access.log
Error log: drslab2.pythonanywhere.com.error.log
Server Log: drslab2.pythonanywhere.com.server.log
