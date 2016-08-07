import os

import twitter

def obtain(search_term, category):
  
  consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
  consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
  access_token_key = os.getenv('TWITTER_TOKEN')
  access_token_secret = os.getenv('TWITTER_TOKEN_SECRET')
  
  api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token_key,
    access_token_secret=access_token_secret
  )
  
  try:
    tweets = api.GetSearch(
      term="%s" % search_term
    )
  except BaseException:
    return None

  return {
    "metadata": {
      "type": "twitter-tweet",
      "term": search_term,
      "category": "category"
    },
    "data": {
      "author": tweets[0].user.name,
      "authorImage": tweets[0].user.profile_image_url,
      "tweet": tweets[0].text
    }
  }
  
  