# kyberfailapp

This is the repository of a [Django](https://www.djangoproject.com/) web app for the [Cybersecurity base project I](https://cybersecuritybase.mooc.fi/module-3.1). 
The app is internally named "Doctor's notes" and has patient and doctor roles for users as well as adding, removing and viewing of doctor's notes. Doctors can write, view and remove notes in addition to viewing patients.

The repository is in two branches: the `main` branch has five security flaws that are implemented on purpose as per the project assignment and the `working` branch that has fixes to those security flaws. Working branch can be found [here](https://github.com/NuiS4ncE/kyberfailapp/tree/working). The report can be read from the [report.md](./docs/report.md) file.

## Setup guide

The app has been configured to be used with [Docker](https://www.docker.com/) as an extra exercise, but can be ran regularly with Django commands. 

### Django setup

1. Install Python 3.10.12 or later.
You can check your Python version by writing `python -V` into the Terminal on Linux or PowerShell on Windows. *Note: Sometimes the Python command might be defined as `python3`.*
2. Make sure pip is installed with `python -m pip -V`
3. Install Django with `python -m pip install Django`
4. Migrate databases by: 
- First run `python manage.py makemigrations`
- Then run `python manage.py migrate`
5. Then start the app with `python manage.py runserver`

The app runs in the local address of `127.0.0.1:8000`.

### Docker setup 

1. [Download Docker](https://docs.docker.com/get-docker/).
2. Build and run the app with `docker-compose up`

The app runs in the local address of `0.0.0.0:8000`.

__*Note: Building and running the app with Docker might lock the SQLite database to a read-only status, so that running the app straight from the Terminal or PowerShell afterwards doesn't work. 
Remember to remove the `db.sqlite3`. Then run `python manage.py makemigrations` and `python manage.py migrate` to remigrate the database before running `python manage.py runserver`.*__