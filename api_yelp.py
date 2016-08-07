import os

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import pydash as _

consumer_key = os.getenv('YELP_CONSUMER_KEY', '')
consumer_secret = os.getenv('YELP_CONSUMER_SECRET', '')
token = os.getenv('YELP_TOKEN', '')
token_secret = os.getenv('YELP_TOKEN_SECRET', '')

oauth = Oauth1Authenticator(
  consumer_key=consumer_key,
  consumer_secret=consumer_secret,
  token=token,
  token_secret=token_secret
)
client = Client(oauth)

def obtain(search_term, category):
  
  results = client.search(search_term)
  
  if not results.businesses:
    return None
  
  return {
    "metadata": {
      "type": "yelp-information",
      "term": search_term,
      "category": category
    },
    "data": {
      "name": results.businesses[0].name,
      "description": results.businesses[0].location.cross_streets,
      "ratings": results.businesses[0].rating,
      "images": results.businesses[0].image_url
    }
  }
  