import tweepy
consumer_key="O8bYrgMxKG0A9SNdQP5JI1zQ6"
consumer_secret="Td43C3kupvfOyGdsXDndmBrwE5Vq2sWKStwXjJpkvMhnnZZAOT"
access_token="1014050132-W4WIcK3XauGD7xoUXbOPtYmB7FTq82rS93JpykA"
access_token_secret="QOvgDAMwMYCKvfq8eCHLEAhLGepdP0fj4W9O5o0FZ4zOd"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

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
