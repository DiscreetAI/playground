from oauth import *
from adapters import *
from application import *

hasAge = {'fitbit': True, 'uber': False, 'lyft': False}
hasGender = {'fitbit': True, 'uber': False, 'lyft': False}
hasCity = {'fitbit': True, 'uber': False, 'lyft': False}
idNames = {'fitbit': 'encodedID', 'uber':'uiud', 'lyft':'userID'}

@application.route("/", methods=['GET', 'POST'])
def main():
    return render_template('index.html')


@application.route("/home", methods=['POST'])
def home():
    return redirect('/')

@application.route('/results', methods=['POST'])
def results():
    if 'test' in request.form:
        categ = request.form['test']
    else:
        categ = 'lol'
    #return execute()
    #insert_fitbit()
    if categ == 'Fitbit':
        return fitbit_oauth()
    elif categ == 'Uber':
        return uber_oauth()
    elif categ == 'Lyft':
        return lyft_oauth()
    elif categ == 'Twitter':
        return twitter_oauth()
    table_name = "fitbit_daily_activity_summary"
    col_names = get_columns(table_name)
    temp = str(col_names)
    #print(temp)
    temp = temp.replace("'", '"')
    # print(temp)
    import ast
    col_names = ast.literal_eval(temp)
    maxUsers = -1
    if 'categ' in request.form:
        if request.form['categ'] == 'Fitbit':
            maxUsers = get_user_count('user_id', 'fb_activities')
            print(maxUsers)

    # print(col_names)
    return render_template('left-sidebar.html', table=table_name, cols=json.dumps(col_names), users=maxUsers)

def get_table(tableName):
    query = "select * from {};".format(tableName)
    df = pd.read_sql_query(query, db.engine)
    return df 

def get_user_count(colName, tableName):
    query = "select count(distinct {col_name}) as count from {table_name};".format(col_name=colName, table_name=tableName)
    df = pd.read_sql_query(query, db.engine)
    return df['count'][0] 

#userDF is dataframe of userids with corresponding metadata.
#dfArr is array of tuples (dataframe, api) to be filtered
def fake_filter(userInfo, dfArr, minAge=0, maxAge=200, city=None, gender=None):
    filtereDFs = []
    for df, api in dfArr:
        if not hasAge[api]:
            tempUser = userInfo[userInfo['age'] != None]
            merged = pd.merge(df, userInfo, left_on=idNames[api], right_on='userid', how='inner')
            merged = merged[df.columns + ['age']]
            df = merged
        df = df[df['age'] > minAge]
        df = df[df['age'] < maxAge]
        if not hasCity[api]:
            tempUser = userInfo[userInfo['city'] != None]
            merged = pd.merge(df, userInfo, left_on=idNames[api], right_on='userid', how='inner')
            merged = merged[df.columns + ['city']]
            df = merged
        if city != None:
            df = df[df['city'] == city]
        if not hasGender[api]:
            tempUser = userInfo[userInfo['gender'] != None]
            merged = pd.merge(df, userInfo, left_on=idNames[api], right_on='userid', how='inner')
            merged = merged[df.columns + ['gender']]
            df = merged
            if gender != None:
                df = df[df['gender'] == gender]
        filtereDFs.append(df)
    return filteredDFs

#Assume given a dataframe where for each user, there is 1 for each API if user has data from API (0 otherwise), and demographic information.
def count(userInfo, api):
    return userInfo[userInfo['age'] != None & userInfo['city'] != None & userInfo['gender'] != None & userInfo['city'] != None & userInfo[api] == 1]        
        
    
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
    query = 'select * from fb_activities;'
    df = pd.read_sql_query(query, db.engine)
    # query = 'create table ubero (num real, display_name varchar(255), distance real, end_time real, latitude real, longitude real, product_id varchar(255), request_id varchar(255), request_time real, start_time real, status varchar(255))'
    # query = 'create table lyft_table (canceled_by varchar(255), origin varchar(255), line_items varchar(255), passenger varchar(255), distance_miles real, duration_seconds int, dropoff varchar(255),  charges varchar(255), requested_at varchar(255), price varchar(255), destination varchar(255), driver varchar(255), status varchar(255), pickup varchar(255), route_url varchar(255), ride_id varchar(255), vehicle varchar(255), ride_type varchar(255), pricing_details_url varchar(255), ride_profile varchar(255))'
    # df = pd.read_sql_query(query, db.engine)
    # df = pd.read_sql_query("select * from fitbit_daily_activity_summary", db.engine)
    csv = df.to_csv(index=False)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=fb_activities.csv"}
    )


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

@application.route('/download/type/', methods=['POST'])
def download():
    print(request.form)
    r = request.get_json()
    datatype = r['type']
    clause = "select * from "
    # clause = // end selected table 
    df = pd.read_sql(db.session.execute(clause))
    if datatype.equals("csv"):
        return df.to_csv()
    elif datatype.equals("excel"):
        return df.to_excel()
    elif datatype.equals("json"):
        return df.to_json()

def get_columns(categ):
    cmd = 'select col, description from metadata where table_name=:val'
    # result = db.session.execute(cmd, {'val': categ})
    # result = db.session.execute('create table uber (display_name varchar(255), distance real, end_time real, latitude real, longitude real, product_id varchar(255), request_id varchar(255), request_time real, start_time real, status varchar(255))')
    # result = db.session.execute('select * from fitbit_daily_activity_summary')
    # print(result.fetchall())

    result = db.session.execute(cmd, {'val': categ})
    db.session.commit()
    return result.fetchall()


    
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
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from marshmallow import fields, Schema

application.config.update({
    'APISPEC_SPEC': APISpec(
        title='pets',
        version='v1',
        plugins=['apispec.ext.marshmallow'],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})
docs = FlaskApiSpec(application)

docs.register(insert_fitbit)
docs.register(insert_lyft)
docs.register(insert_uber)
docs.register(fitbit_oauth)
docs.register(lyft_oauth)
docs.register(uber_oauth)
docs.register(get_fitbit)
docs.register(get_lyft)
docs.register(get_uber)

if __name__ == "__main__":
    application.run()