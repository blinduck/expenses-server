# Expenses Project Server

This expense tracker allows multiple people who belong to the same household to record their personal and household expenses.
This is the backend, the client can be found <a href="https://github.com/blinduck/expenses-client">here</a>

# Tech
This Django project implements a REST API (with the help of <a href="http://www.django-rest-framework.org/">DRF</a>.



To setup the project:
1. Clone the repo, setup a new Python 3 virtual environment and install dependencies from 'requirements.txt'
2. Create a new database. Postgres is preferred but, MYSQL or SQLite should work just fine as well.
3. Open up settings.py, and change the database settings to reflect your database setup.
4. Run 'python manage.py migrate' to create the required tables
5. Run 'python manage.py runserver' to start the server.

If you have any questions, reach out to me at blinduck@gmail.com


