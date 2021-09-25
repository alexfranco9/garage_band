from flask_app import app # importing the instance of the flask app
from flask import render_template, redirect, request, session,flash

from flask_app.models.user import User

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users/create', methods=['POST'])
def create_user():
    print(request.form)

    is_valid = User.validate_user(request.form)

    if is_valid:
        hashed_password = bcrypt.generate_password_hash(request.form['password'])
        
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': hashed_password
        }

        user_id = User.create_user(data)
        session['user_id'] = user_id
        session['first_name'] = request.form['first_name']
        
        flash('Account created successfully, please login.')
        return redirect('/')
    else:
        return redirect('/')


@app.route('/users/login', methods=['POST'])
def user_login():

    user = User.get_user_by_email(request.form)

    if not user: 
        flash('Email is incorrect')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password is incorrect')
        return redirect('/')

    session['user_id'] = user.id
    session['first_name'] = user.first_name

    return redirect('/dashboard')

@app.route('/users/<int:user_id>')
def get_user(user_id):

    data = {
        'id': user_id
    }

    user = User.get_user(data)

    if user == False:
        return redirect('/dashboard')

    return render_template('mybands.html', user = user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

