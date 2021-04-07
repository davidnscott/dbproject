from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, BooleanField 
from wtforms.validators import InputRequired, Email, DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[InputRequired(),Email()])

class UserForm(FlaskForm):
	#uid = StringField('UserId', validators=[InputRequired()])
	fname = StringField('First Name', validators=[InputRequired()])
	lname = StringField('Last Name', validators=[InputRequired()])
	age = StringField('Age', validators=[InputRequired()])
	gender = StringField('Gender', validators=[InputRequired()])
	email = StringField('Email', validators=[InputRequired(),Email()])

class InstructionForm(FlaskForm):
	#instrucid = StringField('InstructionId', validators=[InputRequired()])
	#recid = StringField('RecipeId', validators=[InputRequired()])
	stepnum = StringField('StepNum', validators=[InputRequired()])
	instruction = StringField('Instruction', validators=[InputRequired()])

class IngredientsForm(FlaskForm):
	#ingredid = StringField('IngredientId', validators=[InputRequired()])
	#recid = StringField('RecipeId', validators=[InputRequired()])
	ingredname= StringField('Ingredient Name', validators=[InputRequired()])
	quantity = StringField('Quantity', validators=[InputRequired()])
	measurement = StringField('Measurement', validators=[InputRequired()])

class RecipeForm(FlaskForm):
	#mealid = StringField('MealId', validators=[InputRequired()])
	#recid = StringField('RecId', validators=[InputRequired()])
	instrucid = TextAreaField('Instruction ID', validators=[InputRequired()])
	ingredid = TextAreaField('Ingredient ID', validators=[InputRequired()])
	desc = TextAreaField('Description / Name', validators=[InputRequired()])
	#numofcals = StringField('Number of Calories', validators=[InputRequired()])
	typeofdiet = StringField('Type of Diet', validators=[InputRequired()])
	servings = StringField('Servings', validators=[InputRequired()])

class CalorieForm(FlaskForm):
	caloriecount = StringField('Max Calorie Count')
	
class MealForm(FlaskForm):
	#mealid = StringField('MealId',validators=[DataRequired()])
	recid = StringField('Recipe Id', validators=[InputRequired()])
	#name = StringField('Meal Name', validators=[DataRequired()])
	mealtype = StringField('Type of Meal', validators=[DataRequired()])
	#day = StringField('Day of the Week', validators=[DataRequired()])
	numofcals = StringField('Number of Calories', validators=[InputRequired()])
	photo = FileField('Meal Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

class MealPlanForm(FlaskForm):
	#uid = StringField('UserId', validators=[InputRequired()])
	email = StringField('Email', validators=[InputRequired(),Email()])
	#mpid = StringField('MealPlanId', validators=[InputRequired()])
	mealid = StringField('MealId', validators=[InputRequired()])
	meals = StringField('Num of Meals', validators=[InputRequired()])
	dow = StringField('Day of Week', validators=[InputRequired()])

class KitchenForm(FlaskForm):
	ingredid = BooleanField('Ingredient Id')

class ShoppingListForm(FlaskForm):
	#slid = StringField('ShoppingListId',validators=[InputRequired()])
	kid = StringField('KitchenId', validators=[InputRequired()])
	ingredid = StringField('Ingredient ID',validators=[InputRequired()])
	
class SearchForm(FlaskForm):
	name = StringField('Recipe Name', validators=[InputRequired()])
