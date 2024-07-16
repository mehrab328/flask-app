from flask import Flask, render_template, request, redirect, url_for, flash, json
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mehrab'

db.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:
            return render_template('secretPage.html')
        else:
            flash('Invalid credentials!')
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        errors = []
        if len(password) < 8:
            errors.append("Password should be at least 8 characters long.\n")
        if not any(c.islower() for c in password):
            errors.append("You did not use a lowercase letter.\n")
        if not any(c.isupper() for c in password):
            errors.append("You did not use an uppercase letter.\n")
        if not (password[-1].isdigit()):
            errors.append("You did not end your password with a number.\n")

        if errors:
            flash("\n".join(errors))  # Join all errors into one message
            return render_template('signup.html', first_name=first_name, last_name=last_name, email=email)

        if password != confirm_password:
            flash('Passwords do not match!')
            return render_template('signup.html', first_name=first_name, last_name=last_name, email=email)
        
        # Check if the email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.')
            return render_template('signup.html', first_name=first_name, last_name=last_name, email=email)

        # Create a new user instance
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)  # Hash password in production
        db.session.add(new_user)
        db.session.commit()

        # Directly render thank-you page after successful registration
        return render_template('thankyou.html')
    
    return render_template('signup.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
