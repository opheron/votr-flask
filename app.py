# -*- coding: utf-8 -*-

import logging

from os import getenv

# import requests
from forms import *

from flask import Flask, render_template, url_for, request, redirect, jsonify

from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData, Table, Column, Numeric, Integer, VARCHAR
from sqlalchemy.engine import result, Engine

from flask_wtf import FlaskForm

from wtforms import (
    Form,
    BooleanField,
    StringField,
    validators,
    EmailField,
    DecimalField,
)

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


# TODO: update addNewPollForm to work,
class AddNewPollForm(Form):
    poll_title = StringField(
        "poll title",
        [validators.Length(min=1, max=254)],
        render_kw={"class": "mb-3 form-control"},
    )
    poll_type = EmailField(  # this is a enum of type: enum('single_transferable', 'popular', 'ranked_choice')
        "poll type",
        [validators.Length(min=6, max=254)],
        render_kw={"class": "form-control"},
    )
    poll_voting_choices = BooleanField(  # this is a json array of format JSON_ARRAY('lima','fava','pinto')
        id="site_permissions_guest",
        name="guest",
        label="guest",
        default="checked",
        render_kw={"class": "form-check-input"},
    )


# TODO: update addNewVoteForm to work,
class AddNewVoteForm(Form):
    poll_id = (
        SelectField(  # this is a to be dynamically updated select feild of poll_id's
            "poll id",
            [validators.Length(min=1, max=254)],
            render_kw={"class": "mb-3 form-control"},
        )
    )
    user_id = (
        SelectField(  # this is a to be dynamically updated select feild of user_id's
            "user id",
            [validators.Length(min=6, max=254)],
            render_kw={"class": "form-control"},
        )
    )
    vote_values = BooleanField(  # this is a json object of form JSON_OBJECT('andrew chong', 1, 'sebastian allen', 0)
        id="vote_values",
    )


class AddNewUserForm(FlaskForm):
    username = StringField(
        "username",
        [validators.Length(min=1, max=254)],
        render_kw={"class": "form-control"},
    )
    email_address = EmailField(
        "email_address",
        [validators.Length(min=6, max=254)],
        render_kw={"class": "form-control"},
    )
    site_permissions_guest = BooleanField(
        id="site_permissions_guest",
        name="guest",
        label="guest",
        default="checked",
        render_kw={"class": "form-check-input"},
    )
    site_permissions_user = BooleanField(
        id="site_permissions_user", name="user", label="user"
    )
    site_permissions_admin = BooleanField(
        id="site_permissions_admin",
        name="admin",
        label="admin",
    )
    site_permissions_superadmin = BooleanField(
        id="site_permissions_superadmin",
        name="superadmin",
        label="superadmin",
        default="checked",
    )


class AddNewPaymentForm(FlaskForm):
    # TODO: get user_id dynamically updating, update validator for amount_usd (not negative?)
    user_id = SelectField("user_id", coerce=int)
    amount_usd = DecimalField("amount_usd", places=2)
    payment_purposes_test = BooleanField("test", default="checked")
    payment_purposes_free_trial = BooleanField("free trial")
    payment_purposes_subscription = BooleanField("subscription")
    payment_purposes_donation = BooleanField("donation")


class AddNewUserPollSettingForm(FlaskForm):
    # TODO: Validation, actual functionality
    user_poll_setting_id = StringField("user_poll_setting_id")
    user_id = StringField("user_id")
    poll_id = BooleanField("poll_id")
    user_permissions_collaborator = BooleanField("collaborator")
    user_permissions_poll_creator = BooleanField("poll creator")
    user_permissions_admin = BooleanField("admin")
    user_permissions_superadmin = BooleanField("superadmin")


@app.route("/users", methods=["GET", "POST"])
def users():
    """Users CRUD page"""
    # create_user_form = CreateUserForm(request.form)
    if request.method == "GET":

        # TODO: Separate this out into another function
        # get all users

        # with engine.connect() as connection:
        # result = connection.execute(text("select username from users"))
        # for row in result:
        #     print("username:", row['username'])
        connection = db_engine.connect()
        users_query = "SELECT * FROM Users"
        all_users = connection.execute(users_query).fetchall()
        connection.close()

        # add new user form
        add_new_user_form = AddNewUserForm()

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


@app.route("/add_new_user", methods=["POST"])
def add_new_user():
    # if request.method == "POST" and "add-new-user" in request.form:
    add_new_user_form = AddNewUserForm()
    # NOTE: Use the next line if you need to test w/out form validation stopping
    # if request.method == "POST":
    if add_new_user_form.validate_on_submit():
        connection = db_engine.connect()
        new_user = {
            "username": add_new_user_form.username.data,
            "email_address": add_new_user_form.email_address.data,
        }

        # Permissions are tricky because of the sql string has to be exact with punctuation like commas and quotes
        new_user_site_permissions_set = (
            add_new_user_form.site_permissions_guest.data,
            add_new_user_form.site_permissions_user.data,
            add_new_user_form.site_permissions_admin.data,
            add_new_user_form.site_permissions_superadmin.data,
        )
        new_user[
            "site_permissions_guest"
        ] = add_new_user_form.site_permissions_guest.data
        new_user["site_permissions_user"] = add_new_user_form.site_permissions_user.data
        new_user[
            "site_permissions_admin"
        ] = add_new_user_form.site_permissions_admin.data
        new_user[
            "site_permissions_superadmin"
        ] = add_new_user_form.site_permissions_superadmin.data

        # Need to make a single proper sql string for site_permissions

        site_permissions_set = ("guest", "user", "admin", "superadmin")
        new_user_sqlstr_site_permissions = ""
        new_user_permissions_indices = list(
            filter(
                lambda x: new_user_site_permissions_set[x] == True,
                range(len(new_user_site_permissions_set)),
            )
        )
        app.logger.debug(
            f"new_user_permissions_indices: {new_user_permissions_indices}"
        )
        new_user_sqlstr_site_permissions = ""
        match new_user_site_permissions_set.count(True):
            case 0:
                pass
            case 1:
                new_user_sqlstr_site_permissions = (
                    f"{site_permissions_set[new_user_site_permissions_set.index(True)]}"
                )
            case 2:
                new_user_sqlstr_site_permissions = (
                    f"{site_permissions_set[new_user_permissions_indices[0]]},"
                    f"{site_permissions_set[new_user_permissions_indices[1]]}"
                )
            case 3:
                new_user_sqlstr_site_permissions = (
                    f"{site_permissions_set[new_user_permissions_indices[0]]},"
                    f"{site_permissions_set[new_user_permissions_indices[1]]},"
                    f"{site_permissions_set[new_user_permissions_indices[2]]}"
                )
            case 4:
                new_user_sqlstr_site_permissions = "guest,user,admin,superadmin"

            # Default case should never occur
            case _:
                app.logger.warn(f"Default case for site permissions bug!")
                app.logger.debug(f"new_user_sqlstr_site_permissions")
                connection.close()
                return redirect(url_for("users"))

        app.logger.debug(f"{new_user['site_permissions_guest']}")
        app.logger.debug(f"{new_user['site_permissions_user']}")
        app.logger.debug(f"{new_user['site_permissions_admin']}")
        app.logger.debug(f"{new_user['site_permissions_superadmin']}")
        app.logger.debug(
            f"new_user_sqlstr_site_permissions: {new_user_sqlstr_site_permissions}"
        )
        app.logger.debug(f"new_user: {new_user}")
        add_new_user_query = f"INSERT INTO Users (username, email_address, site_permissions) VALUES ('{new_user['username']}', '{new_user['email_address']}', '{new_user_sqlstr_site_permissions}')"
        app.logger.debug(add_new_user_query)
        connection.execute(add_new_user_query)
        connection.close()
        return redirect(url_for("users"))
    else:
        return redirect(url_for("users"))


def get_user_data_by_id(user_id):
    """Get user data from db and return data as a dictionary"""
    with db_engine.connect() as connection:
        find_user_by_id_query = f"SELECT * FROM Users WHERE user_id = {user_id}"
        find_user_by_id_query_result = connection.execute(
            find_user_by_id_query
        ).fetchone()
        app.logger.debug(find_user_by_id_query_result)
        # user_data = dict(
        #     zip(
        #         [
        #             "user_id",
        #             "username",
        #             "email",
        #         ],
        #         find_user_by_id_query_result[0, 3],
        #     )
        # )
        # user_data["site_permissions"] = {find_user_by_id_query_result.split(",")}
        # return user_data
        user_data = dict(find_user_by_id_query_result)
        user_data["site_permissions"] = user_data["site_permissions"].split(",")
        app.logger.debug(user_data)

        return user_data


@app.route("/find_user_by_id", methods=["POST"])
def find_user_by_id():
    """Select user by ID"""
    if request.method == "POST":
        app.logger.debug(request.form)
        user_id = request.form["users-find-by-id-id"]

        # params = request.get_json()
        # app.logger.debug(f"params: {params}")
        # app.logger.debug(f"user_id: {user_id}")

        # user_data = {result.meta_key: result.metag_value for result in results}

        user_data = get_user_data_by_id(user_id)
        app.logger.debug(user_data)
        # user_data_dict = {kvp.meta_key: kvp.meta_value for kvp in user_data}
        # user_data_dict = {user_id: user_id, username: username}

        return jsonify(user_data)
    else:
        return redirect(url_for("users"))


#  add_new_user_form = AddNewUserForm()
#     # NOTE: Use the next line if you need to test w/out form validation stopping
#     # if request.method == "POST":
#     if add_new_user_form.validate_on_submit():
#         connection = db_engine.connect()
#         new_user = {
#             "username": add_new_user_form.username.data,
#             "email_address": add_new_user_form.email_address.data,
#         }

# # ###################

#         # Permissions are tricky because of the sql string has to be exact with punctuation like commas and quotes
#         new_user_site_permissions_set = (
#             add_new_user_form.site_permissions_guest.data,
#             add_new_user_form.site_permissions_user.data,
#             add_new_user_form.site_permissions_admin.data,
#             add_new_user_form.site_permissions_superadmin.data,
#         )
#         new_user[
#             "site_permissions_guest"
#         ] = add_new_user_form.site_permissions_guest.data
#         new_user["site_permissions_user"] = add_new_user_form.site_permissions_user.data
#         new_user[
#             "site_permissions_admin"
#         ] = add_new_user_form.site_permissions_admin.data
#         new_user[
#             "site_permissions_superadmin"
#         ] = add_new_user_form.site_permissions_superadmin.data

#         # Need to make a single proper sql string for site_permissions

#         site_permissions_set = ("guest", "user", "admin", "superadmin")
#         new_user_sqlstr_site_permissions = ""
#         new_user_permissions_indices = list(
#             filter(
#                 lambda x: new_user_site_permissions_set[x] == True,
#                 range(len(new_user_site_permissions_set)),
#             )
#         )
#         app.logger.debug(
#             f"new_user_permissions_indices: {new_user_permissions_indices}"
#         )

#         connection = db_engine.connect()
# users_query = "SELECT * FROM Users"
# all_users = connection.execute(users_query).fetchall()
# connection.close()


@app.route("/polls/", methods=["GET", "POST"])
def polls():
    """Polls CRUD page"""
    # create_poll_form = CreatePollForm(request.form)
    if request.method == "GET":

        # get all Polls
        connection = db_engine.connect()
        polls_query = "SELECT * FROM Polls"
        all_polls = connection.execute(polls_query).fetchall()
        connection.close()

        # add new poll form
        add_new_poll_form = AddNewPollForm(request.form)

        return render_template(
            "polls.html", all_polls=all_polls, add_new_poll_form=add_new_poll_form
        )
    elif request.method == "POST":
        # TODO: get forms working
        if True:
            # flash("Created new poll!", "success")
            return redirect(url_for("polls"))
        else:
            flash_errors(create_user_form)
            return redirect(url_for("public.users"))
    # return render_template("users.html", create_user_form=create_user_form)


# @app.route("/votes/")
# def votes():
#     """Votes CRUD page."""
#     return render_template("votes.html")


@app.route("/votes/", methods=["GET", "POST"])
def votes():
    """Votes CRUD page"""
    # create_vote_form = CreateVoteForm(request.form)
    if request.method == "GET":

        # get all Votes
        connection = db_engine.connect()
        votes_query = "SELECT * FROM Votes"
        all_votes = connection.execute(votes_query).fetchall()
        connection.close()

        # add new vote form
        add_new_vote_form = AddNewVoteForm(request.form)

        return render_template(
            "votes.html", all_votes=all_votes, add_new_vote_form=add_new_vote_form
        )
    elif request.method == "POST":
        # TODO: get forms working
        if True:
            # flash("Created new vote!", "success")
            return redirect(url_for("votes"))
        else:
            flash_errors(create_user_form)
            return redirect(url_for("public.users"))
    # return render_template("users.html", create_user_form=create_user_form)


# TODO: delete
# @app.route("/payments/")
# def payments():
#     """Payments CRUD page."""
#     return render_template("payments.html")


@app.route("/payments/", methods=["GET", "POST"])
def payments():
    """Payments CRUD page"""
    # add_new_payment_form = CreatepPymentForm(request.form) ----
    if request.method == "GET":
        connection = db_engine.connect()
        payments_query = "SELECT * FROM Payments"
        all_payments = connection.execute(payments_query).fetchall()
        connection.close()

        # TODO: add new ptayment form - not working yet, the select list is not dynamic
        add_new_payment_form = AddNewPaymentForm(request.form)

        return render_template(
            "payments.html",
            all_payments=all_payments,
            add_new_payment_form=add_new_payment_form,
        )
    elif request.method == "POST":
        # TODO: also not working yet, dont know where to start
        if True:
            # flash("Created new user!", "success")
            return redirect(url_for("payments"))
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
            flash_errors(create_payment_form)
            return redirect(url_for("public.payments"))
    # return render_template("users.html", create_user_form=create_user_form)


# app.route("/user_poll_settings/")
# def user_poll_settings():
#     """User_Poll_Settings CRUD page."""
#     return render_template("user_poll_settings.html")


@app.route("/user_poll_settings/", methods=["GET", "POST"])
def user_poll_settings():
    """User_Poll_Settings CRUD page"""
    # create_user_poll_setting_form = CreateUserPollSettingForm(request.form)
    if request.method == "GET":

        # get all User_Poll_Settings
        connection = db_engine.connect()
        user_poll_settings_query = "SELECT * FROM User_Poll_Settings"
        all_user_poll_settings = connection.execute(user_poll_settings_query).fetchall()
        connection.close()

        # add new user_poll_setting form
        add_new_user_poll_setting_form = AddNewUserPollSettingForm(request.form)

        return render_template(
            "user_poll_settings.html",
            all_user_poll_settings=all_user_poll_settings,
            add_new_user_poll_setting_form=add_new_user_poll_setting_form,
        )
    elif request.method == "POST":
        # TODO: get forms working
        if True:
            # flash("Created new user_poll_setting!", "success")
            return redirect(url_for("user_poll_settings"))
        else:
            flash_errors(create_user_form)
            return redirect(url_for("public.users"))
    # return render_template("users.html", create_user_form=create_user_form)


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
