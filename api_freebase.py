import os
import json

import requests
import requests.packages.urllib3
import pydash as _


api_key = os.getenv('FREEBASE_API_KEY', '')
requests.packages.urllib3.disable_warnings()

def obtain(search_term):
  
  params = {
    'query': search_term,
    'output': '(description)'
  }
  if api_key:
    params = _.assign({'api_key': api_key}, params)
    
  
  request = requests.get(
    'https://www.googleapis.com/freebase/v1/search', params, verify=False
  )
  if request.status_code != requests.codes.ok:
    return None
  
  try:
    payload = json.loads(request.text)
  except ValueError:
    return None
  
  return {
    "name": _.get(payload, 'result.0.name', None),
    "description": _.get(
      payload, 
      "result.0.output.description./common/topic/description.0"
    ),
    "images": []
  }
