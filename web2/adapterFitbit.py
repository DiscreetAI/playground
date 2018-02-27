from application import *

@application.route('/insert/Fitbit', methods=['POST', 'GET'])
def insert_fitbit():
    ## FOR DATASHARK
    print("HERE v3")
    print(request.form)
    # access_token = request.form['accessToken']
    client_id = '22CH8Y'
    client_secret = '92ef15bf527e8c3684ff6f54517d235e'

    ## FOR SPECIFIC USER - ROHAN - CONFIDENTIAL
    # access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U1pMN0YiLCJhdWQiOiIyMjhNV0YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTA3NDM5OTc3LCJpYXQiOjE1MDc0MTExNzd9.RGXvH1fUoAJjhqGEwP_wsjL7MYkP2xvzQgs36BtxlvA'
    access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U05IVDgiLCJhdWQiOiIyMkNIOFkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTE5NjU0Nzc5LCJpYXQiOjE1MTk2MjU5Nzl9.BTditAoHSOrapVJ9M9augfTbRXDZC8kh6pzIeMY0FrE'
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
    elif day >= month_days[str(month)]:
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
    return getProfileInfo(access_token, header)
    user_id = parsed2['user']['encodedId']
    print(user_id)
    # print(parsed2)
    return
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

def get_profile_info(accessToken, header):
    profile_endpoint = 'https://api.fitbit.com/1/user/-/profile.json'
    response2 = requests.get(profile_endpoint, headers=header)
    parsed2 = json.loads(response2.text)
    data = parsed2['user']
    dicto = defaultdict(lambda: [])
    for key,value in data.items():
        if type(value) != list and type(value) != dict:
            dicto[str(key)].append(value)
            print(value)
    data = pd.DataFrame(dicto)
    print(data)
    data.to_sql('fbprofile', db.engine, if_exists='append', index=False)
    #print(parsed2)
    return
