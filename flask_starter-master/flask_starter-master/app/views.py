"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for,Flask, flash, session, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import UserForm, LoginForm, IngredientsForm, InstructionForm, RecipeForm, MealForm, MealPlanForm, KitchenForm, ShoppingListForm, CalorieForm, SearchForm
from flask_mysqldb import MySQL
from datetime import date
from werkzeug.utils import secure_filename
import os
import random
#from fake import Faker

 

mysql = MySQL(app)



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Kalia-Lee Rodney, Shaquan Robinson, Keneil Thompson, David Scott")

@app.route('/logout')
#@login_required
def logout():
	session.clear()
	#logout_user()
	return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if request.method == "POST":
		if form.email.data:
			email = form.email.data
            #user = UserProfile.query.filter_by(email=email).first()
			cursor = mysql.connection.cursor()
			query_string = """SELECT * FROM User WHERE email = %s"""
			cursor.execute(query_string, (email,))

			user = cursor.fetchone()
			cursor.close()
			print(user)
			if user is not None:
				session['loggedin'] = True
				session['email'] = user[4]
				session['fname'] = user[0]
				session['lname'] = user[1]
				#login_user(user)
				#flash("Login Successful","Success")
				flash("Logged in as "+session['fname']+" "+session['lname'])
				return redirect(url_for("home"))
			else:
				flash("User not found.")
	return render_template("login.html", form=form)

@app.route('/secure-page')
#@login_required
def secure_page():
	return render_template('home.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
	form = UserForm()
   
	if request.method == 'POST' and form.validate_on_submit():
		#uid = request.form['uid']
		fname = request.form['fname']
		lname = request.form['lname']
		age = request.form['age']
		gender = request.form['gender']
		email = request.form['email']
		cursor = mysql.connection.cursor()
		cursor.execute(''' INSERT INTO User (FirstName,LastName,Age,Gender,Email) VALUES(%s,%s,%s,%s,%s)''',(fname,lname,age,gender,email))
		mysql.connection.commit()
		cursor.close()
		flash("Succesfully signed up!!")
		return render_template("home.html")
	return render_template("signup.html", form=form)

@app.route('/ingredient', methods = ['POST', 'GET'])
def ingredient():
	form = IngredientsForm()
	print("OMEGA")
	if request.method == 'POST' and form.validate_on_submit():
		name = request.form['ingredname']
		qty = request.form['quantity']
		measurement = request.form['measurement']
		cursor = mysql.connection.cursor()
		cursor.execute(''' INSERT INTO Ingredients (IngredientName, Quantity, Measurement) VALUES(%s,%s,%s)''',(name, qty, measurement))
		mysql.connection.commit()
		cursor.close()
		flash("Succesfully added recipe!!")
		return render_template("home.html")
	return render_template("ingred.html", form=form)

@app.route('/instruction', methods = ['POST', 'GET'])
def instruction():
	form = InstructionForm()
	print("OMEGA")
	if request.method == 'POST' and form.validate_on_submit():
		step1 = request.form['step1']
		step2 = request.form['step2']
		step3 = request.form['step3']
		#measurement = request.form['measurement']
		cursor = mysql.connection.cursor()
		cursor.execute(''' INSERT INTO Instruction (Step1,Step2,Step3) VALUES(%s,%s,%s)''',(step1, step2,step3))
		mysql.connection.commit()
		cursor.execute(''' Select max(InstructionID) from Instruction''')
		id = cursor.fetchone()
		cursor.close()
		flash("Succesfully added Instruction with ID - "+str(id[0]))
		return render_template("home.html")
	return render_template("instruc.html", form=form)

@app.route('/recipe', methods = ['POST', 'GET'])
def recipe():
	form = RecipeForm()
	print("OMEGA")
	if request.method == 'POST' and form.validate_on_submit():
		#uid = request.form['uid']
		instrucid = request.form['instrucid']
		ingredid = request.form['ingredid']
		desc = request.form['desc']
		#numofcals = request.form['numofcals']
		typeofdiet = request.form['typeofdiet']
		servings = request.form['servings']
		cursor = mysql.connection.cursor()
		creationdate = date.today()
		#print(mealid,desc,numofcals,typeofdiet,servings,creationdate)
		cursor.execute(''' INSERT INTO Recipe (InstructionID,IngredientID,CreationDate,RDescription,TypeofDiet,Servings) VALUES(%s,%s,%s,%s,%s,%s)''',(instrucid,ingredid,creationdate,desc,typeofdiet,servings))
		mysql.connection.commit()
		cursor.execute(''' Select max(RecID) from Recipe''')
		id = cursor.fetchone()
		cursor.close()
		flash("Succesfully added Recipe with ID - "+str(id[0]))	
		return render_template("home.html")
	return render_template("recipe.html", form=form)
	
@app.route('/search', methods = ['POST', 'GET'])
def recipesearch():
	form = SearchForm()
	if request.method == 'POST' and form.validate_on_submit():
		name = request.form['name']
		return redirect(url_for("searchresults",search=name))
	return render_template("search.html",form=form)

@app.route('/search/<search>')
def searchresults(search):
	cursor = mysql.connection.cursor()
	likeString = "%" + search + "%"
	cursor.execute('''Select recid,RDescription from Recipe where RDescription like %s ''',(likeString,))
	results = cursor.fetchall()
	mysql.connection.commit()
	cursor.close()
	return render_template("results.html",results=results)
	
@app.route('/recipe/<recipeid>')
def viewrecipe(recipeid):
	cursor = mysql.connection.cursor()
	cursor.execute('''call recipe_display(%s) ''',(recipeid,))
	recipe = cursor.fetchone()
	cursor.close()
	return render_template("recipedisplay.html",recipe=recipe)
	
@app.route('/meal', methods = ['POST', 'GET'])
def meal():
	form = MealForm()
	print("OMEGA")
	if request.method == 'POST' and form.validate_on_submit():
		recid = request.form['recid']
		#name = request.form['name']
		mealtype = request.form['mealtype']
		numofcals = request.form['numofcals']
		photo = form.photo.data
		file = secure_filename(photo.filename)
		photo.save(os.path.join(app.config['UPLOAD_FOLDER'],file))
		#measurement = request.form['measurement']
		cursor = mysql.connection.cursor()
		cursor.execute(''' select RDescription from recipe where recid = %s''',(recid,))
		name = cursor.fetchone()
		cursor.execute(''' INSERT INTO Meal (RecID, NameofMeal,TypeofMeal,NumofCalories,ImageFileName) VALUES(%s,%s,%s,%s,%s)''',(recid, name,mealtype,numofcals,file))
		mysql.connection.commit()
		cursor.close()
		flash("Succesfully added recipe!!")
		return render_template("home.html")
	return render_template("meal.html", form=form)

@app.route('/mealplan', methods = ['POST', 'GET'])
def getcaloriecount():
	form = CalorieForm()
	if request.method == 'POST' and form.validate_on_submit():
		caloriecount = request.form['caloriecount']
		print("check1\n\n\n\n\n\n",caloriecount)
		if caloriecount == "":
			return redirect(url_for("mealplan",caloriecount=0))
		else:
			return redirect(url_for("mealplan",caloriecount=caloriecount))
	return render_template("caloriecount.html",form=form)

@app.route('/mealplan/<caloriecount>')
def mealplan(caloriecount):
	cursor = mysql.connection.cursor()
	cursor.execute('''Delete from MealPlan where Email = %s ''',(session['email'],))
	mysql.connection.commit()
	days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
	cursor.execute('''select min(numofcalories) from Meal''')
	minimumcalories = cursor.fetchone()
	for dow in days:
		cals = []
		meal = []
		for i in range(3):
			if int(caloriecount) >= minimumcalories[0]:
				cursor.execute('''select MealID from Meal where numofcalories <= %s''',(caloriecount,))
				meals = cursor.fetchall()
			else:
				cursor.execute('''select MealID from Meal''')
				meals = cursor.fetchall()
			print("check\n\n\n\n",meals,len(meals),meals[0])
			num = random.randint(0,len(meals)-1)
			print("check2",num)
			mealid = meals[num]
			cursor.execute('''select NumofCalories from meal where MealID = %s''',(mealid,))
			cal = cursor.fetchone()
			cal = cal[0]
			cursor.execute('''select NameofMeal from meal where MealID = %s''',(mealid,))
			name = cursor.fetchone()
			name = name[0]
			meal.append(name)
			cals.append(cal)
		#numofmeals = random.randint(1,7)
		#numofmeals = 3
		#days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
		#dow = random.randint(0,6)
		print("check4\n\n\n",meal)
		totalcalories = sum(cals)
		#print("check3\n\n\n\n\n\n",mealid[0],numofmeals,totalcalories)
		cursor.execute(''' INSERT INTO MealPlan (Email, breakfast,lunch,dinner,TotalCalories,DayofWeek) VALUES(%s,%s,%s,%s,%s,%s)''',(session['email'],meal[0],meal[1],meal[2],totalcalories,dow))
		#cursor.execute(''' INSERT INTO User (FirstName,LastName,Age,Gender,Email) VALUES(%s,%s,%s,%s,%s)''',(fname,lname,age,gender,email))
		mysql.connection.commit()
	cursor.execute('''select breakfast,lunch,dinner,TotalCalories,DayofWeek  from MealPlan where Email = %s''',(session['email'],))
	plan = cursor.fetchall()
	print("check3\n\n\n\n\n\n",plan)
	cursor.close()
	return render_template("mealplan.html", plan=plan[:7])

@app.route('/mealpland')
def mealpland():
	cursor = mysql.connection.cursor()
	cursor.execute('''select breakfast,lunch,dinner,TotalCalories,DayofWeek  from MealPlan where Email = %s''',(session['email'],))
	plan = cursor.fetchall()
	cursor.close()
	return render_template("mealplan.html", plan=plan[:7])

@app.route('/kitchen', methods = ['POST', 'GET'])
def kitchen():
	'''form = KitchenForm()
	if request.method == 'POST' and form.validate_on_submit():
		for i in range(18):
			ingred = request.form['ingredid']'''
	cursor = mysql.connection.cursor()		
	if request.method == 'POST':
		lst = request.form.getlist('add')
		cursor.execute('''delete from kitchen where email = %s''',(session['email'],))
		print("check3\n\n\n\n\n\n",lst)
		for i in lst:
			cursor.execute('''insert into kitchen(ingredientid,email) values(%s,%s)''',(i,session['email']))
		mysql.connection.commit()
		flash("Succesfully updated your kitchen!!")
		return render_template("home.html")
	cursor.execute('''select IngredientName,IngredientID from Ingredients''')
	names = cursor.fetchall()
	lst = [False]*len(names)
	cursor.execute('''select IngredientID  from kitchen where Email = %s''',(session['email'],))
	lst2 = cursor.fetchall()
	#for i in lst2:
		#lst[i-1] = True
	cursor.close()
	return render_template("kitchen.html", names=names,count=len(names))

@app.route('/shoppinglist')
def shoppinglist():
	cursor = mysql.connection.cursor()
	cursor.execute('''call generate_shopping_list(%s)''',(session['email'],))
	lst = cursor.fetchall()
	cursor.close()
	return render_template("shoppinglist.html",lst=lst)
	
def addingred(names):
	cursor = mysql.connection.cursor()
	cursor.execute('''insert into kitchen(Email,IngredientID) Values(%s,%s)''',(session['email'],names))
	cursor.close()

def removeingred():
	pass

	

def get_uploaded_images():
	rootdir = os.getcwd()
	lst=[]
	for subdir, dirs, files in os.walk(rootdir + '/uploads'):
		for file in files:
			lst.append(file)
	return lst
	
@app.route("/uploads/<filename>")
def get_image(filename):
	rootdir = os.getcwd()
	return send_from_directory(rootdir + "/" + app.config['UPLOAD_FOLDER'],filename)

@app.route("/files")
def files():
	if session.get('logged in'):
		abort(401)
	lst = get_uploaded_images()
	return render_template('files.html',lst=lst)


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
