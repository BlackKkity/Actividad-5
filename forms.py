from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AddRecipeForm(FlaskForm):
    name = StringField('Nombre de la receta', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredientes (separados por comas)', validators=[DataRequired()])
    steps = TextAreaField('Pasos (separados por comas)', validators=[DataRequired()])
    submit = SubmitField('Agregar Receta')

class UpdateRecipeForm(FlaskForm):
    ingredients = TextAreaField('Ingredientes (separados por comas)', validators=[DataRequired()])
    steps = TextAreaField('Pasos (separados por comas)', validators=[DataRequired()])
    submit = SubmitField('Actualizar Receta')

class SearchRecipeForm(FlaskForm):
    name = StringField('Nombre de la receta', validators=[DataRequired()])
    submit = SubmitField('Buscar Receta')
