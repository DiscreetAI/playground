from application import *

@application.route('/insert/Lyft', methods=['POST', 'GET'])
def insert_lyft():
    client_id = 'xWcQoJgCDyyx'
    access_token = 'e7oVoPTz/ySGT3Avl709lh6dhMar2AeAHRpkg2qfmDmt5Nm4dVQRWmT2fcovUriEOeWb5DBiZbxN2rGVkFUVqEPeGbxinSiCLPgOh/c8xyq3TUyzrfunoGk='
    refresh_token = 'C5BR2cGIWK4aMeHBMtmiNnGlp9Fi4lkmlxchUS5Nf0nDzwj2nhUdjqOdvV29sy+38C/OvCTcSMGxanMwEn0zj03FT4AkypGFr0q9pOgdrdzA'
    client_secret = 've3ul8VMMiiQ7zrft33S2gzAy8258436'
    print("Access: " + access_token)
    #access_token = request.form['accessToken']
    header = {'Authorization': 'Bearer ' + access_token}
    lyft_endpoint = 'https://api.lyft.com/v1/profile'
    response = requests.get(lyft_endpoint, headers=header)
    parsed = json.loads(response.text)
    user_id = parsed['id']
    '''
    #uncomment when session is resolved
    if session['user_id'] in user_id_df['user_id']:
        user_id_df.lyft[user_id_df.user_id == user_id] = user_id
    else: 
        row = [session['user_id'], None, user_id, None, None, None, None]
        user_id_df.loc[len(user_id_df.index)] = row
    '''
    lyft_endpoint = 'https://api.lyft.com/v1/rides?start_time=2015-12-01T21:04:22Z'
    lyft_values = ['ride_history']
    response = requests.get(lyft_endpoint, headers=header)
    parsed = json.loads(response.text)
    #print(parsed['ride_history'])
    history = parsed['ride_history']
    normal = ['origin', 'passenger', 'requested_at', 'price', 'destination', 'status', 'route_url',
              'ride_id', 'ride_type', 'pricing_details_url', 'ride_profile']
    bad = ['distance_miles', 'duration_seconds', 'dropoff', 'charges', 'pickup']
    weird = ['vehicle', 'driver', 'beacon_color', 'line_items']
    # bad = ['dropoff_lat', 'dropoff_lng', 'dropoff_time', '']
    dict1 = defaultdict(lambda: [])
    dict2 = defaultdict(lambda: [])
    for ride in history:
        if 'canceled_by' in ride.keys():
            for k in normal:
                v = ride[k]
                if isinstance(v, dict):
                    for k2, v2 in v.items():
                        new_k = k + "_" + k2
                        if v2 != None:
                            dict1[new_k].append(v2)
                else:
                    dict1[k].append(v)
            dict1['canceled_by'].append(ride['canceled_by'])
        if 'canceled_by' not in ride.keys():
            for k,v in ride.items():
                if k not in weird:
                    if k == 'charges':
                        v = v[0]
                    if isinstance(v, dict):
                        for k2, v2 in v.items():
                            new_k = k + "_" + k2
                            dict2[new_k].append(v2)
                    else:
                        dict2[k].append(v)
        '''
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
        '''
    lyft_df1 = pd.DataFrame(dict1)
    lyft_df2 = pd.DataFrame(dict2)
    for k,v in dict1.items():
        print(v[0])
    for k,v in dict2.items():
        print(k, v[0])
    print(lyft_df1)
    print(lyft_df2)
    lyft_df2.to_sql('lyft_history', db.engine, if_exists='append', index=False)
    lyft_df1.to_sql('lyft_historycancelled', db.engine, if_exists='append', index=False)

    print("finished lyft")