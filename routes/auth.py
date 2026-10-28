from flask import Blueprint, request, render_template, redirect, url_for, session
from db import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# Register
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Hash password
        hashed_pw = generate_password_hash(password)

        # Create user
        user = User(username=username, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template("register.html")

# Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for("auth.dashboard"))
        else:
            return "❌ Invalid credentials"

    return render_template("login.html")

# Dashboard (protected)
@auth_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user = User.query.get(session["user_id"])

    # Stats
    from db import Student, Career
    total_students = Student.query.count()
    total_careers = Career.query.count()

    return render_template("dashboard.html", user=user,
                           total_students=total_students,
                           total_careers=total_careers)


# Logout
@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))
