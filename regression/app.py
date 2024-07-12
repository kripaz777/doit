import streamlit as st
import csv
import pickle as pk
import pandas as pd
import mysql.connector  		#importing database
from sklearn.preprocessing import OrdinalEncoder
ord_enc = OrdinalEncoder()

#database connection
database = mysql.connector.connect(host="localhost",
								   user="root",
								   password="",
								   database = "covid")
db = database.cursor()

#create a form
name = st.text_input("Enter name")
Age = st.number_input("Enter Age", 20, 65)
Gender = st.selectbox("Gender", ["Male","Female"])
Experience = st.number_input("Enter Experience", 0, 40)
Education = st.selectbox("Education", ["Bachelor's","Master's","PhD"])

if st.button("Submit"):
	if Education == "Bachelor's":
		b = True; m = False; p = False

	elif Education == "Master's":
		b = False; m = True; p = False

	else:
		b = False; m = False; p = True

	df = pd.DataFrame({
		"Age":[Age],
		"Years of Experience":[Experience],
		#"Male":[Gender],
		"Bachelor's":[b],
		"Master's":[m],
		"PhD":[p],
		})

	#load and predict model
	file = open('model.pickle', 'rb')
	# dump information to that file
	my_model = pk.load(file)
	salary = my_model.predict(df)[0]
	st.write(salary)
	df['name'] = name
	df['salary'] = salary

	#sql query
	sql = f'''INSERT INTO salary (name,age,gender,experience,education,salary) 
	VALUES ('{name}', {Age}, '{Gender}',{Experience},"{Education}",{salary});'''
	st.write(sql)
	db.execute(sql)
	database.commit()
	st.write('Inserted into Database!')
	df