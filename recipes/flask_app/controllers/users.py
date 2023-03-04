
from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models import user, recipe

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def first():

    return render_template('home_page.html')


@app.route('/create', methods = ['POST'])
def register():

    if request.form['action'] == 'register':

        if not user.User.validate(request.form):
            return redirect('/')
        
        email_exists = user.User.get_onewith_email({'email': request.form['email'].lower()})
        if email_exists:
            flash('Email already used')
            return redirect('/')

        pw_hash = bcrypt.generate_password_hash(request.form["password"])

        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password': pw_hash
        
        }

        user_info = user.User.save(data)
        print(f'you got {user_info} in ')
        session['user_info'] = user_info
        print()

    else:


        print('wow we are here')
        user_info = user.User.get_onewith_email ({'email': request.form['email'].lower()})
        print(user_info)

        if user_info:
            if request.form['email'] == user_info.email and bcrypt.check_password_hash(user_info.password, request.form['password']):
                session['user_info'] = user_info.id
                return redirect('/recipes')
            else:
                flash('Wrong Password')
                return redirect('/')
        else:
            flash('Email incorrect')
            return redirect('/')

        



    return redirect('/recipes')

@app.route('/recipes')
def all_recipes():

    if 'user_info' not in session:
        return redirect('/')

    data = {
        'id' : session['user_info']
    }

    return render_template('index.html', user = user.User.get_one(data), recipes = recipe.Recipes.get_all() )

@app.route('/recipes/<int:id>/recipe')
def view_one(id):
    if 'user_info' not in session:
        return redirect('/')
    data = {
        'id':id
    }

    return render_template('single_recipe.html', recipe = recipe.Recipes.one_recipe_with_user(data), user = user.User.get_one({'id' : session['user_info']}))

@app.route('/logout')

def logout():
    session.clear()
    return redirect('/')

