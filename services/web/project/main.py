import time
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import Patient, Exam, Note

from .views import plot_labour

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    user = Patient.query.filter_by(email=current_user.email).first()
    
    if user.profile_init:
        return render_template(
            "profile.html",
            user=current_user,
        )
    else:
        return render_template(
            "init_profile.html",
            user=current_user,
            pregs=[i for i in range(10)],
            height=[i for i in range(200)],
            weight=[i for i in range(300)],
        )

@main.route("/update_profile")
@login_required
def update_profile():
    user = Patient.query.filter_by(email=current_user.email).first()
    user.profile_init = False
    db.session.commit()
    return redirect(url_for("main.profile"))

@main.route("/init_profile", methods=["POST"])
@login_required
def init_profile():
    prev_pregs = request.form.get("prev_pregs")
    height = request.form.get("height")
    weight = request.form.get("weight")

    user = Patient.query.filter_by(email=current_user.email).first()

    if height and weight:
        user.no_pregnancies = prev_pregs
        user.height = height
        user.weight = weight
        user.profile_init = True
        db.session.commit()
        flash("Profile successully updated.")
    else:
        flash("Error updating profile.")

    return redirect(url_for("main.profile"))

@main.route("/graph")
@login_required
def graph():
    hist_plot = plot_labour(current_user)
    return render_template(
        "graph.html",
        history=hist_plot,
    )


@main.route("/new_exam")
@login_required
def new_exam():
    return render_template(
        "new_exam.html",
        user=current_user,
        dilation=[i for i in range(-10, 10)],
        effacement=[i for i in range(-10, 10)],
        station=[i for i in range(-10, 10)],
    )

@main.route("/labor_status", methods=["POST"])
@login_required
def labor_status():

    user = Patient.query.filter_by(email=current_user.email).first()

    user.in_labour = time.time()

    db.session.commit()

    return redirect(url_for("main.profile"))


@main.route("/notes")
@login_required
def notes():
    return render_template("notes.html")

@main.route("/submit_exam", methods=["POST"])
@login_required
def submit_exam():
    dilation = request.form.get("dilation")
    effacement = request.form.get("effacement")
    station = request.form.get("station")

    exam = Exam(name=current_user.name, dilation=dilation, effacement=effacement, station=station)
    
    db.session.add(exam)
    db.session.commit()

    flash("Exam data added.")

    return redirect(url_for("main.graph"))


@main.route("/submit_note", methods=["POST"])
@login_required
def submit_note():
    note_text = request.form.get("notes")

    note = Note(name=current_user.name, note=note_text)
    
    db.session.add(note)
    db.session.commit()

    flash("Exam data added.")

    return redirect(url_for("main.graph"))
    

@main.route("/user_password_change", methods=["POST"])
@login_required
def user_password_change():
    old_pass = request.form.get("old_pw")
    new_pass1 = request.form.get("pw1")
    new_pass2 = request.form.get("pw2")

    user = Patient.query.filter_by(email=current_user.email).first()

    if check_password_hash(user.password, old_pass):
        if new_pass1 == new_pass2:
            user.password = generate_password_hash(new_pass1, method="sha256")
            # db.session.add(user)
            db.session.commit()
            flash("Password has been updated.", "success")
            return redirect(url_for("main.profile"))
        else:
            flash("The new password entries do not match.")
    else:
        flash("The old password is incorrect.")

    return render_template("update_password.html")


@main.route("/update_password")
@login_required
def update_password():
    return render_template("update_password.html")
