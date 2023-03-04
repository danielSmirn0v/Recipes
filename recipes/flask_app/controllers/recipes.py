
from flask_app import app

from flask import Flask, render_template, request, redirect, session, flash

from flask_app.models import user, recipe






@app.route('/recipe/new')
def create_recipe():

    if 'user_info' not in session:
        return redirect('/')

    return render_template('new_recipe.html')

@app.route('/create_recipe', methods = ['POST'])
def new_recipe():
    print('we made it this far')
    if 'user_info' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_info'],
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'under_30': request.form['under_30'],
        'when_made' : request.form['when_made'],
    }
    
    print(data)
    recipe.Recipes.save_recipe(data)
    print('it may have created recipe')


    return redirect('/recipes')

@app.route('/recipe/<int:id>/update')
def edit_view(id):

    if 'user_info' not in session:
        return redirect('/')

    return render_template('edit_recipe.html', rec_user = recipe.Recipes.one_recipe_with_user({'id': id}) )

@app.route('/recipe/<int:id>/edit', methods = ['POST'])
def edit_recipe(id):
    data = {
        'id' : id,
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'under_30': request.form['under_30'],
        'when_made' : request.form['when_made'],
    }

    return redirect('/recipes')


@app.route('/delete/<int:id>')
def delete_recipe(id):
    recipe.Recipes.delete({'id': id})

    return redirect('/recipes')

