from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from . import db
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user: 
                if check_password_hash(user.password, password):
                    flash("Logged in!", category='Sucess')
                    login_user(user, remember=True)
                    flash("Welcome {{email}}", category="Welcome")
                    return redirect(url_for('views.home'))
                else:
                    flash("Password is incorrect!", category="error")
        else:
            flash("Email is incorrect!", category="error")
        


    return render_template("login.html", useri = current_user)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
    
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email already in use.', category='error')
        elif len(email) < 10:
            flash("Email is invalid", category="error")
        elif username_exists:
            flash('Username already in use', category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(username) < 2:
            flash("Username is too short", category="error")
        elif len(password1) < 2:
            flash("Password is too short", category="error")
        
        else:
            new_user = User(email=email, username=username, password= generate_password_hash(password1, method='scrypt'))
            print("a")
            db.session.add(new_user)
            print("b")
            db.session.commit()
            print("c")
            login_user(new_user, remember=True)
            flash("Signed un!", category='Sucess')
            flash("Welcome", username, category="Welcome")
            return redirect(url_for('views.home'))

    return render_template("signup.html", useri = current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))