from werkzeug.utils import html
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app.models.band import Band

@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    bands = Band.get_all_bands()
    return render_template('dashboard.html', bands = bands)

@app.route('/bands/new')
def new_band():
    return render_template('new_band.html')

@app.route('/bands/create', methods=['POST'])
def create_band():
    
    if Band.validate_band(request.form):
        data = {
            'band_name': request.form['band_name'],
            'music_genre': request.form['music_genre'],
            'home_city': request.form['home_city'],
            'founder_id': session['user_id']
        }
        Band.create_band(data)
        return redirect('/dashboard')

    return redirect('/bands/new')

@app.route('/bands/<int:band_id>')
def single_band(band_id):

    data = {
        'id': band_id
    }

    band = Band.get_band_by_id(data)

    if band == False:
        return redirect('/dashboard')

    return render_template('one_band.html', band = band)

@app.route('/bands/<int:band_id>/edit')
def edit_band(band_id):

    data = {
        'id': band_id
    }

    band = Band.get_band_by_id(data)

    if band == False:
        return redirect('/dashboard')

    if band.founder.id != session['user_id']:
        return redirect('/dashboard')

    return render_template('edit_band.html', band = band)

@app.route('/bands/<int:band_id>/update', methods=['POST'])
def update_band(band_id):

    if not Band.validate_band(request.form):
        return redirect(f'/bands/{band_id}/edit')

    else:
        data = {
            'band_name': request.form['band_name'],
            'music_genre': request.form['music_genre'],
            'home_city': request.form['home_city'],
            'band_id': band_id
        }
        Band.update_band(data)
        return redirect(f'/bands/{band_id}')

@app.route('/bands/<int:band_id>/confirm_delete')
def confirm_delete_band(band_id):

    data = {
        'id': band_id
    }

    band = Band.get_band_by_id(data)

    if band == False:
        return redirect('/dashboard')

    if band.founder.id != session['user_id']:
        return redirect('/dashboard')

    Band.delete_band(data)
    return render_template('confirm_delete_band.html', band = band)

@app.route('/bands/<int:band_id>/delete')
def destroy_band(band_id):

    data = {
        'id': band_id
    }

    band = Band.get_band_by_id(data)

    if band == False:
        return redirect('/dashboard')

    if band.founder.id != session['user_id']:
        return redirect('/dashboard')

    Band.delete_band(data)
    return redirect('/dashboard')
