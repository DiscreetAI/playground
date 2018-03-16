#request authorization
#dependencies: spotipy, requests
import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib
from application import *
# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
#Client Keys
CLIENT_ID = "78fd273678d54d5cb6f352307b578a42"
CLIENT_SECRET = "6ce54cfc4e1b46059b7c2f433e4178d9"
# Server-side Parameters
CLIENT_SIDE_URL = "https://demo.dataagora.com"
# PORT = 5000
REDIRECT_URI = "{}/get/Spotify/".format(CLIENT_SIDE_URL)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()
SCOPE = "playlist-read-private playlist-read-collaborative user-library-read user-read-private user-read-birthdate user-read-email user-follow-read user-top-read user-read-recently-played"
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}
@application.route('/oauth/Spotify/')
def spotify_oauth():
    # Auth Step 1: Authorization
    scopes = ['user-read-private', 'user-read-email', 'user-read-birthdate', 'playlist-read-private']
    #url_args = "&".join(["{}={}".format(key,urllib.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = "{url}/?client_id={client_id}&response_type=code&redirect_uri={redirect}&state={state}&scope=".format(url=SPOTIFY_AUTH_URL, client_id=CLIENT_ID, redirect=REDIRECT_URI, state='')
    for scope in scopes:
        auth_url += scope + '%20'
    auth_url = auth_url[:-3]
    print(auth_url)
    return redirect(auth_url)
@application.route('/get/Spotify/', methods=['POST', 'GET'])
def get_spotify():
# Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    print(access_token)
    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)
    
    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"]
    #return 'OK'
    return render_template('payment.html')
# #SET USERNAME
# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Usage: %s username" % (sys.argv[0],))
#     sys.exit()
# #SET TOKEN PROGRAMMATICALLY FROM MOBILE APP
# token = util.prompt_for_user_token(username, scopes_, client_id=client_Id,
# client_secret=client_Secret, redirect_uri=redirect_Uri)

# if token:
#     sp = spotipy.Spotify(auth=token)
#     playlists = sp.user_playlists(username)
#     for playlist in playlists['items']:
#         if playlist['owner']['id'] == username:
#             print(playlist['name'])
#             print('  total tracks', playlist['tracks']['total'])
#             results = sp.user_playlist(username, playlist['id'],
#                 fields="tracks,next")
#             tracks = results['tracks']
#             show_tracks(tracks)
#             while tracks['next']:
#                 tracks = sp.next(tracks)
#                 show_tracks(tracks)
#     results = sp.current_user_saved_tracks()
#     for item in results['items']:
#         track = item['track']
#         print(track['name'] + ' - ' + track['artists'][0]['name'])
#     sp.trace = False
#     ranges = ['short_term', 'medium_term', 'long_term']
#     for range in ranges:
#         print("range:", range)
#         results = sp.current_user_top_artists(time_range=range, limit=50)
#         for i, item in enumerate(results['items']):
#             print(i, item['name'])
#         results = sp.current_user_top_tracks(time_range=range, limit=50)
#         for i, item in enumerate(results['items']):
#             print(i, item['name'], '//', item['artists'][0]['name'])

# #TODO: Put this into a database. @AMOG
