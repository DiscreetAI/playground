from application import *
consumer_key="O8bYrgMxKG0A9SNdQP5JI1zQ6"
consumer_secret="Td43C3kupvfOyGdsXDndmBrwE5Vq2sWKStwXjJpkvMhnnZZAOT"
access_token="1014050132-W4WIcK3XauGD7xoUXbOPtYmB7FTq82rS93JpykA"
access_token_secret="QOvgDAMwMYCKvfq8eCHLEAhLGepdP0fj4W9O5o0FZ4zOd"
@application.route('/get/Twitter', methods = ['POST', 'GET'])
def get_twitter():
	request_token = session['request_token']
    del session['request_token']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    session['token'] = (auth.access_token, auth.access_token_secret)

    return redirect('/app')

@application.route('/oauth/Twitter', methods = ['POST', 'GET'])
def twitter_oauth():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)