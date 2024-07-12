import streamlit as st
import csv
import pickle as pk
import pandas as pd
import mysql.connector  		#importing database
from sklearn.preprocessing import OrdinalEncoder
ord_enc = OrdinalEncoder()

st.title('Covid19 classification Project')
st.write('Fill the following form')

database = mysql.connector.connect(host="localhost",
								   user="root",
								   password="",
								   database = "covid")
db = database.cursor()

#form start
Name = st.text_input("Enter name")
Cough_symptoms = st.radio("Cough symptoms", [True, False])
Fever = st.radio("Fever", [True, False])
Sore_throat = st.radio("Sore Throat", [True, False])
Shortness_of_breath	 = st.radio("Shortness of breath", [True, False])
Headache = st.radio("Headache", [True, False])
Age_60_above = st.selectbox("Is Age 60 above ?", ["Yes", "No"])
Sex = st.selectbox("Gender", ["male", "female"])
Known_contact = st.selectbox("Known Contact", ["Abroad", "Contact with confirmed","Other"])

if st.button("Submit"):

#Create a DataFrame
	df = pd.DataFrame({
		"Cough_symptoms":[Cough_symptoms],
		"Fever":[Fever],
		"Sore_throat":[Sore_throat],
		"Shortness_of_breath":[Shortness_of_breath],
		"Headache": [Headache],
		"Age_60_above":[Age_60_above],
		"Sex":[Sex],
		"Known_contact":[Known_contact]
		})

#Encoding the data
# df["Age_60_above"] = ord_enc.fit_transform(df[["Age_60_above"]]).astype('int')
# df["Sex"] = ord_enc.fit_transform(df[["Sex"]]).astype('int')
# df["Known_contact"] = ord_enc.fit_transform(df[["Known_contact"]]).astype('int')
	if Age_60_above == "No":
		df["Age_60_above"] = 0
	else:
		df["Age_60_above"] = 1

	if Sex == 'female':
		df["Sex"] = 0
	else:
		df["Sex"] = 1

	if Known_contact == "Abroad":
		df["Known_contact"] = 0
	elif Known_contact == "Other":
		df["Known_contact"] = 2
	else:
		df["Known_contact"] = 1

	# open a file, where you stored the pickled data
	file = open('model.pickle', 'rb')
	# dump information to that file
	my_model = pk.load(file)
	result = my_model.predict(df)
	if int(result) == 1:
		output = "Positive"
	else:
		output = "Negative"

	st.write(output)

	# close the file
	sql = f'''INSERT INTO corona (name,Cough_symptoms,Fever,Sore_throat,
	Shortness_of_breath,Headache,Age_60_above,Sex,Known_contact,Corona)
	 VALUES ('{Name}', {Cough_symptoms}, {Fever}, {Sore_throat}, {Shortness_of_breath}, {Headache}, 
	 '{Age_60_above}', '{Sex}', '{Known_contact}', '{output}');'''
	st.write(sql)
	db.execute(sql)
	database.commit()
	st.write("form Submitted!")

