# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)


@app.route("/")
def home():
    """Home page."""
    return render_template("public/home.html")


@app.route("/about")
def about():
    """About page."""
    return render_template("public/about.html")


@app.route("/users", methods=["GET", "POST"])
def users():
    return "Hi"
    # """Users CRUD page"""
    # create_user_form = CreateUserForm(request.form)
    # if request.method == "GET":
    #     return render_template("public/users.html", create_user_form=create_user_form)
    # elif request.method == "POST":

    #     if True:
    #         # flash("Created new user!", "success")
    #         return redirect(url_for("public.users"))
    #     # if create_user_form.validate_on_submit():
    #     #     User.create(
    #     #         username=create_user_form.username.data,
    #     #         email=create_user_form.email.data,
    #     #         password=create_user_form.password.data,
    #     #         active=create_user_form,
    #     #     )
    #     #     flash("Created new user!", "success")
    #     #     return redirect(url_for("public.users"))
    #     else:
    #         flash_errors(create_user_form)
    #         return redirect(url_for("public.users"))
    # return render_template("public/users.html", create_user_form=create_user_form)


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


@blueprint.route("/polls/")
def polls():
    """Polls CRUD page."""
    return render_template("public/polls.html")


@blueprint.route("/votes/")
def votes():
    """Votes CRUD page."""
    return render_template("public/votes.html")


@blueprint.route("/payments/")
def payments():
    """Payments CRUD page."""
    return render_template("public/payments.html")


@blueprint.route("/users_polls/")
def users_polls():
    """Users_Polls CRUD page."""
    return render_template("public/users_polls.html")
