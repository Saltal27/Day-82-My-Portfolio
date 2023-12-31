import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from forms import ContactMe, LoginForm, AddProjectForm, AddTestimonialForm

# ---------------------------- CREDENTIALS ------------------------------- #
# MY_EMAIL = os.environ.get("MY_EMAIL")
# MY_PASSWORD = os.environ.get("MY_PASSWORD")

LOGO = "</>"

# ------------------ Initializing A Flask App With Some Extensions --------------------- #
# Initialize the Flask app and set a secret key
app = Flask(__name__)


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
    technologies_used = db.Column(db.String)
    role = db.Column(db.String, nullable=False)
    links = db.Column(db.String)
    links_texts = db.Column(db.String)
    status = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Project {self.title}>'


# Testimonials table in db
class Testimonial(db.Model):
    __tablename__ = "testimonials"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    profession = db.Column(db.String, nullable=False)
    profession_link = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Testimonial {self.id}>'


with app.app_context():
    db.create_all()


# ---------------------------- Custom Functions ------------------------------- #
# Create a custom function to print all users in the database
def all_users():
    users = User.query.all()
    print(users)


# Create a custom function to add users to the database
def add_user_db(name, email, password):
    with app.app_context():
        new_user = User()
        new_user.name = name
        new_user.email = email
        salted_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user.password = salted_hash
        db.session.add(new_user)
        db.session.commit()


# Create a custom function to delete a user from the database
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()


# Create a custom function to send emails
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
    projects = Project.query.all()
    projects_webdev = [project for project in projects if project.category == "Web Development"]
    projects_uiux = [project for project in projects if project.category == "UI/UX"]
    projects_python = [project for project in projects if project.category == "Python"]
    online_projects = [project for project in projects if project.status == "Online"]
    online_projects_webdev = [project for project in online_projects if project.category == "Web Development"]
    online_projects_uiux = [project for project in online_projects if project.category == "UI/UX"]
    online_projects_python = [project for project in online_projects if project.category == "Python"]

    testimonials_list = []
    online_testimonials_list = []
    testimonials = Testimonial.query.all()
    online_testimonials = [testimonial for testimonial in testimonials if testimonial.status == "Online"]
    for testimonial in testimonials:
        testimonial_dict = {
            "id": testimonial.id,
            "photo": testimonial.photo,
            "name": testimonial.name,
            "profession": testimonial.profession,
            "professionLink": testimonial.profession_link,
            "description": testimonial.description
        }
        testimonials_list.append(testimonial_dict)
    for testimonial in online_testimonials:
        testimonial_dict = {
            "id": testimonial.id,
            "photo": testimonial.photo,
            "name": testimonial.name,
            "profession": testimonial.profession,
            "professionLink": testimonial.profession_link,
            "description": testimonial.description
        }
        online_testimonials_list.append(testimonial_dict)

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
        projects=projects,
        projects_webdev=projects_webdev,
        projects_uiux=projects_uiux,
        projects_python=projects_python,
        online_projects=online_projects,
        online_projects_webdev=online_projects_webdev,
        online_projects_uiux=online_projects_uiux,
        online_projects_python=online_projects_python,
        testimonials_list=testimonials_list[::-1],
        online_testimonials_list=online_testimonials_list[::-1],
        contact_form=contact_form,
        sent_successfully=sent_successfully
    )


@app.route("/Portfolio")
def portfolio():
    projects = Project.query.all()
    projects_webdev = [project for project in projects if project.category == "Web Development"]
    projects_uiux = [project for project in projects if project.category == "UI/UX"]
    projects_python = [project for project in projects if project.category == "Python"]
    online_projects = [project for project in projects if project.status == "Online"]
    online_projects_webdev = [project for project in online_projects if project.category == "Web Development"]
    online_projects_uiux = [project for project in online_projects if project.category == "UI/UX"]
    online_projects_python = [project for project in online_projects if project.category == "Python"]

    return render_template(
        "portfolio.html",
        logo=LOGO,
        projects=projects,
        projects_webdev=projects_webdev,
        projects_uiux=projects_uiux,
        projects_python=projects_python,
        online_projects=online_projects,
        online_projects_webdev=online_projects_webdev,
        online_projects_uiux=online_projects_uiux,
        online_projects_python=online_projects_python,
    )


@app.route("/Portfolio/<int:project_id>", methods=["GET", "Post"])
def project_details(project_id):
    project = Project.query.filter_by(id=project_id).first()
    return render_template("project-details.html", logo=LOGO, project=project)


# ---------------------------- Admin Pages Routes ------------------------------- #
@app.route("/login-admin", methods=["GET", "Post"])
@logout_required
def login_admin():
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
    if add_form.validate_on_submit():
        with app.app_context():
            new_project = Project(
                title=add_form.title.data,
                subtitle=add_form.subtitle.data,
                category=add_form.category.data,
                description=add_form.description.data,
                imgs_urls=add_form.imgs_urls.data,
                technologies_used=add_form.technologies_used.data,
                role=add_form.role.data,
                links=add_form.links.data,
                links_texts=add_form.links_texts.data,
                status=add_form.status.data,
            )
            db.session.add(new_project)
            db.session.commit()
        return redirect(url_for("home"))

    return render_template("add-project.html", logo=LOGO, form=add_form)


@app.route("/edit-project/<int:project_id>", methods=["GET", "Post"])
@login_required
def edit_project(project_id):
    project = Project.query.get(project_id)
    edit_form = AddProjectForm(obj=project)
    if edit_form.validate_on_submit():
        edit_form.populate_obj(project)
        db.session.commit()
        return redirect(url_for("project_details", project_id=project.id))

    return render_template("edit-project.html", logo=LOGO, form=edit_form, project=project)


@app.route("/delete/<int:project_id>")
@login_required
def delete_project(project_id):
    project_to_delete = Project.query.get(project_id)
    db.session.delete(project_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/new-testimonial", methods=["GET", "POST"])
@login_required
def add_new_testimonial():
    add_form = AddTestimonialForm()
    if add_form.validate_on_submit():
        with app.app_context():
            new_testimonial = Testimonial(
                photo=add_form.photo.data,
                name=add_form.name.data,
                profession=add_form.profession.data,
                profession_link=add_form.profession_link.data,
                description=add_form.description.data,
                status=add_form.status.data,
            )
            db.session.add(new_testimonial)
            db.session.commit()
        return redirect(url_for("home"))

    return render_template("add-testimonial.html", logo=LOGO, form=add_form)


@app.route("/edit-testimonial/<int:testimonial_id>", methods=["GET", "POST"])
@login_required
def edit_testimonial(testimonial_id):
    testimonial = Testimonial.query.get(testimonial_id)
    edit_form = AddTestimonialForm(obj=testimonial)
    if edit_form.validate_on_submit():
        edit_form.populate_obj(testimonial)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit-testimonial.html", logo=LOGO, form=edit_form, testimonial=testimonial)


@app.route("/delete-testimonial/<int:testimonial_id>")
@login_required
def delete_testimonial(testimonial_id):
    testimonial_to_delete = Testimonial.query.get(testimonial_id)
    db.session.delete(testimonial_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
