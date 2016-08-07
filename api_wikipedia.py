import wikipedia
import pydash as _


def obtain(search_term, category):
  
  try:
    wpage = wikipedia.WikipediaPage(title=search_term)
  except BaseException:
    return None
  
  wimages = wpage.images
  wimages_length = len(wimages)
  if wimages_length <= 6:
    wimages = []
  wimages = _.drop_right(
    wimages,
    wimages_length - 6
  )
  
  return {
    "metadata": {
      "type": "wikipedia-information",
      "term": search_term,
      "category": category
    },
    "data": {
      "name": search_term,
      "description": wpage.summary,
      "images": wimages
    }
  }
  