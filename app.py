from flask import Flask, render_template
from db import db, User, Career
from routes.students import students_bp
from routes.auth import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cmate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"  # needed for sessions

db.init_app(app)

with app.app_context():
    db.create_all()

    # Seed demo data if empty
    if not Career.query.first():
        db.session.add_all([
            Career(name="Software Engineer"),
            Career(name="Data Analyst"),
            Career(name="Designer")
        ])
        db.session.commit()

    if not User.query.first():
        db.session.add(User(username="admin", email="admin@example.com", password="admin"))
        db.session.commit()

# Register blueprints
app.register_blueprint(students_bp)
app.register_blueprint(auth_bp)

# Index page (landing page)
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

