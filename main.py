import datetime as dt
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_wtf import FlaskForm
from flask import Flask, render_template, flash
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

# ---------------------------- CREDENTIALS ------------------------------- #
MY_EMAIL = "pythontest32288@gmail.com"
MY_PASSWORD = "gsrfzucledwimgqp"

# ------------------ Initializing A Flask App With Some Extensions --------------------- #
# Initialize the Flask app and set a secret key
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6derzihBXox7C0sKR6b'


# ---------------------------- WTForms ------------------------------- #
def validate_email(form, field):
    if '@' not in field.data:
        raise ValidationError('Please enter a valid email address.')


class ContactMe(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message='This field is required.')])
    email = StringField("Email", validators=[DataRequired(message='This field is required.'), validate_email])
    phone_number = StringField("Phone Number", validators=[DataRequired(message='This field is required.')])
    message = TextAreaField("Message", validators=[DataRequired(message='This field is required.')], render_kw={"rows": 10})
    submit = SubmitField("Submit")


# ---------------------------- Custom Functions ------------------------------- #
def send_mail(name, email, phone, message):
    # create message object instance
    msg = MIMEMultipart()

    # set up the parameters of the message
    password = MY_PASSWORD
    msg['From'] = MY_EMAIL
    msg['To'] = "omarmobarak53@gmail.com"
    msg['Subject'] = "New message from 'Omar Mobarak' Portfolio' user"

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


# ---------------------------- Main Pages Routes ------------------------------- #
@app.route("/", methods=["GET", "POST"])
def home():
    logo = "</> Omar Mobarak"

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
        logo=logo,
        year=year,
        contact_form=contact_form,
        sent_successfully=sent_successfully
    )


if __name__ == "__main__":
    app.run(debug=True)
