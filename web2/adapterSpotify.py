from application import *

@application.route('/insert/Spotify', methods=['POST', 'GET'])
def insert_spotify():
    CLIENT_ID = "78fd273678d54d5cb6f352307b578a42"
    CLIENT_SECRET = "6ce54cfc4e1b46059b7c2f433e4178d9"
    access_token = "BQAEPazqLheMQs15UyMoy_0Yq7SP-9amQtEpeEjp6s2-RMI-"
    base_url = "https://api.spotify.com/v1/"
    header = {'Authorization': 'Bearer ' + access_token}
    endpoints = ['me/tracks', 'me/following?type=artist', 'me/top/artists', 'me/top/tracks']
    names = ['saved_tracks', 'followed_artists', 'top_artists', 'top_tracks']
    user_id = None
    for endpoint, name in zip(endpoints, names):
        response2 = requests.get(endpoint, headers=header)
        dicto = defaultdict(lambda: [])
        parsed2 = json.loads(response2.text)
        for item in parsed['items']:
            dicto['user_id'].append(user_id)
            for k,v in item.items():
                if not isinstance(v, dict):
                    dicto([k]).append(v)
        df = pd.DataFrame(dicto)
        df.to_sql('spotify_' + name,db.engine, if_exists='append', index=False)