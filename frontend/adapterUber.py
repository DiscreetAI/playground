from application import *

@application.route('/insert/Uber', methods=['POST', 'GET'])
def insert_uber():
    #pd.read_sql_table('yum', db.engine)
    #print('yum')
    # uber_endpoint = 'https://api.uber.com/v1.2/products?latitude=37.7759792&longitude=-122.41823'
    # access_token = 'KA.eyJ2ZXJzaW9uIjoyLCJpZCI6IldmM2wzdWZUUkx1YWZtVEZpY2Ira0E9PSIsImV4cGlyZXNfYXQiOjE1MTk1MzU2MzIsInBpcGVsaW5lX2tleV9pZCI6Ik1RPT0iLCJwaXBlbGluZV9pZCI6MX0.XyzA3qM5CRTzg0y3J05g9U8ntd61JMSRoyxy2jy8oQY'
    # client_id = 'cvcaMdUYPlqkoFtrEECV1bbEEBnmpd5K'
    # client_secret = 'J7vY3yBGZr19EIrtibQZPhJm2qPulKy-Zs2VMMQz'
    access_token = request.form['accessToken']
    session_token = request.form['uid']
    user_endpoint = 'http://auth.dataagora.com/auth/user/'
    header = {"Authorization": "Token " + session_token}
    response = requests.get(user_endpoint, headers = header)
    parsed = json.loads(response)
    if 'pk' in parsed:
        user_id = parsed['pk']
    else:
        user_id = None #or some kind of error handling
    #access_token = 'KA.eyJ2ZXJzaW9uIjoyLCJpZCI6IlFtbFFuTnllUWFhaWYzMXpQYVR0VXc9PSIsImV4cGlyZXNfYXQiOjE1MjI4MDkxOTcsInBpcGVsaW5lX2tleV9pZCI6Ik1RPT0iLCJwaXBlbGluZV9pZCI6MX0.T67EHU7zifkLLQBLOiMyKbacugyjss-zI155GU52AwU'
    header = {'Authorization': 'Bearer ' + access_token, 'Accept-Language': 'en_US', 'Content-Type': 'application/json'}
    # auth_url = auth_flow.get_authorization_url()
    # response = client.get_user_activity()
    # history = response.json
    # print(history)
    print(SQLAlchemy.metadata)
    print("my dude")
    uber_endpoint = "https://api.uber.com/v1.2/me"
    response = requests.get(uber_endpoint, headers=header)
    # print(response.text)
    parsed = json.loads(response.text)
    #user_id = parsed['uuid']
    '''
    #uncomment when session is resolved
    if session['user_id'] in user_id_df['user_id']:
        user_id_df.uber[user_id_df.user_id == user_id] = user_id
    else: 
        row = [session['user_id'], None, user_id, None, None, None, None]
        user_id_df.loc[len(user_id_df.index)] = row
    '''
    uber_endpoint2 = "https://api.uber.com/v1.2/history"
    uber_endpoint3 = "https://api.uber.com/v1.2/requests/"
    response = requests.get(uber_endpoint2, headers=header)
    # print(response.text)
    parsed = json.loads(response.text)
    print(parsed)
    dict = defaultdict(lambda: [])
    '''
    for p in parsed['history']:
        req_id = p['request_id']
        receipt_end = uber_request_template(req_id, 'receipt')
        response1 = requests.get(receipt_end, headers=header)
        parsed1 = json.loads(response1.text)
        dict['request_id'].append(req_id)
        for k,v in parsed1.items():
            if k != 'request_id':
                dict[k].append(v)
    '''
    #print(dict)
    #request_df = pd.DataFrame(dict)
    #print(request_df)
    #u.to_sql(name='uberrequests', con=db.engine, if_exists='append', index=False)
    print(parsed['history'])
    history = parsed['history']
    print(history[0])
    print(len(history))
    dict = defaultdict(lambda: [])
    for trip in history:
        for key in trip.keys():
            dict['user_id'].append(user_id)
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
    ubero.to_sql(name='uberhistory', con=db.engine, if_exists='append', index=False)
    print("finished uber")

def get_profile_info(accessToken, header):
    uber_endpoint = "https://api.uber.com/v1.2/me"
    response = requests.get(uber_endpoint2, headers=header)
    parsed = json.loads(response.text)

def uber_request_template(request_id, endpoint):
    return "https://api.uber.com/v1.2/requests/{rid}/{end}".format(rid=request_id, end = endpoint)