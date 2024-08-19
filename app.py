from flask import Flask, render_template, redirect, url_for, request, flash
import redis
import json
from forms import AddRecipeForm, SearchRecipeForm, UpdateRecipeForm

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    keys = r.keys()
    recipes = [key.decode('utf-8') for key in keys]
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    form = AddRecipeForm()
    if form.validate_on_submit():
        name = form.name.data
        ingredients = form.ingredients.data.split(',')
        steps = form.steps.data.split(',')
        recipe = {
            "ingredients": ingredients,
            "steps": steps
        }
        r.set(name, json.dumps(recipe))
        flash('Receta añadida con éxito', 'success')
        return redirect(url_for('index'))
    return render_template('add_recipe.html', form=form)

@app.route('/update/<recipe_name>', methods=['GET', 'POST'])
def update_recipe(recipe_name):
    form = UpdateRecipeForm()
    recipe = json.loads(r.get(recipe_name))
    if request.method == 'GET':
        form.ingredients.data = ','.join(recipe['ingredients'])
        form.steps.data = ','.join(recipe['steps'])
    if form.validate_on_submit():
        ingredients = form.ingredients.data.split(',')
        steps = form.steps.data.split(',')
        updated_recipe = {
            "ingredients": ingredients,
            "steps": steps
        }
        r.set(recipe_name, json.dumps(updated_recipe))
        flash('Receta actualizada con éxito', 'success')
        return redirect(url_for('index'))
    return render_template('update_recipe.html', form=form, recipe_name=recipe_name)

@app.route('/delete/<recipe_name>')
def delete_recipe(recipe_name):
    r.delete(recipe_name)
    flash('Receta eliminada con éxito', 'success')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_recipe():
    form = SearchRecipeForm()
    recipe = None
    if form.validate_on_submit():
        recipe_name = form.name.data
        if r.exists(recipe_name):
            recipe = json.loads(r.get(recipe_name))
        else:
            flash('Receta no encontrada', 'danger')
    return render_template('search_recipe.html', form=form, recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
