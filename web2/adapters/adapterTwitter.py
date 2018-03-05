import tweepy

@application.route('/insert/Twitter', methods=['POST', 'GET'])
def insert_twitter():
	token, token_secret = session['token']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

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

###TLDR this API is super easy to use and ref documentation is great.
