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


dotenv.load_dotenv(
  os.path.join(os.path.dirname(__file__), 
               './.env')
)

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
  
  result_list = []
  for ner_tuple in picked_ner_tuple_list:
    term, entity_type = ner_tuple
    
    if entity_type == "PERSON":
      result = api_freebase.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
      
      result = api_youtube.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
      
      result = api_wikipedia.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
      
      result = api_twitter.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
    
    
    elif entity_type == "LOCATION":
      result = api_freebase.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
        
      result = api_googlemaps.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
        
      result = api_youtube.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
        
      result = api_yelp.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
        
      result = api_twitter.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
        
      result = api_wikipedia.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
    
    
    elif entity_type == "ORGANIZATION":
      result = api_freebase.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
        
      result = api_twitter.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
        
      result = api_youtube.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
        
      result = api_wikipedia.obtain(term, entity_type)
      if result is not None:
        result_list.append(json.dumps(result))
        result = None
      
  print json.dumps(result_list)

if __name__ == "__main__":
  main()
  