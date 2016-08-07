def obtain(search_term, category):
  return {
    "metadata": {
      "type": "google-maps",
      "term": search_term,
      "category": category
    },
    "data": "https://maps.google.com/?q=%s" % search_term
  }