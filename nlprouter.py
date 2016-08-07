import os
import sys
import json

import dotenv

import webpage_process
import api_freebase
import api_googlemaps
import api_twitter
import api_wikipedia
import api_yelp
import api_youtube


dotenv.load_dotenv(os.path.realpath('./.env'))

def main():
  _, payload = sys.argv
  
  try:
    payload = json.loads(payload)
  except BaseException:
    return []
  
  if "webpageText" not in payload:
    return []
  
  content = payload["webpageText"]
  
  content = webpage_process.cleanse_tags(content)
  ner_tuple_list = webpage_process.ner_tagging(content)
  ner_tuple_list = webpage_process.reduce_neighbors(ner_tuple_list)
  picked_ner_tuple_list = webpage_process.pick_most_important(ner_tuple_list, 20)
  

if __name__ == "__main__":
  main()
  