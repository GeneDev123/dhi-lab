# dhi-lab
A medical chatbot web application capable of giving possible diagnosis based on both personal info and inquiries.

Setup notes:
- Open a terminal in the main directory and type "pip install pipenv" to install the package management ecosystem.
    - Take note that you must first install Python 3.10.0 and PIP must be added to the path.
    - To check if it is added, open a command prompt then type python, if it is not recognizable, google how to setup the path
    - Do the same for pip
- type "pipenv shell" to generate the environment
- type "pipenv install" to update the dependencies depending on the current pipfile.lock files
- go to the folder dhiLab by typing "cd dhiLab"
- Run the command "python manage.py runserver"