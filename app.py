# -*- coding: utf-8 -*-

from os import getenv

# import requests
from forms import *

from flask import Flask, render_template, url_for, request, redirect

from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData, Table, Column, Numeric, Integer, VARCHAR
from sqlalchemy.engine import result, Engine

from wtforms import Form, BooleanField, StringField, validators, EmailField

# from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["DEBUG"] = getenv("FLASK_ENV")
app.config["FLASK_APP"] = getenv("FLASK_APP")
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "mysql+pymysql://root:@localhost:3306/votr_flask"
# mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]


# FLASK_APP=app.py
# FLASK_ENV=development
# FLASK_DEBUG=1
# SECRET_KEY = secret-key-for-dev-only
# CSRF_ENABLED = True
# app.debug = True
# app.config.update(
#     DEBUG=True, SECRET_KEY="secret-key-for-development-only", CSRF_ENABLED=True
# )
# app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# db = SQLAlchemy(app)

# from models import *


# establish connections
db_engine = create_engine("mysql+pymysql://root:@localhost:3306/votr_flask", echo=True)


@app.route("/")
def home():
    """Home page."""
    # return "HI"
    return render_template("home.html")


@app.route("/about")
def about():
    """About page."""
    return render_template("about.html")


@app.route("/darkly_reference")
def darkly_reference():
    """Darkly theme reference."""
    return render_template("darkly_reference.html")


class AddNewUserForm(Form):
    username = StringField("username", [validators.Length(min=1, max=254)])
    email_address = EmailField("email_address", [validators.Length(min=6, max=254)])
    site_permissions_guest = BooleanField("site_permisions_guest", default="checked")
    site_permissions_user = BooleanField("site_permisions_user")
    site_permissions_admin = BooleanField("site_permisions_admin")
    site_permissions_superadmin = BooleanField("site_permisions_superadmin")


@app.route("/users", methods=["GET", "POST"])
def users():
    """Users CRUD page"""
    # create_user_form = CreateUserForm(request.form)
    if request.method == "GET":

        # TODO: Separate this out into another function
        # get all users
        connection = db_engine.connect()
        users_query = "SELECT * FROM Users"
        all_users = connection.execute(users_query).fetchall()
        connection.close()

        # add new user form
        add_new_user_form = AddNewUserForm(request.form)

        return render_template(
            "users.html", all_users=all_users, add_new_user_form=add_new_user_form
        )
    elif request.method == "POST":

        if True:
            # flash("Created new user!", "success")
            return redirect(url_for("users"))
        # if create_user_form.validate_on_submit():
        #     User.create(
        #         username=create_user_form.username.data,
        #         email=create_user_form.email.data,
        #         password=create_user_form.password.data,
        #         active=create_user_form,
        #     )
        #     flash("Created new user!", "success")
        #     return redirect(url_for("public.users"))
        else:
            flash_errors(create_user_form)
            return redirect(url_for("public.users"))
    # return render_template("users.html", create_user_form=create_user_form)


# @blueprint.route("/register/", methods=["GET", "POST"])
# def register():
#     """Register new user."""
#     form = RegisterForm(request.form)
#     if form.validate_on_submit():
#         User.create(
#             username=form.username.data,
#             email=form.email.data,
#             password=form.password.data,
#             active=True,
#         )
#         flash("Thank you for registering. You can now log in.", "success")
#         return redirect(url_for("public.home"))
#     else:
#         flash_errors(form)
#     return render_template("public/register.html", form=form)


@app.route("/polls/")
def polls():
    """Polls CRUD page."""
    return render_template("polls.html")


@app.route("/votes/")
def votes():
    """Votes CRUD page."""
    return render_template("votes.html")


@app.route("/payments/")
def payments():
    """Payments CRUD page."""
    return render_template("payments.html")


@app.route("/user_poll_settings/")
def user_poll_settings():
    """User_Poll_Settings CRUD page."""
    return render_template("user_poll_settings.html")


@app.route("/test_db/")
def test_db():
    """Database test page."""
    # reflect = db.reflect()

    connection = db_engine.connect()
    users_query = "SELECT * FROM Users"
    result = connection.execute(users_query).fetchall()

    return render_template("test_db.html", result=result)


if __name__ == "__main__":
    # port = int(getenv("PORT"), 8000)
    # app.run(port = 2386)
    app.run()
