from flask import Flask, render_template, request, redirect, url_for, Response, json, jsonify
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd
from collections import defaultdict
from uber_rides.auth import AuthorizationCodeGrant
from pandas.io.sql import SQLTable

def _execute_insert(self, conn, keys, data_iter):
    data = [dict((k, v) for k, v in zip(keys, row)) for row in data_iter]
    print("Using monkey-patched _execute_insert", data)
    
    conn.execute(self.insert_statement().values(data))

SQLTable._execute_insert = _execute_insert
#from models import db

application = Flask(__name__)
application.config['DEBUG'] = True

POSTGRES = {
	'user': 'datashark',
	'pw': 'datashark',
	'db': 'datasharkdb',
	'host':  'datasharkdatabase.cwnzqu4zi2kl.us-west-1.rds.amazonaws.com',
	'port': '5432'
}
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db = SQLAlchemy(application)

@application.route("/", methods=['GET', 'POST'])
def main():
	return render_template('index.html')


@application.route("/home", methods=['POST'])
def home():
	return redirect('/')

@application.route('/results', methods=['POST'])
def results():
	categ = request.form['categ']
	#execute()
	insertUber()
	table_name = "fitbit_daily_activity_summary"
	col_names = get_columns(table_name)
	temp = str(col_names)
	print(temp)
	temp = temp.replace("'", '"')
	#print(temp)
	import ast
	col_names = ast.literal_eval(temp)
	#print(col_names)
	return render_template('left-sidebar.html', table = table_name, cols=json.dumps(col_names))


@application.route('/checkout', methods=['POST'])
def checkout():
	return render_template('checkout.html')


@application.route('/account', methods=['POST'])
def account():
	return render_template('account.html')


@application.route('/payment', methods=['POST'])
def payment():
	return render_template('payment.html')

@application.route('/execute', methods=['POST'])
def execute():
	print("execute called")
	#query = request.form['query']
	#print(query)
	query = 'drop table uber'
	df = pd.read_sql_query(query, db.engine)
	query = 'create table ubero (num real, display_name varchar(255), distance real, end_time real, latitude real, longitude real, product_id varchar(255), request_id varchar(255), request_time real, start_time real, status varchar(255))'
	df = pd.read_sql_query(query, db.engine)
	return
	#df = pd.read_sql_query("select * from fitbit_daily_activity_summary", db.engine)
	csv = df.to_csv(index=False)
	return Response(
		csv,
		mimetype="text/csv",
		headers={"Content-disposition": "attachment; filename=data.csv"}
		)


@application.route('/insert/Fitbit', methods=['POST', 'GET'])
def insert():
	## FOR DATASHARK
	print("HERE v3")
	print(request.form)
	#access_token = request.form['accessToken']
	client_id = '228MWF'
	client_secret = 'ed16cd1e79a28f00c990e304b87f3bb6'

	## FOR SPECIFIC USER - ROHAN - CONFIDENTIAL
	access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U1pMN0YiLCJhdWQiOiIyMjhNV0YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA3NDM5OTc3LCJpYXQiOjE1MDc0MTExNzd9.RGXvH1fUoAJjhqGEwP_wsjL7MYkP2xvzQgs36BtxlvA'
	refresh_token = 'bbb44b3a0e05a4235b9bd837481d4796372ee3d51d5a1f4b2b82af4c85216534'
	print("Access: " + access_token)
	header = {'Authorization': 'Bearer ' + access_token}


	## FOR FITBIT DAILY ACTIVITY SUMMARY

	fitbit_daily_activity_summary_values = ['lightlyActiveMinutes', 'caloriesBMR', 'caloriesOut', 'marginalCalories', 'fairlyActiveMinutes', 'veryActiveMinutes', 'sedentaryMinutes', 'restingHeartRate', 'elevation', 'activityCalories', 'activeScore', 'floors', 'steps']
	fitbit_daily_activity_summary_endpoint = 'https://api.fitbit.com/1/user/-/activities/date/2017-9-{0}.json'

	dict = defaultdict(lambda: [])

	for date in range(1, 30):
			endpoint = fitbit_daily_activity_summary_endpoint.format(str(date).zfill(2))
			response = requests.get(endpoint, headers=header)
			parsed = json.loads(response.text)
			print(parsed)
			return
			for value in fitbit_daily_activity_summary_values:
				if value in parsed['summary']:
					dict[value.lower()].append(parsed['summary'][value])
				else:
					dict[value.lower()].append(None)
			if 'distances' in parsed['summary']:
				distances = parsed['summary']['distances']
				if len(distances) > 0:
					if 'distance' in distances[0]:
						dict['distance'].append(distances[0]['distance'])

	fitbit_daily_activity_summary_df = pd.DataFrame(dict)

	fitbit_daily_activity_summary_df.to_sql('fitbit_daily_activity_summary', db.engine, if_exists='append', index=False)

	print("finished you monkeys")

@application.route('/insert/Lyft', methods=['POST', 'GET'])
def insertLyft():
		client_id = 'xWcQoJgCDyyx'
		#access_token = request.form['accessToken']
		client_secret = 've3ul8VMMiiQ7zrft33S2gzAy8258436'
		print("Access: " + access_token)
		header = {'Authorization': 'Bearer ' + access_token}
		lyft_endpoint = 'https://api.lyft.com/v1/rides'
		lyft_values = ['ride_history']

		dict = defaultdict(lambda: [])

		for date in range(1, 30):
			response = requests.get(lyft_endpoint, headers=header)
			parsed = json.loads(response.text)
			print(parsed)
			for value in lyft_values:
				if value in parsed['summary']:
					dict[value.lower()].append(parsed['summary'][value])
				else:
					dict[value.lower()].append(None)
			if 'distances' in parsed['summary']:
				distances = parsed['summary']['distances']
				if len(distances) > 0:
					if 'distance' in distances[0]:
						dict['distance'].append(distances[0]['distance'])
		lyft_df = pd.DataFrame(dict)
		lyft_df.to_sql('lyft', db.engine, if_exists='append', index=False)

		print("finished lyft")

@application.route('/insert/Uber', methods=['POST', 'GET'])
def insertUber():
	pd.read_sql_table('yum', db.engine)
	print('yum')
	session = Session(server_token='BNgvucsIimnyDZxb9bDY1oH6Wi-Du1cK0pWqZYWS')
	client = UberRidesClient(session)
	#uber_endpoint = 'https://api.uber.com/v1.2/products?latitude=37.7759792&longitude=-122.41823'
	access_token = 'KA.eyJ2ZXJzaW9uIjoyLCJpZCI6IldmM2wzdWZUUkx1YWZtVEZpY2Ira0E9PSIsImV4cGlyZXNfYXQiOjE1MTk1MzU2MzIsInBpcGVsaW5lX2tleV9pZCI6Ik1RPT0iLCJwaXBlbGluZV9pZCI6MX0.XyzA3qM5CRTzg0y3J05g9U8ntd61JMSRoyxy2jy8oQY'
	header = {'Authorization': 'Bearer ' + access_token, 'Accept-Language': 'en_US', 'Content-Type': 'application/json'}
	'''
	auth_flow = AuthorizationCodeGrant(
		'cvcaMdUYPlqkoFtrEECV1bbEEBnmpd5K',
		<SCOPES>,
		'J7vY3yBGZr19EIrtibQZPhJm2qPulKy-Zs2VMMQz',
		'https://datasharkofficial.github.io/'
	)
	'''
	#auth_url = auth_flow.get_authorization_url()
	#response = client.get_user_activity()
	#history = response.json
	#print(history)
	print(SQLAlchemy.metadata)
	print("my dude")
	uber_endpoint2 = "https://api.uber.com/v1.2/history"
	response = requests.get(uber_endpoint2, headers=header)
	#print(response.text)
	parsed = json.loads(response.text)

	print(parsed['history'])
	history = parsed['history']
	print(history[0])
	print(len(history))
	dict = defaultdict(lambda: [])
	for trip in history:
		for key in trip.keys():
			if key == 'start_city':
				for k in trip['start_city']:
					dict[k.lower()].append(trip['start_city'][k])
			else:
				dict[key.lower()].append(trip[key])
	print(dict)
	ubero = pd.DataFrame(dict)
	# uber_df.to_csv('uber.csv')
	# ubero = pd.read_csv('uber.csv')
	# print(ubero['status'])
	#db.session.execute('select * from uber;')
	#db.engine.execute('insert into table t')
	#db.session.execute("INSERT INTO uber (display_name, distance, end_time, latitude, longitude, product_id, request_id, request_time, start_time, status) VALUES ('b', '1', '1', '1', '1', 'a', 'a', '1', '1', 'c');")
	db.session.commit()
	ubero.to_sql(name = 'yum', con=db.engine, if_exists='append', index=False)
	print("finished uber")

@application.route('/insert/Instagram/', methods=['POST', 'GET'])
def insertInsta():
	## FOR DATASHARK
	print("HERE v3")
	print(request.form)
	r = request.args
	#access_token = request.form['accessToken']
	client_id = '228MWF'
	client_secret = 'ed16cd1e79a28f00c990e304b87f3bb6'

	access_token = '3267610983.1677ed0.2240d1a1d85f49a48a5a58a90cb40703'
	#access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U1pMN0YiLCJhdWQiOiIyMjhNV0YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA3NDM5OTc3LCJpYXQiOjE1MDc0MTExNzd9.RGXvH1fUoAJjhqGEwP_wsjL7MYkP2xvzQgs36BtxlvA'
	refresh_token = 'bbb44b3a0e05a4235b9bd837481d4796372ee3d51d5a1f4b2b82af4c85216534'
	print("Access: " + access_token)
	header = {'Authorization': 'Bearer ' + access_token}
	
@application.route('/transactionHistory/', methods=['GET'])
def transactionHistory():
	print(request.form)
	r = request.args
	return jsonify({'Fitbit': 10.02, 'Lyft': 2.25})
	
@application.route('/loginUser', methods=['POST'])
def loginUser():
	print(request.form)
	r = request.get_json()
	return jsonify({'userID': 1246743, 'address': '0x56ABCD'})

@application.route('/createUser', methods=['POST'])
def createUser():
	print(request.form)
	r = request.get_json()
	return jsonify({'userID': 1246743, 'address': '0x56ABCD'})

@application.route('/datasharkServices', methods=['GET'])
def returnServices():
	return jsonify({'services': 'Fitbit, Uber, Lyft'})

@application.route('/userServices/', methods=['GET'])
def userServices():
	r = request.args
	return jsonify({'Fitbit': 'activity, heartrate, location, nutrition, profile, settings, sleep, social, weight',
					'Uber': 'history, places, all_trips, request_receipt, request',
					'Lyft': 'public_profile, rides.read'})

@application.route('/allServices/', methods=['GET'])
def allServices():
	r = request.args
	return jsonify({'Fitbit': 'activity, heartrate, location, nutrition, profile, settings, sleep, social, weight',
					'Uber': 'history, places, all_trips, request_receipt, request',
					'Lyft': 'public_profile, rides.read'})

def get_columns(categ):
	cmd = 'select col, description from metadata where table_name=:val'
	#result = db.session.execute(cmd, {'val': categ})
	#result = db.session.execute('create table uber (display_name varchar(255), distance real, end_time real, latitude real, longitude real, product_id varchar(255), request_id varchar(255), request_time real, start_time real, status varchar(255))')
	#result = db.session.execute('select * from fitbit_daily_activity_summary')
	#print(result.fetchall())
	
	result = db.session.execute(cmd, {'val': categ})
	db.session.commit()
	return result.fetchall()

if __name__ == "__main__":
	application.run()
