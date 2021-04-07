# ID#(s) - 620133240, 620131566, 620128524, 620132398
from faker import Faker
import os
import random
import mysql.connector
#pip install random
#python -m pip install mysql-connector-python
#python -m pip install Faker

db_connection = mysql.connector.connect(
host="localhost",
user="root",
passwd="",
database="MealPlanOrganizer"
 )
cursor = db_connection.cursor()

def populate_database():
	gender = ['Male','Female']
	fake = Faker()
	for i in range(200000):
		fname = fake.first_name() 
		lname = fake.last_name()
		email = fake.unique.email()
		age = random.randint(12,80)
		num = random.randint(0,1)
		cursor.execute(''' INSERT INTO User (FirstName,LastName,Age,Gender,Email) VALUES(%s,%s,%s,%s,%s)''',(fname,lname,age,gender[num],email))

	for i in range(1000):
			step1 = fake.sentence()
			step2 = fake.sentence()
			step3 = fake.sentence()
			cursor.execute(''' INSERT INTO Instruction (Step1,Step2,Step3) VALUES(%s,%s,%s)''',(step1,step2,step3))

	ingredients_list = ['chicken',
		'flour',
		'beans',
		'rice',
		'bacon',
		'cheese',
		'ketchup',
		'mustard',
		'strawberry',
		'egg',
		'orange',
		'lime',
		'wheat',
		'vegetable oil',
		'sugar',
		'corn syrup',
		'vanilla extract',
		'milk']
	measurements_list = [
		'1/4 Cup',
		'1/2 Cup',
		'3/4 Cup',
		'1 Cup',
		'2 tps',
		'1 tbps',
		'50g',
		'100g',
		'100ml',
		'200ml']
	for i in range(len(ingredients_list)):
		measurement = measurements_list[random.randint(0,len(measurements_list)-1)]
		name = ingredients_list[i]
		cursor.execute(''' INSERT INTO Ingredients (IngredientName,Measurement) VALUES(%s,%s)''',(name,measurement))
	
	cursor.execute('''select count(InstructionID) from instruction''')
	instruccount = cursor.fetchone()
	cursor.execute('''select count(IngredientID) from ingredients''')
	ingredcount = cursor.fetchone()
	diets = ['vegan','vegetarian','paleo','keto','mediterranean','pescatarian']
	my_word_list = [
	'danish','cheesecake','sugar',
	'Lollipop','wafer','Gummies',
	'sesame','Jelly','beans',
	'pie','bar','Ice','oat','sweet','tasty','delicious' ]
	db_connection.commit()
	for i in range(600000):
		instrucid = random.randint(1,instruccount[0])
		ingredid = random.randint(1,ingredcount[0])
		creationdate = fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=5)
		desc = fake.sentence(ext_word_list=my_word_list)
		num = random.randint(0,5)
		servings = random.randint(1,6)
		cursor.execute(''' INSERT INTO Recipe (InstructionID,IngredientID,CreationDate,RDescription,TypeofDiet,Servings) VALUES(%s,%s,%s,%s,%s,%s)''',(instrucid,ingredid,creationdate,desc,diets[num],servings))
	db_connection.commit()
	cursor.close()

populate_database()