import datetime as dt
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length

# ---------------------------- CREDENTIALS ------------------------------- #
# MY_EMAIL = os.environ.get("MY_EMAIL")
# MY_PASSWORD = os.environ.get("MY_PASSWORD")

LOGO = "</>"


# ---------------------------- WTForms ------------------------------- #
class ContactMe(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message='This field is required.')])
    email = StringField("Email", validators=[DataRequired(message='This field is required.'), Email()])
    phone_number = StringField("Phone Number", validators=[DataRequired(message='This field is required.')])
    message = TextAreaField("Message", validators=[DataRequired(message='This field is required.')],
                            render_kw={"rows": 10})
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(message='This field is required.'), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(message='This field is required.'), Length(min=8, max=50)])
    submit = SubmitField("Login")


class AddProjectForm(FlaskForm):
    title = StringField("Project Title", validators=[DataRequired()])
    subtitle = StringField("Project Subtitle", validators=[DataRequired()])
    category = StringField("Project Category", validators=[DataRequired()])
    description = StringField("Project Description", validators=[DataRequired()])
    imgs_urls = StringField("Images URLs", validators=[DataRequired()])
    submit = SubmitField("Submit Project")


# ------------------ Initializing A Flask App With Some Extensions --------------------- #
# Initialize the Flask app and set a secret key
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6derzihBXox7C0sKR6b'

# Initialize the Bootstrap extension
Bootstrap(app)

# Initialize the Flask-Login extension
login_manager = LoginManager()
login_manager.init_app(app)

# Set up the database connection (locally - SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///omar-mobarak.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# # Set up the database connection (pythonanywhere - MySQL)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://omarblog:mysqlpassword@omarblog.mysql.pythonanywhere-services.com:3306/omarblog$default'
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 280, 'pool_timeout': 10}
# app.config['SQLALCHEMY_POOL_SIZE'] = 5
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# # Use SQLite as a fallback if the MySQL URL fails
# app.config['SQLALCHEMY_FALLBACK_URI'] = 'sqlite://///home/omarblog/Day-59-60-67-69-blog--5th-capstone-/instance/blog.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# ---------------------------- DB Tables ------------------------------- #
# Users table in db
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return f'<User {self.name}>'


# Projects table in db
class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    subtitle = db.Column(db.String)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    imgs_urls = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Project {self.title}>'


with app.app_context():
    db.create_all()


# ---------------------------- Custom Functions ------------------------------- #
def send_mail(name, email, phone, message):
    # create message object instance
    msg = MIMEMultipart()

    # set up the parameters of the message
    password = MY_PASSWORD
    msg['From'] = MY_EMAIL
    msg['To'] = "omarmobarak53@gmail.com"
    msg['Subject'] = "New message from 'Omar's Portfolio' user"

    # add in the message body
    body = f"Name: {name}\nEmail: {email}\nPhone Number: {phone}\nMessage: {message}"
    msg.attach(MIMEText(body, 'plain'))

    # create server instance
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for secure connection
    server.starttls()

    # Login to the server
    server.login(msg['From'], password)

    # send the message via the server
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    # close the server connection
    server.quit()


# Create a custom decorator to restrict access to non-logged-in users
def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You must log out first in order to access this page.')
            return redirect(url_for('home'))
        return func(*args, **kwargs)

    return decorated_function


# Set up the user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------------------- Main Pages Routes ------------------------------- #
@app.route("/", methods=["GET", "Post"])
def home():
    now = dt.datetime.now()
    year = now.year

    contact_form = ContactMe()
    sent_successfully = ""
    if contact_form.validate_on_submit():
        name = contact_form.name.data
        email = contact_form.email.data
        phone = contact_form.phone_number.data
        message = contact_form.message.data
        try:
            send_mail(name, email, phone, message)
            sent_successfully = "Your message has been sent successfully! We will get back to you as soon as possible."

        except (smtplib.SMTPException, socket.gaierror):
            flash("Sorry, there was an error sending your message. Please try again later.")

    return render_template(
        "index.html",
        logo=LOGO,
        year=year,
        contact_form=contact_form,
        sent_successfully=sent_successfully
    )


@app.route("/Portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/Project-details/<int:project_id>")
def project_details(project_id):
    return render_template("project_details.html", project_id=project_id)


# ---------------------------- Admin Pages Routes ------------------------------- #
@app.route("/login-admin", methods=["GET", "Post"])
@logout_required
def login_admin():
    now = dt.datetime.now()
    year = now.year

    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("The password is incorrect, please try again.")
        else:
            flash("The email does not exist, please try again.")

    return render_template("login-admin.html",
                           logo=LOGO,
                           year=year,
                           login_form=login_form
                           )


@app.route('/logout-admin')
@login_required
def logout_admin():
    logout_user()
    return redirect(url_for('home'))


@app.route("/new-project", methods=["GET", "Post"])
@login_required
def add_new_project():
    add_form = AddProjectForm()
    h2 = "New Project"
    p = "Enrich your portfolio with a new fabulous project!"
    if add_form.validate_on_submit():
        with app.app_context():
            new_project = Project(
                title=add_form.title.data,
                subtitle=add_form.subtitle.data,
                category=add_form.category.data,
                description=add_form.description.data,
                imgs_urls=add_form.imgs_urls.data,
            )
            db.session.add(new_project)
            db.session.commit()
        return redirect(url_for("home"))

    return render_template("add-project.html", add_form=add_form, h2=h2, p=p)


@app.route("/edit-project/<int:project_id>", methods=["GET", "Post"])
@login_required
def edit_project(project_id):
    project = Project.query.get(project_id)
    h2 = "Edit Project"
    p = "Optimize your portfolio with some edits!"
    edit_form = AddProjectForm(
        title=project.title,
        subtitle=project.subtitle,
        category=project.category,
        description=project.description,
        imgs_urls=project.imgs_urls,
    )
    if edit_form.validate_on_submit():
        project.title = edit_form.title.data
        project.subtitle = edit_form.subtitle.data
        project.category = edit_form.category.data
        project.description = edit_form.description.data
        project.imgs_urls = edit_form.imgs_urls.data
        db.session.commit()
        return redirect(url_for("project-details", project_id=project.id))

    return render_template("add-project.html", form=edit_form, h2=h2, p=p)


@app.route("/delete/<int:project_id>")
@login_required
def delete_project(project_id):
    project_to_delete = Project.query.get(project_id)
    db.session.delete(project_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
