from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import Patient, Exam
from .util import send_email, ts

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = Patient.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user:
        flash("Patient not found. Please Sign Up.")
        return redirect(url_for("auth.signup"))
    elif not user.email_confirmed:
        flash(
            "Please confirm your e-mail before logging in. An email has been sent to {}.".format(
                user.email
            )
        )
        generate_user_email(user.email)
        return redirect(url_for("auth.login"))
    elif not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():

    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = Patient.query.filter_by(
        email=email
    ).first()  # if this returns a user, then the email already exists in database

    if (
        user
    ):  # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = Patient(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
    )

    generate_user_email(email)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except Exception:
        # flake8: noqa: F821
        abort(404)

    user = Patient.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


def generate_user_email(email):
    # Now we'll send the email confirmation link
    subject = "Baby Curve - Confirm your email"

    token = ts.dumps(email, salt="email-confirm-key")

    confirm_url = url_for("auth.confirm_email", token=token, _external=True)

    html = render_template("email/activate.html", confirm_url=confirm_url)

    # We'll assume that send_email has been defined in myapp/util.py
    send_email(email, subject, html)
