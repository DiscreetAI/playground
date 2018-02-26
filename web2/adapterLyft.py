from application import *

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