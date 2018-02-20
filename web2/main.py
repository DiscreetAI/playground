from flask import Flask, render_template, request, redirect, url_for, Response, json, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd
from collections import defaultdict
from pandas.io.sql import SQLTable
import datetime

application = Flask(__name__)
application.config['DEBUG'] = True

POSTGRES = {
    'user': 'datashark',
    'pw': 'datashark',
    'db': 'datasharkdb',
    'host': 'datasharkdatabase.cwnzqu4zi2kl.us-west-1.rds.amazonaws.com',
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
    # execute()
    #insertUber()
    table_name = "fitbit_daily_activity_summary"
    col_names = get_columns(table_name)
    temp = str(col_names)
    print(temp)
    temp = temp.replace("'", '"')
    # print(temp)
    import ast
    col_names = ast.literal_eval(temp)
    # print(col_names)
    return render_template('left-sidebar.html', table=table_name, cols=json.dumps(col_names))


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
    # query = request.form['query']
    # print(query)
    query = 'create table fb_calories (date_of_activity varchar(255), calories int, user_id varchar(255));'
    df = pd.read_sql_query(query, db.engine)
    # query = 'create table ubero (num real, display_name varchar(255), distance real, end_time real, latitude real, longitude real, product_id varchar(255), request_id varchar(255), request_time real, start_time real, status varchar(255))'
    # query = 'create table lyft_table (canceled_by varchar(255), origin varchar(255), line_items varchar(255), passenger varchar(255), distance_miles real, duration_seconds int, dropoff varchar(255),  charges varchar(255), requested_at varchar(255), price varchar(255), destination varchar(255), driver varchar(255), status varchar(255), pickup varchar(255), route_url varchar(255), ride_id varchar(255), vehicle varchar(255), ride_type varchar(255), pricing_details_url varchar(255), ride_profile varchar(255))'
    # df = pd.read_sql_query(query, db.engine)
    return
    # df = pd.read_sql_query("select * from fitbit_daily_activity_summary", db.engine)
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
    # access_token = request.form['accessToken']
    client_id = '22CH8Y'
    client_secret = '92ef15bf527e8c3684ff6f54517d235e'

    ## FOR SPECIFIC USER - ROHAN - CONFIDENTIAL
    # access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U1pMN0YiLCJhdWQiOiIyMjhNV0YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA3NDM5OTc3LCJpYXQiOjE1MDc0MTExNzd9.RGXvH1fUoAJjhqGEwP_wsjL7MYkP2xvzQgs36BtxlvA'
    access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U05IVDgiLCJhdWQiOiIyMkNIOFkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTE3OTAzNTAxLCJpYXQiOjE1MTc4NzQ3MDF9.k62Hg6BmpTmXfdiXwXE9A9ZuFAFs2fsTG-RqMoitWDw'
    refresh_token = 'bbb44b3a0e05a4235b9bd837481d4796372ee3d51d5a1f4b2b82af4c85216534'
    encode64 = 'MjJDSDhZOjkyZWYxNWJmNTI3ZThjMzY4NGZmNmY1NDUxN2QyMzVl'
    print("Access: " + access_token)
    header = {'Authorization': 'Bearer ' + access_token}
    month_days = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30, '10': 31, '11': 30,
                  '12': 31}
    now = datetime.datetime.now()
    year = now.year
    year2 = year - 3
    month = now.month
    month2 = month
    day = now.day
    day2 = day + 2
    if day < 10:
        day = '0' + str(day)
    if day2 < 10:
        day2 = '0' + str(day2)
    elif day >= month_days[month]:
        day2 = '01'
        month2 += 1
        if month2 == 13:
            month2 = 1
    if month < 10:
        month = '0' + str(month)
    if month2 < 10:
        month2 = '0' + str(month2)
    date = str(year) + "-" + str(month) + "-" + str(day)
    date2 = str(year2) + "-" + str(month2) + "-" + str(day2)
    print(date)
    print(date2)
    ## FOR FITBIT DAILY ACTIVITY SUMMARY

    fitbit_daily_activity_summary_values = ['lightlyActiveMinutes', 'caloriesBMR', 'caloriesOut', 'marginalCalories',
                                            'fairlyActiveMinutes', 'veryActiveMinutes', 'sedentaryMinutes',
                                            'restingHeartRate', 'elevation', 'activityCalories', 'activeScore',
                                            'floors', 'steps']
    steps_endpoint = 'https://api.fitbit.com/1/user/-/activities/steps/date/' + date2 + '/' + date + '.json'
    profile_endpoint = 'https://api.fitbit.com/1/user/-/profile.json'
    print(steps_endpoint)
    response2 = requests.get(profile_endpoint, headers=header)
    parsed2 = json.loads(response2.text)
    user_id = parsed2['user']['encodedId']
    print(user_id)
    # print(parsed2)

    calories_endpoint = 'https://api.fitbit.com/1/user/-/activities/calories/date/' + date2 + '/' + date + '.json'
    response = requests.get(steps_endpoint, headers=header)
    parsed = json.loads(response.text)
    # print(parsed)
    steps = parsed['activities-steps']
    dict = defaultdict(lambda: [])
    count = 0
    for activity in steps:
        # endpoint = fitbit_daily_activity_summary_endpoint.format(str(date).zfill(2))
        # print(parsed)
        # print(date
        # print(date2)
        # print(activity)
        val = int(activity['value'])
        if val >= 0:
            dict['user_id'].append(user_id)
            dict['date_of_activity'].append(activity['dateTime'])
            dict['calories'].append(val)
            count += 1
        '''
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
        '''
    steps_df = pd.DataFrame(dict)

    print('steps')
    print(steps_df)
    steps_df.to_sql('fbcalories', db.engine, if_exists='append', index=False)

    response = requests.get(steps_endpoint, headers=header)
    parsed = json.loads(response.text)
    steps = parsed['activities-steps']
    dict = defaultdict(lambda: [])
    count = 0
    for activity in steps:
        # endpoint = fitbit_daily_activity_summary_endpoint.format(str(date).zfill(2))
        # print(parsed)
        # print(date
        # print(date2)
        # print(activity)
        val = int(activity['value'])
        if val >= 0:
            dict['user_id'].append(user_id)
            dict['date_of_activity'].append(activity['dateTime'])
            dict['steps'].append(val)
            count += 1
        '''
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
        '''
    steps_df = pd.DataFrame(dict)

    print('steps')
    print(steps_df)
    steps_df.to_sql('fbsteps', db.engine, if_exists='append', index=False)

    print("finished you monkeys")


@application.route('/insert/Lyft', methods=['POST', 'GET'])
def insertLyft():
    client_id = 'xWcQoJgCDyyx'
    # access_token = 's8FIXnUQkMe0huSo7UcRxiGJ9AMLKT/eBM6ILrsEeyGeMV6/sgU8/cn1EVB8AtohUqBe0EkfECVxjAMVrKZbdZaeLSeFH9jWbWiCOHL8CosCHcxR7fG6cFM='
    refresh_token = 'C5BR2cGIWK4aMeHBMtmiNnGlp9Fi4lkmlxchUS5Nf0nDzwj2nhUdjqOdvV29sy+38C/OvCTcSMGxanMwEn0zj03FT4AkypGFr0q9pOgdrdzA'
    client_secret = 've3ul8VMMiiQ7zrft33S2gzAy8258436'
    print("Access: " + access_token)
    access_token = request.form['accessToken']
    header = {'Authorization': 'Bearer ' + access_token}
    lyft_endpoint = 'https://api.lyft.com/v1/rides?start_time=2015-12-01T21:04:22Z'
    lyft_values = ['ride_history']
    dict = defaultdict(lambda: [])
    response = requests.get(lyft_endpoint, headers=header)
    parsed = json.loads(response.text)
    print(parsed['ride_history'])
    history = parsed['ride_history']
    normal = ['origin', 'line_items', 'passenger', 'requested_at', 'price', 'destination', 'status', 'route_url',
              'ride_id', 'ride_type', 'pricing_details_url', 'ride_profile']
    bad = ['distance_miles', 'duration_seconds', 'dropoff', 'charges', 'pickup']
    weird = ['vehicle', 'driver']
    # bad = ['dropoff_lat', 'dropoff_lng', 'dropoff_time', '']
    for ride in history:
        if 'vehicle' not in ride.keys():
            dict['vehicle'].append(None)
        if 'driver' not in ride.keys():
            dict['driver'].append(None)
        if 'canceled_by' in ride.keys(): from flask import Flask, render_template, request, redirect, url_for, Response, \
            json, jsonify


from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd
from collections import defaultdict
from pandas.io.sql import SQLTable
import datetime

application = Flask(__name__)
application.config['DEBUG'] = True

POSTGRES = {
    'user': 'datashark',
    'pw': 'datashark',
    'db': 'datasharkdb',
    'host': 'datasharkdatabase.cwnzqu4zi2kl.us-west-1.rds.amazonaws.com',
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
    # execute()
    insertUber()
    table_name = "fitbit_daily_activity_summary"
    col_names = get_columns(table_name)
    temp = str(col_names)
    print(temp)
    temp = temp.replace("'", '"')
    # print(temp)
    import ast
    col_names = ast.literal_eval(temp)
    # print(col_names)
    return render_template('left-sidebar.html', table=table_name, cols=json.dumps(col_names))


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
    # query = request.form['query']
    # print(query)
    query = 'create table fb_calories (date_of_activity varchar(255), calories int, user_id varchar(255));'
    df = pd.read_sql_query(query, db.engine)
    # query = 'create table ubero (num real, display_name varchar(255), distance real, end_time real, latitude real, longitude real, product_id varchar(255), request_id varchar(255), request_time real, start_time real, status varchar(255))'
    # query = 'create table lyft_table (canceled_by varchar(255), origin varchar(255), line_items varchar(255), passenger varchar(255), distance_miles real, duration_seconds int, dropoff varchar(255),  charges varchar(255), requested_at varchar(255), price varchar(255), destination varchar(255), driver varchar(255), status varchar(255), pickup varchar(255), route_url varchar(255), ride_id varchar(255), vehicle varchar(255), ride_type varchar(255), pricing_details_url varchar(255), ride_profile varchar(255))'
    # df = pd.read_sql_query(query, db.engine)
    return
    # df = pd.read_sql_query("select * from fitbit_daily_activity_summary", db.engine)
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
    # access_token = request.form['accessToken']
    client_id = '22CH8Y'
    client_secret = '92ef15bf527e8c3684ff6f54517d235e'

    ## FOR SPECIFIC USER - ROHAN - CONFIDENTIAL
    # access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U1pMN0YiLCJhdWQiOiIyMjhNV0YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA3NDM5OTc3LCJpYXQiOjE1MDc0MTExNzd9.RGXvH1fUoAJjhqGEwP_wsjL7MYkP2xvzQgs36BtxlvA'
    access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U05IVDgiLCJhdWQiOiIyMkNIOFkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTE3OTAzNTAxLCJpYXQiOjE1MTc4NzQ3MDF9.k62Hg6BmpTmXfdiXwXE9A9ZuFAFs2fsTG-RqMoitWDw'
    refresh_token = 'bbb44b3a0e05a4235b9bd837481d4796372ee3d51d5a1f4b2b82af4c85216534'
    encode64 = 'MjJDSDhZOjkyZWYxNWJmNTI3ZThjMzY4NGZmNmY1NDUxN2QyMzVl'
    print("Access: " + access_token)
    header = {'Authorization': 'Bearer ' + access_token}
    month_days = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30, '10': 31, '11': 30,
                  '12': 31}
    now = datetime.datetime.now()
    year = now.year
    year2 = year - 3
    month = now.month
    month2 = month
    day = now.day
    day2 = day + 2
    if day < 10:
        day = '0' + str(day)
    if day2 < 10:
        day2 = '0' + str(day2)
    elif day >= month_days[month]:
        day2 = '01'
        month2 += 1
        if month2 == 13:
            month2 = 1
    if month < 10:
        month = '0' + str(month)
    if month2 < 10:
        month2 = '0' + str(month2)
    date = str(year) + "-" + str(month) + "-" + str(day)
    date2 = str(year2) + "-" + str(month2) + "-" + str(day2)
    print(date)
    print(date2)
    ## FOR FITBIT DAILY ACTIVITY SUMMARY

    fitbit_daily_activity_summary_values = ['lightlyActiveMinutes', 'caloriesBMR', 'caloriesOut', 'marginalCalories',
                                            'fairlyActiveMinutes', 'veryActiveMinutes', 'sedentaryMinutes',
                                            'restingHeartRate', 'elevation', 'activityCalories', 'activeScore',
                                            'floors', 'steps']
    steps_endpoint = 'https://api.fitbit.com/1/user/-/activities/steps/date/' + date2 + '/' + date + '.json'
    profile_endpoint = 'https://api.fitbit.com/1/user/-/profile.json'
    print(steps_endpoint)
    response2 = requests.get(profile_endpoint, headers=header)
    parsed2 = json.loads(response2.text)
    user_id = parsed2['user']['encodedId']
    print(user_id)
    # print(parsed2)

    calories_endpoint = 'https://api.fitbit.com/1/user/-/activities/calories/date/' + date2 + '/' + date + '.json'
    response = requests.get(steps_endpoint, headers=header)
    parsed = json.loads(response.text)
    # print(parsed)
    steps = parsed['activities-steps']
    dict = defaultdict(lambda: [])
    count = 0
    for activity in steps:
        # endpoint = fitbit_daily_activity_summary_endpoint.format(str(date).zfill(2))
        # print(parsed)
        # print(date
        # print(date2)
        # print(activity)
        val = int(activity['value'])
        if val >= 0:
            dict['user_id'].append(user_id)
            dict['date_of_activity'].append(activity['dateTime'])
            dict['calories'].append(val)
            count += 1
        '''
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
        '''
    steps_df = pd.DataFrame(dict)

    print('steps')
    print(steps_df)
    steps_df.to_sql('fbcalories', db.engine, if_exists='append', index=False)

    response = requests.get(steps_endpoint, headers=header)
    parsed = json.loads(response.text)
    steps = parsed['activities-steps']
    dict = defaultdict(lambda: [])
    count = 0
    for activity in steps:
        # endpoint = fitbit_daily_activity_summary_endpoint.format(str(date).zfill(2))
        # print(parsed)
        # print(date
        # print(date2)
        # print(activity)
        val = int(activity['value'])
        if val >= 0:
            dict['user_id'].append(user_id)
            dict['date_of_activity'].append(activity['dateTime'])
            dict['steps'].append(val)
            count += 1
        '''
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
        '''
    steps_df = pd.DataFrame(dict)

    print('steps')
    print(steps_df)
    steps_df.to_sql('fbsteps', db.engine, if_exists='append', index=False)

    print("finished you monkeys")


@application.route('/insert/Lyft', methods=['POST', 'GET'])
def insertLyft():
    client_id = 'xWcQoJgCDyyx'
    # access_token = 's8FIXnUQkMe0huSo7UcRxiGJ9AMLKT/eBM6ILrsEeyGeMV6/sgU8/cn1EVB8AtohUqBe0EkfECVxjAMVrKZbdZaeLSeFH9jWbWiCOHL8CosCHcxR7fG6cFM='
    refresh_token = 'C5BR2cGIWK4aMeHBMtmiNnGlp9Fi4lkmlxchUS5Nf0nDzwj2nhUdjqOdvV29sy+38C/OvCTcSMGxanMwEn0zj03FT4AkypGFr0q9pOgdrdzA'
    client_secret = 've3ul8VMMiiQ7zrft33S2gzAy8258436'
    print("Access: " + access_token)
    access_token = request.form['accessToken']
    header = {'Authorization': 'Bearer ' + access_token}
    lyft_endpoint = 'https://api.lyft.com/v1/rides?start_time=2015-12-01T21:04:22Z'
    lyft_values = ['ride_history']
    dict = defaultdict(lambda: [])
    response = requests.get(lyft_endpoint, headers=header)
    parsed = json.loads(response.text)
    print(parsed['ride_history'])
    history = parsed['ride_history']
    normal = ['origin', 'line_items', 'passenger', 'requested_at', 'price', 'destination', 'status', 'route_url',
              'ride_id', 'ride_type', 'pricing_details_url', 'ride_profile']
    bad = ['distance_miles', 'duration_seconds', 'dropoff', 'charges', 'pickup']
    weird = ['vehicle', 'driver']
    # bad = ['dropoff_lat', 'dropoff_lng', 'dropoff_time', '']
    for ride in history:
        if 'vehicle' not in ride.keys():
            dict['vehicle'].append(None)
        if 'driver' not in ride.keys():
            dict['driver'].append(None)
        if 'canceled_by' in ride.keys():
            for key in bad:
                dict[key].append(None)
            for key in normal:
                dict[key].append(str(ride[key]))
            for key in weird:
                if key in ride.keys():
                    dict[key].append(str(ride[key]))
            dict['canceled_by'].append(ride['canceled_by'])
        else:
            dict['canceled_by'].append(None)
            for key in ride.keys():
                if key != 'beacon_color':
                    dict[key].append(str(ride[key]))
    print(dict)
    for key in dict.keys():
        print(key, len(dict[key]))
    lyft_df = pd.DataFrame(dict)
    lyft_df.to_sql('lyft_table', db.engine, if_exists='append', index=False)
    print("finished lyft")


@application.route('/insert/Uber', methods=['POST', 'GET'])
def insertUber():
    pd.read_sql_table('yum', db.engine)
    print('yum')
    # uber_endpoint = 'https://api.uber.com/v1.2/products?latitude=37.7759792&longitude=-122.41823'
    # access_token = 'KA.eyJ2ZXJzaW9uIjoyLCJpZCI6IldmM2wzdWZUUkx1YWZtVEZpY2Ira0E9PSIsImV4cGlyZXNfYXQiOjE1MTk1MzU2MzIsInBpcGVsaW5lX2tleV9pZCI6Ik1RPT0iLCJwaXBlbGluZV9pZCI6MX0.XyzA3qM5CRTzg0y3J05g9U8ntd61JMSRoyxy2jy8oQY'
    # access_token = request.form['accessToken']
    access_token = 'KA.eyJ2ZXJzaW9uIjoyLCJpZCI6ImpoaUtCMDJQVERxSHJ2YVNydzdrQkE9PSIsImV4cGlyZXNfYXQiOjE1MjEzNzM2ODEsInBpcGVsaW5lX2tleV9pZCI6Ik1RPT0iLCJwaXBlbGluZV9pZCI6MX0.j3og-jnfY1IDm8njcKt9P4ba53IMiUrCR61Ng-hqkXg'
    header = {'Authorization': 'Bearer ' + access_token, 'Accept-Language': 'en_US', 'Content-Type': 'application/json'}
    '''
    auth_flow = AuthorizationCodeGrant(
        'cvcaMdUYPlqkoFtrEECV1bbEEBnmpd5K',
        <SCOPES>,
        'J7vY3yBGZr19EIrtibQZPhJm2qPulKy-Zs2VMMQz',
        'https://datasharkofficial.github.io/'
    )
    '''
    # auth_url = auth_flow.get_authorization_url()
    # response = client.get_user_activity()
    # history = response.json
    # print(history)
    print(SQLAlchemy.metadata)
    print("my dude")
    uber_endpoint2 = "https://api.uber.com/v1.2/history"
    uber_endpoint3 = "https://api.uber.com/v1.2/requests/"
    response = requests.get(uber_endpoint2, headers=header)
    # print(response.text)
    parsed = json.loads(response.text)
    print(parsed)
    for p in parsed['history']:
        req_id = p['request_id']
        endpoint = uber_endpoint3 + str(req_id)
        response2 = requests.get(endpoint, headers=header)
        parsed2 = json.loads(response2.text)
        print(parsed2)
    return
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
    # db.session.execute('select * from uber;')
    # db.engine.execute('insert into table t')
    # db.session.execute("INSERT INTO uber (display_name, distance, end_time, latitude, longitude, product_id, request_id, request_time, start_time, status) VALUES ('b', '1', '1', '1', '1', 'a', 'a', '1', '1', 'c');")
    db.session.commit()
    ubero.to_sql(name='yum', con=db.engine, if_exists='append', index=False)
    print("finished uber")


@application.route('/insert/Instagram/', methods=['POST', 'GET'])
def insertInsta():
    ## FOR DATASHARK
    print("HERE v3")
    print(request.form)
    r = request.args
    # access_token = request.form['accessToken']
    client_id = '228MWF'
    client_secret = 'ed16cd1e79a28f00c990e304b87f3bb6'

    access_token = '3267610983.1677ed0.2240d1a1d85f49a48a5a58a90cb40703'
    # access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U1pMN0YiLCJhdWQiOiIyMjhNV0YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA3NDM5OTc3LCJpYXQiOjE1MDc0MTExNzd9.RGXvH1fUoAJjhqGEwP_wsjL7MYkP2xvzQgs36BtxlvA'
    refresh_token = 'bbb44b3a0e05a4235b9bd837481d4796372ee3d51d5a1f4b2b82af4c85216534'
    print("Access: " + access_token)
    header = {'Authorization': 'Bearer ' + access_token}


@application.route('/transactionHistory/', methods=['GET'])
def transactionHistory():
    print(request.form)
    r = request.args
    return jsonify({'Uber': 2.25})


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
    # result = db.session.execute(cmd, {'val': categ})
    # result = db.session.execute('create table uber (display_name varchar(255), distance real, end_time real, latitude real, longitude real, product_id varchar(255), request_id varchar(255), request_time real, start_time real, status varchar(255))')
    # result = db.session.execute('select * from fitbit_daily_activity_summary')
    # print(result.fetchall())

    result = db.session.execute(cmd, {'val': categ})
    db.session.commit()
    return result.fetchall()


if __name__ == "__main__":
    application.run()

    for key in bad:
        dict[key].append(None)
    for key in normal:
        dict[key].append(str(ride[key]))
    for key in weird:
        if key in ride.keys():
            dict[key].append(str(ride[key]))
    dict['canceled_by'].append(ride['canceled_by'])
else:
    dict['canceled_by'].append(None)
    for key in ride.keys():
        if key != 'beacon_color':
            dict[key].append(str(ride[key]))
print(dict)
for key in dict.keys():
    print(key, len(dict[key]))
lyft_df = pd.DataFrame(dict)
lyft_df.to_sql('lyft_table', db.engine, if_exists='append', index=False)
print("finished lyft")

'''
@application.route('/insert/Uber', methods=['POST', 'GET'])
def insertUber():
    pd.read_sql_table('yum', db.engine)
    print('yum')
    # uber_endpoint = 'https://api.uber.com/v1.2/products?latitude=37.7759792&longitude=-122.41823'
    # access_token = 'KA.eyJ2ZXJzaW9uIjoyLCJpZCI6IldmM2wzdWZUUkx1YWZtVEZpY2Ira0E9PSIsImV4cGlyZXNfYXQiOjE1MTk1MzU2MzIsInBpcGVsaW5lX2tleV9pZCI6Ik1RPT0iLCJwaXBlbGluZV9pZCI6MX0.XyzA3qM5CRTzg0y3J05g9U8ntd61JMSRoyxy2jy8oQY'
    # access_token = request.form['accessToken']
    access_token = 'KA.eyJ2ZXJzaW9uIjoyLCJpZCI6ImY0T0lqZi9yUWgrOVF1RGt0YlNWVVE9PSIsImV4cGlyZXNfYXQiOjE1MjEzNzE5NDQsInBpcGVsaW5lX2tleV9pZCI6Ik1RPT0iLCJwaXBlbGluZV9pZCI6MX0.0w9mSD-NFJALrvEDMmBMVjByy9prKIqKP64cjHkUR8U'
    header = {'Authorization': 'Bearer ' + access_token, 'Accept-Language': 'en_US', 'Content-Type': 'application/json'}
    
    auth_flow = AuthorizationCodeGrant(
        'cvcaMdUYPlqkoFtrEECV1bbEEBnmpd5K',
        <SCOPES>,
        'J7vY3yBGZr19EIrtibQZPhJm2qPulKy-Zs2VMMQz',
        'https://datasharkofficial.github.io/'
    )
    
    # auth_url = auth_flow.get_authorization_url()
    # response = client.get_user_activity()
    # history = response.json
    # print(history)
    print(SQLAlchemy.metadata)
    print("my dude")
    uber_endpoint2 = "https://api.uber.com/v1.2/history"
    uber_endpoint3 = "https://api.uber.com/v1.2/requests/"
    response = requests.get(uber_endpoint2, headers=header)
    # print(response.text)
    parsed = json.loads(response.text)
    for p in parsed['history']:
        req_id = p['request_id']
        endpoint = uber_endpoint3 + str(req_id)
        response2 = requests.get(endpoint, headers=header)
        parsed2 = json.loads(response2.text)
        print(parsed)
    break
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
    # db.session.execute('select * from uber;')
    # db.engine.execute('insert into table t')
    # db.session.execute("INSERT INTO uber (display_name, distance, end_time, latitude, longitude, product_id, request_id, request_time, start_time, status) VALUES ('b', '1', '1', '1', '1', 'a', 'a', '1', '1', 'c');")
    db.session.commit()
    ubero.to_sql(name='yum', con=db.engine, if_exists='append', index=False)
    print("finished uber")
'''

@application.route('/insert/Instagram/', methods=['POST', 'GET'])
def insertInsta():
    ## FOR DATASHARK
    print("HERE v3")
    print(request.form)
    r = request.args
    # access_token = request.form['accessToken']
    client_id = '228MWF'
    client_secret = 'ed16cd1e79a28f00c990e304b87f3bb6'

    access_token = '3267610983.1677ed0.2240d1a1d85f49a48a5a58a90cb40703'
    # access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U1pMN0YiLCJhdWQiOiIyMjhNV0YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA3NDM5OTc3LCJpYXQiOjE1MDc0MTExNzd9.RGXvH1fUoAJjhqGEwP_wsjL7MYkP2xvzQgs36BtxlvA'
    refresh_token = 'bbb44b3a0e05a4235b9bd837481d4796372ee3d51d5a1f4b2b82af4c85216534'
    print("Access: " + access_token)
    header = {'Authorization': 'Bearer ' + access_token}


@application.route('/transactionHistory/', methods=['GET'])
def transactionHistory():
    print(request.form)
    r = request.args
    return jsonify({'Uber': 2.25})


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
    # result = db.session.execute(cmd, {'val': categ})
    # result = db.session.execute('create table uber (display_name varchar(255), distance real, end_time real, latitude real, longitude real, product_id varchar(255), request_id varchar(255), request_time real, start_time real, status varchar(255))')
    # result = db.session.execute('select * from fitbit_daily_activity_summary')
    # print(result.fetchall())

    result = db.session.execute(cmd, {'val': categ})
    db.session.commit()
    return result.fetchall()


if __name__ == "__main__":
    application.run()
