# -*- coding: utf-8 -*-

from os import getenv

from enum import Enum

from pymysql import NULL

from forms import *

from flask import Flask, render_template, url_for, request, redirect, jsonify

from dotenv import load_dotenv

from sqlalchemy import create_engine

from flask_wtf import FlaskForm

from wtforms import (
    BooleanField,
    StringField,
    validators,
    EmailField,
    DecimalField,
)

load_dotenv()

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["DEBUG"] = getenv("FLASK_ENV")
app.config["FLASK_APP"] = getenv("FLASK_APP")
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


if app.config["DEBUG"] == "production":
    db_engine = create_engine(getenv("DATABASE_URL"), echo=True)
else:
    db_engine = create_engine(
        "mysql+pymysql://root:@localhost:3306/votr_flask", echo=True
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


@app.errorhandler(401)
def page_unauthorized(error):
    return render_template("401.html")


@app.errorhandler(500)
def page_internal_error(error):
    return render_template("500.html")


@app.route("/")
def home():
    """Home page."""
    return render_template("home.html")


class PollTypes(Enum):
    single_transferable = 1
    popular = 2
    ranked_choice = 3


class AddNewPollForm(FlaskForm):
    poll_title = StringField(
        "poll_title",
        [validators.Length(min=1, max=254)],
        render_kw={"class": "form-control"},
    )
    poll_type = SelectField(
        "poll_type",
        choices=[
            (member.value, name.capitalize())
            for name, member in PollTypes.__members__.items()
        ],
        render_kw={"class": "form-control"},
    )
    poll_voting_choices = StringField(
        "poll_voting_choices",
        render_kw={"class": "form-control"},
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
    )


class AddNewPaymentForm(FlaskForm):
    user_id = SelectField(
        "user_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )
    amount_usd = DecimalField(
        "amount_usd",
        places=2,
        render_kw={"class": "form-control"},
    )
    payment_purposes_test = BooleanField(
        id="payment_purposes_test",
        name="test",
        label="test",
        render_kw={"class": "form-check-input"},
    )
    payment_purposes_free_trial = BooleanField(
        id="payment_purposes_free_trial", name="free_trial", label="free trial"
    )
    payment_purposes_subscription = BooleanField(
        id="payment_purposes_subscription",
        name="subscription",
        label="subscription",
    )
    payment_purposes_donation = BooleanField(
        id="payment_purposes_donation",
        name="donation",
        label="donation",
    )


class UpdatePaymentForm(FlaskForm):
    payment_id = SelectField(
        "payment_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )
    user_id = SelectField(
        "user_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )
    amount_usd = DecimalField(
        "amount_usd",
        places=2,
        render_kw={"class": "form-control"},
    )
    payment_purposes_test = BooleanField(
        id="payment_purposes_test",
        name="test",
        label="test",
        render_kw={"class": "form-check-input"},
    )
    payment_purposes_free_trial = BooleanField(
        id="payment_purposes_free_trial", name="free_trial", label="free trial"
    )
    payment_purposes_subscription = BooleanField(
        id="payment_purposes_subscription",
        name="subscription",
        label="subscription",
    )
    payment_purposes_donation = BooleanField(
        id="payment_purposes_donation",
        name="donation",
        label="donation",
    )


class DeletePaymentForm(FlaskForm):
    payment_id = SelectField(
        "payment_id",
        choices=(1, 1),
        coerce=int,
        render_kw={"class": "form-control"},
    )


class AddNewUserPollSettingForm(FlaskForm):
    user_id = SelectField(
        "user_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )
    poll_id = SelectField(
        "poll_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )
    user_permissions_collaborator = BooleanField(
        id="user_permissions_collaborator",
        name="collaborator",
        label="collaborator",
        render_kw={"class": "form-check-input"},
    )
    user_permissions_poll_creator = BooleanField(
        id="user_permissions_poll_creator", name="poll_creator", label="poll creator"
    )
    user_permissions_admin = BooleanField(
        id="user_permissions_admin",
        name="admin",
        label="admin",
    )
    user_permissions_superadmin = BooleanField(
        id="user_permissions_superadmin",
        name="superadmin",
        label="superadmin",
    )


class UpdateUserPollSettingForm(FlaskForm):
    user_poll_setting_id = SelectField(
        "user_poll_setting_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )
    user_id = SelectField(
        "user_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )
    poll_id = SelectField(
        "poll_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )
    user_permissions_collaborator = BooleanField(
        id="user_permissions_collaborator",
        name="collaborator",
        label="collaborator",
        render_kw={"class": "form-check-input"},
    )
    user_permissions_poll_creator = BooleanField(
        id="user_permissions_poll_creator", name="poll_creator", label="poll creator"
    )
    user_permissions_admin = BooleanField(
        id="user_permissions_admin",
        name="admin",
        label="admin",
    )
    user_permissions_superadmin = BooleanField(
        id="user_permissions_superadmin",
        name="superadmin",
        label="superadmin",
    )


class DeleteUserPollSettingForm(FlaskForm):
    user_poll_setting_id = SelectField(
        "user_poll_setting_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )


class AddNewVoteForm(FlaskForm):
    poll_id = SelectField(
        "poll_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )
    user_id = SelectField(
        "user_id",
        coerce=int,
        render_kw={"class": "form-control"},
    )
    vote_values = StringField(
        "vote_values",
        render_kw={"class": "form-control"},
    )


def get_all_users_data():
    """
    Queries database for all users
    Returns data as a list of dictionaries
    """
    with db_engine.connect() as connection:
        users_query = "SELECT * FROM Users"
        all_users = connection.execute(users_query).fetchall()
        all_users = [dict(user) for user in all_users]

        for user in all_users:
            user["site_permissions"] = user["site_permissions"].split(",")

        return all_users


@app.route("/get_all_users", methods=["GET"])
def get_all_users():
    """Route that returns all users as a JSON object"""
    if request.method == "GET":
        all_users = get_all_users_data()
        return jsonify(all_users)
    else:
        return redirect(url_for("users"))


@app.route("/users", methods=["GET"])
def users():
    """Users CRUD page"""
    if request.method == "GET":
        add_new_user_form = AddNewUserForm()

        all_users = get_all_users_data()

        return render_template(
            "users.html", all_users=all_users, add_new_user_form=add_new_user_form
        )
    else:
        return redirect(url_for("users"))


@app.route("/add_new_user", methods=["POST"])
def add_new_user():
    add_new_user_form = AddNewUserForm()
    if add_new_user_form.validate_on_submit() and (
        add_new_user_form.site_permissions_superadmin.data
        or add_new_user_form.site_permissions_admin.data
        or add_new_user_form.site_permissions_user.data
        or add_new_user_form.site_permissions_guest.data
    ):
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

        add_new_user_query = f"INSERT INTO Users (username, email_address, site_permissions) VALUES ('{new_user['username']}', '{new_user['email_address']}', '{new_user_sqlstr_site_permissions}')"
        connection.execute(add_new_user_query)
        connection.close()
        return redirect(url_for("users"))
    else:
        return redirect(url_for("users"))


@app.route("/add_new_poll", methods=["POST"])
def add_new_poll():
    add_new_poll_form = AddNewPollForm()

    # json validation would be done here
    if add_new_poll_form.poll_voting_choices.data != "":
        connection = db_engine.connect()
        new_poll = {
            "poll_title": add_new_poll_form.poll_title.data,
            "poll_type": add_new_poll_form.poll_type.data,
            "poll_voting_choices": add_new_poll_form.poll_voting_choices.data,
        }
        poll_title = new_poll["poll_title"] if new_poll["poll_title"] != "" else "NULL"

        add_new_poll_query = f"INSERT INTO Polls (poll_title, poll_type, poll_voting_choices) VALUES ('{poll_title}', {new_poll['poll_type']}, '{new_poll['poll_voting_choices']}')"
        connection.execute(add_new_poll_query)
        connection.close()
        return redirect(url_for("polls"))
    else:
        return redirect(url_for("polls"))


@app.route("/polls/", methods=["GET", "POST"])
def polls():
    """Polls CRUD page"""
    if request.method == "GET":

        connection = db_engine.connect()
        polls_query = "SELECT * FROM Polls"
        all_polls = connection.execute(polls_query).fetchall()
        connection.close()

        add_new_poll_form = AddNewPollForm(request.form)

        return render_template(
            "polls.html", all_polls=all_polls, add_new_poll_form=add_new_poll_form
        )
    elif request.method == "POST":
        if True:
            return redirect(url_for("polls"))
        else:
            flash_errors(create_user_form)
            return redirect(url_for("public.users"))


@app.route("/add_new_vote", methods=["POST"])
def add_new_vote():
    add_new_vote_form = AddNewVoteForm()

    # minimal validation done here
    if add_new_vote_form.vote_values.data != "":
        connection = db_engine.connect()
        new_vote = {
            "user_id": add_new_vote_form.user_id.data,
            "poll_id": add_new_vote_form.poll_id.data,
            "vote_values": add_new_vote_form.vote_values.data,
        }

        # here we add the new vote to the table
        add_new_vote_query = f"INSERT INTO Votes (user_id, poll_id, vote_values) VALUES ({new_vote['user_id']}, {new_vote['poll_id']}, '{new_vote['vote_values']}')"
        connection.execute(add_new_vote_query)
        connection.close()
        return redirect(url_for("votes"))
    else:
        return redirect(url_for("votes"))


@app.route("/votes/", methods=["GET", "POST"])
def votes():
    if request.method == "GET":
        # fetch all payments and users to populate dynamic lists
        connection = db_engine.connect()
        votes_query = "SELECT * FROM Votes"
        all_votes = connection.execute(votes_query).fetchall()
        users_query = "SELECT * FROM Users"
        all_users = connection.execute(users_query).fetchall()
        polls_query = "SELECT * FROM Polls"
        all_polls = connection.execute(polls_query).fetchall()
        connection.close()

        # payment forms and select field population, users relationship is NULLABLE which has a value of -1; dealt with later
        add_new_vote_form = AddNewVoteForm(request.form)
        add_new_vote_form.user_id.choices = [(g.user_id, g.user_id) for g in all_users]
        add_new_vote_form.poll_id.choices = [(g.poll_id, g.poll_id) for g in all_polls]

        return render_template(
            "votes.html",
            all_votes=all_votes,
            add_new_vote_form=add_new_vote_form,
        )
    elif request.method == "POST":
        return redirect(url_for("votes"))


@app.route("/add_new_payment", methods=["POST"])
def add_new_payment():
    # if request.method == "POST" and "add-new-payment" in request.form:
    add_new_payment_form = AddNewPaymentForm()

    # only validation done is to check if the amount_usd is empty or payment purposes is empty
    if add_new_payment_form.amount_usd.data != None and (
        add_new_payment_form.payment_purposes_test.data
        or add_new_payment_form.payment_purposes_free_trial.data
        or add_new_payment_form.payment_purposes_subscription.data
        or add_new_payment_form.payment_purposes_donation.data
    ):
        connection = db_engine.connect()
        new_payment = {
            "user_id": add_new_payment_form.user_id.data,
            "amount_usd": add_new_payment_form.amount_usd.data,
        }
        user_id = new_payment["user_id"]
        if new_payment["user_id"] == -1:
            user_id = "NULL"

        # here we set up the 'set' in the expected format EX: 'test,free_trial,donation'
        new_payment_purposes_set = (
            add_new_payment_form.payment_purposes_test.data,
            add_new_payment_form.payment_purposes_free_trial.data,
            add_new_payment_form.payment_purposes_subscription.data,
            add_new_payment_form.payment_purposes_donation.data,
        )
        payment_purposes_set = ("test", "free_trial", "subscription", "donation")
        first_true = True
        string = ""
        for x in range(len(new_payment_purposes_set)):
            if new_payment_purposes_set[x]:
                comma = "," if not first_true else ""
                string = f"{string}{comma}{payment_purposes_set[x]}"
                first_true = False

        # here we add the new payment to the table
        add_new_payment_query = f"INSERT INTO Payments (user_id, amount_usd, payment_purposes) VALUES ({user_id}, {new_payment['amount_usd']}, '{string}')"
        connection.execute(add_new_payment_query)
        connection.close()
        return redirect(url_for("payments"))
    else:
        return redirect(url_for("payments"))


@app.route("/update_payment", methods=["POST"])
def update_payment():
    update_payment_form = UpdatePaymentForm()

    # only validation done is to check if the amount_usd is empty or payment perposes is empty
    if update_payment_form.amount_usd.data != None and (
        update_payment_form.payment_purposes_test.data
        or update_payment_form.payment_purposes_free_trial.data
        or update_payment_form.payment_purposes_subscription.data
        or update_payment_form.payment_purposes_donation.data
    ):
        connection = db_engine.connect()
        new_payment = {
            "user_id": update_payment_form.user_id.data,
            "amount_usd": update_payment_form.amount_usd.data,
        }
        user_id = new_payment["user_id"]
        if new_payment["user_id"] == -1:
            user_id = "NULL"

        # here we set up the 'set' in the expected format EX: 'test,free_trial,donation'
        new_payment_purposes_set = (
            update_payment_form.payment_purposes_test.data,
            update_payment_form.payment_purposes_free_trial.data,
            update_payment_form.payment_purposes_subscription.data,
            update_payment_form.payment_purposes_donation.data,
        )
        payment_purposes_set = ("test", "free_trial", "subscription", "donation")
        first_true = True
        string = ""
        for x in range(len(new_payment_purposes_set)):
            if new_payment_purposes_set[x]:
                comma = "," if not first_true else ""
                string = f"{string}{comma}{payment_purposes_set[x]}"
                first_true = False
        # here we update the payment at payment_id with the new payment data
        update_payment_query = f"UPDATE Payments SET user_id = {user_id}, amount_usd = {new_payment['amount_usd']}, payment_purposes = '{string}' WHERE payment_id = {update_payment_form.payment_id.data}"
        connection.execute(update_payment_query)
        connection.close()
        return redirect(url_for("payments"))
    else:
        return redirect(url_for("payments"))


@app.route("/delete_payment", methods=["POST"])
def delete_payment():
    delete_payment_form = DeletePaymentForm()
    connection = db_engine.connect()
    # delete the payment at payment_id
    delete_payment_query = (
        f"DELETE FROM Payments WHERE payment_id = {delete_payment_form.payment_id.data}"
    )
    connection.execute(delete_payment_query)
    connection.close()
    return redirect(url_for("payments"))


@app.route("/payments/", methods=["GET", "POST"])
def payments():
    if request.method == "GET":
        # fetch all payments and users to populate dynamic lists
        connection = db_engine.connect()
        payments_query = "SELECT * FROM Payments"
        all_payments = connection.execute(payments_query).fetchall()
        users_query = "SELECT * FROM Users"
        all_users = connection.execute(users_query).fetchall()
        connection.close()

        # payment forms and select field population, users relationship is NULLABLE which has a value of -1; dealt with later
        add_new_payment_form = AddNewPaymentForm(request.form)
        add_new_payment_form.user_id.choices = [(-1, "NULL")] + [
            (g.user_id, g.user_id) for g in all_users
        ]
        delete_payment_form = DeletePaymentForm(request.form)
        delete_payment_form.payment_id.choices = [
            (g.payment_id, g.payment_id) for g in all_payments
        ]
        update_payment_form = UpdatePaymentForm(request.form)
        update_payment_form.user_id.choices = [(-1, "NULL")] + [
            (g.user_id, g.user_id) for g in all_users
        ]
        update_payment_form.payment_id.choices = [
            (g.payment_id, g.payment_id) for g in all_payments
        ]
        return render_template(
            "payments.html",
            all_payments=all_payments,
            add_new_payment_form=add_new_payment_form,
            delete_payment_form=delete_payment_form,
            update_payment_form=update_payment_form,
        )
    elif request.method == "POST":
        return redirect(url_for("payments"))


@app.route("/add_new_user_poll_setting", methods=["POST"])
def add_new_user_poll_setting():
    add_new_user_poll_setting_form = AddNewUserPollSettingForm()
    if not (
        add_new_user_poll_setting_form.user_permissions_collaborator.data
        or add_new_user_poll_setting_form.user_permissions_poll_creator.data
        or add_new_user_poll_setting_form.user_permissions_admin.data
        or add_new_user_poll_setting_form.user_permissions_superadmin.data
    ):
        return redirect(url_for("user_poll_settings"))
    connection = db_engine.connect()
    new_user_poll_setting = {
        "user_id": add_new_user_poll_setting_form.user_id.data,
        "poll_id": add_new_user_poll_setting_form.poll_id.data,
    }

    # setting up the set in exact needed format EX: 'permission1,permission2'
    new_user_poll_setting_permissions_set = (
        add_new_user_poll_setting_form.user_permissions_collaborator.data,
        add_new_user_poll_setting_form.user_permissions_poll_creator.data,
        add_new_user_poll_setting_form.user_permissions_admin.data,
        add_new_user_poll_setting_form.user_permissions_superadmin.data,
    )
    user_poll_setting_permissions_set = (
        "collaborator",
        "poll_creator",
        "admin",
        "superadmin",
    )
    first_true = True
    string = ""
    for x in range(len(new_user_poll_setting_permissions_set)):
        if new_user_poll_setting_permissions_set[x]:
            comma = "," if not first_true else ""
            string = f"{string}{comma}{user_poll_setting_permissions_set[x]}"
            first_true = False

    # inserting the new user_poll_setting to it's table
    add_new_user_poll_setting_query = f"INSERT INTO User_Poll_Settings (user_id, poll_id, user_permissions) VALUES ({new_user_poll_setting['user_id']}, {new_user_poll_setting['poll_id']}, '{string}')"
    connection.execute(add_new_user_poll_setting_query)
    connection.close()
    return redirect(url_for("user_poll_settings"))


@app.route("/delete_user_poll_setting", methods=["POST"])
def delete_user_poll_setting():
    delete_user_poll_setting_form = DeleteUserPollSettingForm()
    connection = db_engine.connect()

    # first we delete from user_poll_settings
    delete_user_poll_setting_query = f"Delete FROM User_Poll_Settings WHERE user_poll_setting_id = {delete_user_poll_setting_form.user_poll_setting_id.data}"
    connection.execute(delete_user_poll_setting_query)
    # but a poll cannot be connected to no user, so any polls stranded by the previous deletion are also deleted along with their votes
    delete_user_poll_setting_query = f"Delete FROM Votes where poll_id NOT IN (SELECT poll_id FROM User_Poll_Settings)"
    connection.execute(delete_user_poll_setting_query)
    delete_user_poll_setting_query = f"Delete FROM Polls where poll_id NOT IN (SELECT poll_id FROM User_Poll_Settings)"
    connection.execute(delete_user_poll_setting_query)
    connection.close()
    return redirect(url_for("user_poll_settings"))


@app.route("/user_poll_settings/", methods=["GET", "POST"])
def user_poll_settings():
    """User_Poll_Settings CRUD page"""
    if request.method == "GET":

        # get all User_Poll_Settings, and users and polls to fill dynamic 'select fields'
        connection = db_engine.connect()
        user_poll_settings_query = "SELECT * FROM User_Poll_Settings"
        all_user_poll_settings = connection.execute(user_poll_settings_query).fetchall()
        users_query = "SELECT * FROM Users"
        all_users = connection.execute(users_query).fetchall()
        polls_query = "SELECT * FROM Polls"
        all_polls = connection.execute(polls_query).fetchall()
        connection.close()

        # user_poll_setting forms, and select field population
        add_new_user_poll_setting_form = AddNewUserPollSettingForm(request.form)
        add_new_user_poll_setting_form.user_id.choices = [
            (g.user_id, g.user_id) for g in all_users
        ]
        add_new_user_poll_setting_form.poll_id.choices = [
            (g.poll_id, g.poll_id) for g in all_polls
        ]
        delete_user_poll_setting_form = DeleteUserPollSettingForm(request.form)
        delete_user_poll_setting_form.user_poll_setting_id.choices = [
            (g.user_poll_setting_id, g.user_poll_setting_id)
            for g in all_user_poll_settings
        ]

        return render_template(
            "user_poll_settings.html",
            all_user_poll_settings=all_user_poll_settings,
            add_new_user_poll_setting_form=add_new_user_poll_setting_form,
            delete_user_poll_setting_form=delete_user_poll_setting_form,
        )
    elif request.method == "POST":
        return redirect(url_for("user_poll_settings"))


@app.route("/test_db/")
def test_db():
    """Database test page."""

    connection = db_engine.connect()
    users_query = "SELECT * FROM Users"
    result = connection.execute(users_query).fetchall()

    return render_template("test_db.html", result=result)


if __name__ == "__main__":
    app.run()
