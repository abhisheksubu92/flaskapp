import os
import pandas as pd 
#from sklearn.extern import joblib
import dill as pickle
from flask import Flask, jsonify, request,render_template, redirect,url_for

from sqlalchemy import create_engine

app = Flask(__name__)


# @app.route('/')
# def index():
# 	return render_template('main.html')


@app.route('/')
def dashboard():
    return render_template("dashboard.html")



@app.route('/',methods = ['POST','GET'])
def prediction():


	"Here we send pandas data frame as payload from API call"


	csv_database = create_engine('sqlite:///test_database.db')

	" Now we load the get request from the user about the loan ID"

	clf = 'model_v1.pk'
	# if test.empty:
	# 	return(bad_request())
	# else:
	id = request.form['id']
	value = pd.read_sql_query('''SELECT Distinct * FROM test where test.Loan_ID ='{}' '''.format(id), csv_database,index_col = 'index')
	#test['Dependents'] = [str(x) for x in list(test['Dependents'])]
	loan_ids = value['Loan_ID']
	#Load the saved model
	print("Loading the model...")
	loaded_model = None
	with open(clf,'rb') as f:
		loaded_model = pickle.load(f)
	predictions = loaded_model.predict(value)
	# prediction_series = list(pd.Series(predictions))
	# final_predictions = pd.DataFrame(list(zip(loan_ids, prediction_series)))
	# responses = jsonify(predictions=final_predictions.to_json(orient="records"))
	#responses.status_code = 200

	# return redirect(prediction=predictions)
	return render_template('dashboard.html',prediction=predictions)


if __name__=='__main__':
	
	app.run(debug=True)

