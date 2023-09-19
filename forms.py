from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length


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
    subtitle = StringField("Project Subtitle")
    category = StringField("Project Category", validators=[DataRequired()])
    description = StringField("Project Description", validators=[DataRequired()])
    imgs_urls = StringField("Images URLs", validators=[DataRequired()])
    technologies_used = StringField("Technologies Used")
    role = StringField("Role", validators=[DataRequired()])
    links = StringField("Links")
    links_texts = StringField("Links Texts")
    status = StringField("Status", validators=[DataRequired()])
    submit = SubmitField("Submit Project", validators=[DataRequired()])


class AddTestimonialForm(FlaskForm):
    photo = StringField("Photo", validators=[DataRequired()])
    name = StringField("Project Subtitle", validators=[DataRequired()])
    profession = StringField("Profession", validators=[DataRequired()])
    profession_link = StringField("Profession Link", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    status = StringField("Status", validators=[DataRequired()])
    submit = SubmitField("Submit Testimonial", validators=[DataRequired()])
