from flask import Blueprint, request, render_template, redirect, url_for
from db import db, Student, Career

students_bp = Blueprint("students", __name__)

@students_bp.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        career_id = request.form["career_id"]
        student = Student(name=name, career_id=career_id, user_id=1)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for("students.list_students"))
    careers = Career.query.all()
    return render_template("add_student.html", careers=careers)

@students_bp.route("/students")
def list_students():
    students = Student.query.all()
    careers = {c.id: c.name for c in Career.query.all()}
    return render_template("students.html", students=students, careers=careers)

@students_bp.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    careers = Career.query.all()
    if request.method == "POST":
        student.name = request.form["name"]
        student.career_id = request.form["career_id"]
        db.session.commit()
        return redirect(url_for("students.list_students"))
    return render_template("edit_student.html", student=student, careers=careers)

@students_bp.route("/delete_student/<int:student_id>")
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("students.list_students"))
