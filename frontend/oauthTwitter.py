from application import *
import tweepy

consumer_key = "O8bYrgMxKG0A9SNdQP5JI1zQ6"
consumer_secret = "Td43C3kupvfOyGdsXDndmBrwE5Vq2sWKStwXjJpkvMhnnZZAOT"
access_token = "1014050132-W4WIcK3XauGD7xoUXbOPtYmB7FTq82rS93JpykA"
access_token_secret = "QOvgDAMwMYCKvfq8eCHLEAhLGepdP0fj4W9O5o0FZ4zOd"
# callback = 'https://demo.dataagora.com/get/Twitter/'
callback = 'https://demo.dataagora.com/get/Twitter'
session = {}


@application.route('/get/Twitter/')
def get_twitter():
    print('hola hola')
    request_token = session['request_token']
    print(request_token)
    del session['request_token']
    print('herev2')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    print('got here!')
    verifier = request.args.get('oauth_verifier')
    print(verifier)
    auth.get_access_token(verifier)
    print('herev1')
    session['token'] = (auth.access_token, auth.access_token_secret)
    print(session['token'])
    print('GOT TO ADAPTER')
    token, token_secret = session['token']
    print('FOUND TOKEN!')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    print('GOT AUTH!')
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    print('GOT API!')
    # return api.me()

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
    user = api.get_user('twitter')
    print(user.screen_name)
    print(user.followers_count)
    for friend in user.friends():
        print(friend.screen_name)
    my_tweets = api.user_timeline()
    for tweet in my_tweets:
        print(tweet.text)
    my_retweets = api.retweets_of_me()
    for tweet in my_retweets:
        print(tweet.text)
    return render_template('payment.html')


# return redirect('/insert/Twitter')

@application.route('/oauth/Twitter/')
def twitter_oauth():
    key = 'wvoJgqYFBsQjUyA3I7e4htbeN'
    secret = 'ZU0cWkW6ouLpMLbUiBLq7uKbtL2ytdXVQeIPCY2ED24HHZ77Fq'
    auth = tweepy.OAuthHandler(key, secret, callback)
    url = auth.get_authorization_url()
    request_token = url.split('=')[1]
    # session['request_token'] = auth.request_token
    # request_token = auth.request_token
    url = 'https://api.twitter.com/oauth/authenticate?oauth_token={}'.format(request_token)
    print(url)
    return redirect(url)


@application.route('/insert/Twitter/')
def insert_twitter():
    print('GOT TO ADAPTER')
    token, token_secret = session['token']
    print('FOUND TOKEN!')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    print('GOT AUTH!')
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    print('GOT API!')
    return api.me()

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
    user = api.get_user('twitter')
    print(user.screen_name)
    print(user.followers_count)
    for friend in user.friends():
        print(friend.screen_name)
    my_tweets = api.user_timeline()
    for tweet in my_tweets:
        print(tweet.text)
    my_retweets = api.retweets_of_me()
    for tweet in my_retweets:
        print(tweet.text)
