# votr-flask

An educational demonstration CRUD SQL voting web app built with [Flask]

## About

votr-flask demonstrates using [Flask] and [MySQL] to make a database management app. It is made for educational purposes only, and is not intended to exemplify production-ready software. Specifically, app.py contains nearly all the back-end logic for this application for ease of reading.

## Dev Environment Setup

After you have cloned this repo to your local environment, do the following:

1. Install pyenv if not installed: [pyenv][https://github.com/pyenv/pyenv]

2. Install Python version 3.10.2 and use it:

```zsh
pyenv version 3.10.2
pyenv local 3.10.2
```

3. Install [Poetry] for Python dependency management

4. Install Python dependencies

Do:

```zsh
poetry install
```

5. Set Flask variables:

```zsh
export FLASK_ENV=development
export FLASK_DEBUG=1
```

6. Set up database:

Install MySQL: https://dev.mysql.com/

Create a MySQL user:

- username: root
- password: _no password_

Create a MySQL database with the following parameters:

- port: 3306
- database name: votr_flask

Run set_up_db.sql to create the necessary tables and add sample data.

### Running locally

Do:

````zsh
poetry shell
python app.py
```

You should see the following in your terminal:
```
 * Serving Flask app 'app' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 126-263-310
```

Navigate to the URL provided and you should see the app home page.

## Deployment to Heroku with new dev changes

Update the lockfile with:

```zsh
poetry lock --no-update
````

Freeze requirements with:

```zsh
poetry export -f requirements.txt --output requirements.txt
```

Test the Heroku deploy locally with:

```zsh
heroku local
```

Then do:

```zsh
git push heroku main
```

## Open Source Credits & Acknowledgements

Thanks to all the open source projects that are used as primary dependencies in this project, including:

### Python

- [Flask][https://flask.palletsprojects.com/]
- [Poetry][https://python-poetry.org/docs/#installation]
- [WTForms][https://wtforms.readthedocs.io/en/3.0.x/]
- [Flask-WTF][https://flask-wtf.readthedocs.io/]
- [Jinja2][https://jinja2docs.readthedocs.io/en/stable/]
- [python-dotenv][https://saurabh-kumar.com/python-dotenv/]

### Database & SQL

- [MySQL][https://www.mysql.com/]
- [Flask-SqlAlchemy][https://flask-sqlalchemy.palletsprojects.com/]
- [PyMySQL][https://pymysql.readthedocs.io/en/latest/]

### Javascript

- [List.js][https://listjs.com/]
- [jQuery][https://jquery.com/]

### HTML & CSS Styling

- [Bootswatch][https://bootswatch.com/] - Darkly Theme

### Production Web Server

- [Gunicorn][https://gunicorn.org/]
