# UserApp developed in
      Django
      Django Rest Framework
      MySQL
      Git
      
# Requirements:
    Python version >= 3.8
    Python Virtualenv
    Django version >= 3.1 (Django will installed using virtualenv)
    MySQL
    Nodejs version >= 8.0
    
# Installation
    Clone the repository
    Run command python -m venv env
    On Windows run .\env\Scripts\activate. On Unix based OS run source env/bin/activate
    Run pip install -r requirements.txt to install the packages
    Run npm install and bower install
    Create a database
    Copy the contents of user_app/.env.example to user_app/.env and modify user_app/.env as necessary
    Now you need to migrate the database by "python manage.py migrate"
    Run python manage.py runserver to run the server.
    Finally, visit with localhost:8000 in your browser and localhost:8000/api also for getting the api.
