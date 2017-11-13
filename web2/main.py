from flask import Flask, render_template, request, redirect, url_for, Response, json
from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd
from collections import defaultdict

#from models import db

db = SQLAlchemy()

application = Flask(__name__)
application.config['DEBUG'] = True

POSTGRES = {
    'user': 'datashark',
    'pw': 'datashark',
    'db': 'datasharkdb',
    'host':  'datashark-database.cwnzqu4zi2kl.us-west-1.rds.amazonaws.com',
    'port': '5432'
}
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(application)


@application.route("/", methods=['GET', 'POST'])
def main():
    return render_template('index.html')


@application.route("/home", methods=['POST'])
def home():
    return redirect('/')

@application.route('/results', methods=['POST'])
def results():
    categ = request.form['categ']
    table_name = "fitbit_daily_activity_summary"
    col_names = get_columns(table_name)
    temp = str(col_names)
    print(temp)
    temp = temp.replace("'", '"')
    print(temp)
    import ast
    col_names = ast.literal_eval(temp)
    print(col_names)
    return render_template('left-sidebar.html', table = table_name, cols=json.dumps(col_names))


@application.route('/execute', methods=['POST'])
def execute():
    print("execute called")
    query = request.form['query']
    print(query)
    df = pd.read_sql_query(query, db.engine)
    #df = pd.read_sql_query("select * from fitbit_daily_activity_summary", db.engine)
    csv = df.to_csv(index=False)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=data.csv"}
        )


@application.route('/insert', methods=['POST', 'GET'])
def insert():
    ## FOR DATASHARK
    print("HERE v3")
    print(request.form)
    access_token = request.form['accessToken']
    client_id = '228MWF'
    client_secret = 'ed16cd1e79a28f00c990e304b87f3bb6'

    ## FOR SPECIFIC USER - ROHAN - CONFIDENTIAL
    #access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U1pMN0YiLCJhdWQiOiIyMjhNV0YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA3NDM5OTc3LCJpYXQiOjE1MDc0MTExNzd9.RGXvH1fUoAJjhqGEwP_wsjL7MYkP2xvzQgs36BtxlvA'
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

@application.route('/insertInsta', methods=['POST', 'GET'])
def insertInsta():
    ## FOR DATASHARK
    print("HERE v3")
    print(request.form)
    #access_token = request.form['accessToken']
    client_id = '228MWF'
    client_secret = 'ed16cd1e79a28f00c990e304b87f3bb6'

    access_token = '3267610983.1677ed0.2240d1a1d85f49a48a5a58a90cb40703'
    #access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U1pMN0YiLCJhdWQiOiIyMjhNV0YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA3NDM5OTc3LCJpYXQiOjE1MDc0MTExNzd9.RGXvH1fUoAJjhqGEwP_wsjL7MYkP2xvzQgs36BtxlvA'
    refresh_token = 'bbb44b3a0e05a4235b9bd837481d4796372ee3d51d5a1f4b2b82af4c85216534'
    print("Access: " + access_token)
    header = {'Authorization': 'Bearer ' + access_token}
    

    



def get_columns(categ):
    cmd = 'select col, description from metadata where table_name=:val'
    result = db.session.execute(cmd, {'val': categ})
    db.session.commit()
    return result.fetchall()

if __name__ == "__main__":
    application.run()
