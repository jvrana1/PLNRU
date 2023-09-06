from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import psycopg2  # For PostgreSQL database

app = Flask(__name__)

# Replace these values with your Gmail credentials
GMAIL_USERNAME = 'your@gmail.com'
GMAIL_PASSWORD = 'your_password'

# Replace with your database connection details
DB_HOST = 'your_db_host'
DB_PORT = 'your_db_port'
DB_NAME = 'your_db_name'
DB_USER = 'your_db_user'
DB_PASSWORD = 'your_db_password'

# Function to send an email with a temporary password
def send_email(username, temp_password, recipient_email):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USERNAME
        msg['To'] = recipient_email
        msg['Subject'] = 'Password Reset'

        message = f'Your temporary password is: {temp_password}'
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USERNAME, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(str(e))
        return False

# Database connection function
def connect_db():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except Exception as e:
        print(str(e))
        return None

# Route for the index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route for user registration
@app.route('/signup', methods=['POST'])
def signup():
    # Get user input from the registration form
    username = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    college = request.form['college']
    email = request.form['email']

    # Generate a temporary password
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # TODO: Store user information in the database

    # Send the temporary password via email
    if send_email(first_name, temp_password, email):
        return "Account created successfully. Check your email for the temporary password."
    else:
        return "Account creation failed. Please try again."

# Route for password reset
@app.route('/reset', methods=['POST'])
def reset_password():
    # Get the username from the reset form
    reset_username = request.form['reset_username']

    # TODO: Look up the user's email address from the database

    # Generate a temporary password
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # TODO: Update the user's password in the database

    # Send the temporary password via email
    if send_email(reset_username, temp_password, user_email):
        return "Password reset successful. Check your email for the temporary password."
    else:
        return "Password reset failed. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
