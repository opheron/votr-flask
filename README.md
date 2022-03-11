# votr-flask

An example CRUD SQL voting web app built with Flask

## Dev Environment Setup

1. Install pyenv if not installed: https://github.com/pyenv/pyenv
2. Install Python version 3.10.2:

```zsh
pyenv version 3.10.2
pyenv local 3.10.2
```

3. Install Poetry: https://python-poetry.org/docs/#installation

Do:

```zsh
poetry install
```

4. Set Flask variables:

```zsh
export FLASK_ENV=development
export FLASK_DEBUG=1

```

### Running locally

Run the following commands to bootstrap your environment if you are unable to run the application using Docker

```bash
cd votr-flask
pip install -r requirements/dev.txt
```

#### Database Initialization (locally)

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration

```bash
flask db init
flask db migrate
flask db upgrade
```

## Deployment to Heroku with new dev changes

Update the lockfile with:

```zsh
poetry lock --no-update
```

Freeze requirements with:

```zsh
poetry export -f requirements.txt --output requirements.txt
```

## Shell

To open the interactive shell, run

```bash
docker-compose run --rm manage db shell
flask shell # If running locally without Docker
```

By default, you will have access to the flask `app`.

## Running Tests/Linter

To run all tests, run

```bash
docker-compose run --rm manage test
flask test # If running locally without Docker
```

To run the linter, run

```bash
docker-compose run --rm manage lint
flask lint # If running locally without Docker
```

The `lint` command will attempt to fix any linting/style errors in the code. If you only want to know if the code will pass CI and do not wish for the linter to make changes, add the `--check` argument.

## Migrations

Whenever a database migration needs to be made. Run the following commands

```bash
docker-compose run --rm manage db migrate
flask db migrate # If running locally without Docker
```

This will generate a new migration script. Then run

```bash
docker-compose run --rm manage db upgrade
flask db upgrade # If running locally without Docker
```

To apply the migration.

For a full migration command reference, run `docker-compose run --rm manage db --help`.

If you will deploy your application remotely (e.g on Heroku) you should add the `migrations` folder to version control.
You can do this after `flask db migrate` by running the following commands

```bash
git add migrations/*
git commit -m "Add migrations"
```

Make sure folder `migrations/versions` is not empty.

## Asset Management

Files placed inside the `assets` directory and its subdirectories
(excluding `js` and `css`) will be copied by webpack's
`file-loader` into the `static/build` directory. In production, the plugin
`Flask-Static-Digest` zips the webpack content and tags them with a MD5 hash.
As a result, you must use the `static_url_for` function when including static content,
as it resolves the correct file name, including the MD5 hash.
For example

```html
<link
  rel="shortcut icon"
  href="{{static_url_for('static', filename='build/img/favicon.ico') }}"
/>
```

If all of your static files are managed this way, then their filenames will change whenever their
contents do, and you can ask Flask to tell web browsers that they
should cache all your assets forever by including the following line
in `.env`:

```text
SEND_FILE_MAX_AGE_DEFAULT=31556926  # one year
```

## Documentation References

- WTForms: https://wtforms.readthedocs.io/en/3.0.x/
- Jinja2: https://jinja2docs.readthedocs.io/en/stable/
