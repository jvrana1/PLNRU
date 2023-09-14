# app.py

from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_session import Session # Import Flask-Session extension
from app.models import db, User, Task  # Import your User and Task models
from app.config import Config  # Import your Config class

app = Flask(__name__, template_folder="app/templates")

# Load the configuration settings defined in the Config class
app.config.from_object(Config)

# Initialize the SQLAlchemy database with the Flask app
db.init_app(app)

# Initialize the Flask-Session extension
app.config['SESSION_TYPE'] = 'filesystem'  # You can configure the session type as needed
Session(app)

# Your other configuration settings...

# Define your routes here

# Define the is_user_logged_in function
def is_user_logged_in():
    return 'user_id' in session  # Check if the 'user_id' is present in the session

# Home route
@app.route('/')
def home():
    if is_user_logged_in():
        # Implement your logic for logged-in users here
        return render_template('home.html')
    else:
        # Implement your logic for non-logged-in users here
        return render_template('login.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Login logic here
        # Assuming login is successful and you have the user's ID, set it in the session
        session['user_id'] = user_id  # Replace 'user_id' with the actual user's ID
        flash('Login successful!', 'success')

        # Redirect to the user's profile or another page
        return redirect(url_for('home'))

    return render_template('login.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        # Check if username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            # Username is already in use
            flash('Username is already taken. Please choose another.')
            return redirect(url_for('register'))  # Use url_for to specify the route

        if existing_email:
            # Email is already in use
            flash('Email is already registered. Please use a different email.')
            return redirect(url_for('register'))  # Use url_for to specify the route

        # If both username and email are unique, you can proceed with user registration
        # Save the user's information to the database, hash their password, etc.
        # Then, redirect to a success page or login page

    return render_template('register.html')  # Use the correct template name


# Profile route
@app.route('/profile')
def profile():
    # Your profile logic here
    return render_template('profile.html')

# Edit Profile route
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    # Retrieve the user's current profile information from the database
    # For example:
    user_id = session.get('user_id')  # Replace 'user_id' with the actual key used in your session
    user = User.query.get(user_id)

    if request.method == 'POST':
        # Update the user's profile information with user-submitted data
        user.email = request.form['email']
        user.school = request.form['school']

        # Save the changes to the database
        db.session.commit()

        flash('Profile updated successfully!', 'success')

        # Redirect the user to their profile page or another appropriate page
        return redirect(url_for('profile'))

    # Render the edit profile form with pre-filled data
    return render_template('edit_profile.html', email=user.email, school=user.school)

# Tasks route
@app.route('/tasks')
def tasks():
    # Retrieve tasks from the database (adjust based on your database structure)
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

# Edit Task route
@app.route('/edit-task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # Retrieve the task to edit from the database (adjust based on your database structure)
    task = Task.query.get(task_id)

    if request.method == 'POST':
        # Update the task with user-submitted data
        task.title = request.form['title']
        task.description = request.form['description']

        # Save the changes to the database
        db.session.commit()

        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks'))  # Redirect to the tasks page

    return render_template('edit_task.html', task=task)

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')

        # Update the task in the database
        if update_task_function(task_id, title, description, due_date, priority):
            flash('Task updated successfully', 'success')
        else:
            flash('Failed to update task', 'error')

    # Redirect back to the tasks page or the task details page
    return redirect(url_for('tasks'))

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Custom error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

# Your other routes and views...



if __name__ == '__main__':
    app.run(debug=True)
