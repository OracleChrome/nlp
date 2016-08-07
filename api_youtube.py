import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pydash as _


DEVELOPER_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def obtain(search_term, category):
  
  try:
    youtube = build(
      YOUTUBE_API_SERVICE_NAME, 
      YOUTUBE_API_VERSION,
      developerKey=DEVELOPER_KEY
    )
  except HttpError:
    return None
  
  try:
    search_response = youtube.search().list(
      q=search_term,
      part="id,snippet",
      maxResults=1
    ).execute()
  except HttpError:
    return None
  
  video_list = search_response.get("items", [])
  if not video_list:
    return None

  return {
    "metadata": {
      "type": "youtube-video",
      "term": search_term,
      "category": category
    },
    "data": {
      "name": _.get(video_list, '0.title', None),
      "link": "https://www.youtube.com/embed/%s" % 
      _.get(video_list, '0.id.videoId')
    }
  }
