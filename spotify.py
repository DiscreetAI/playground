#request authorization
#dependencies: spotipy, requests
import sys
import spotipy
import spotipy.util as util
authorization = "https://accounts.spotify.com/authorize"
client_Id = "78fd273678d54d5cb6f352307b578a42"
client_Secret = "6ce54cfc4e1b46059b7c2f433e4178d9"
response_Type = "code"
redirect_Uri = "https://datasharkofficial.github.io/"
scopes_ = "playlist-read-private playlist-read-collaborative user-library-read user-read-private user-read-birthdate user-read-email user-follow-read user-top-read user-read-recently-played"
#SET USERNAME
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()
#SET TOKEN PROGRAMMATICALLY FROM MOBILE APP
token = util.prompt_for_user_token(username, scopes_, client_id=client_Id,
client_secret=client_Secret, redirect_uri=redirect_Uri)

if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
    sp.trace = False
    ranges = ['short_term', 'medium_term', 'long_term']
    for range in ranges:
        print("range:", range)
        results = sp.current_user_top_artists(time_range=range, limit=50)
        for i, item in enumerate(results['items']):
            print(i, item['name'])
        results = sp.current_user_top_tracks(time_range=range, limit=50)
        for i, item in enumerate(results['items']):
            print(i, item['name'], '//', item['artists'][0]['name'])
