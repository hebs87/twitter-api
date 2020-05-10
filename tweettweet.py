import env
# Code copied from the tweepy docs
import tweepy
import time

auth = tweepy.OAuthHandler(env.CONSUMER_KEY, env.CONSUMER_SECRET)
auth.set_access_token(env.ACCESS_TOKEN, env.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# List public tweets in timeline
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

# Print information about myself
user = api.me()
print(user)


def limit_handler(cursor):
    """
    Handles Twitter's rate limit - keeps going until it hits the rate limit, and waits for a second once it hits
    the limit before proceeding again
    """
    try:
        while True:
            yield cursor.next()
    except StopIteration:
        return
    except tweepy.RateLimitError:
        time.sleep(1)


# Generous bot - always follows back any followers
# Wrap our cursor in the limit_handler function - if we have many items
for follower in limit_handler(tweepy.Cursor(api.followers).items()):
    if follower.name == 'Directus':
        follower.follow()


# Search bot - searches based on specified term
search_string = 'python'
number_of_tweets = 2

for tweet in limit_handler(tweepy.Cursor(api.search, search_string).items(number_of_tweets)):
    try:
        # Like the tweet
        tweet.favorite()
        # Retweet the tweet
        tweet.retweet()
        print('I liked that tweet')
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break
