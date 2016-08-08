import os

from bs4 import BeautifulSoup
from nltk.tag.stanford import StanfordNERTagger
import pydash as _


path_sner_model = os.getenv(
  'STANFORD_NER_MODEL',
  os.path.realpath('./stanford-ner/models/english.all.3class.distsim.crf.ser.gz')
)
path_sner_jar = os.getenv(
  'STANFORD_NER_JAR',
  os.path.realpath('./stanford-ner/tagger/stanford-ner.jar')
)
stanford_tagger = StanfordNERTagger(path_sner_model, path_sner_jar)

"""
Strips out HTML tags
@param webpage_data:string
@returns string
"""
def cleanse_tags(webpage_data):
  return BeautifulSoup(webpage_data, "html.parser").get_text()

"""
Mapper that works on each word token, tagging it as usual with a 
  Named Entity Recognition Tagger
@param webpage_data:string
@returns [(string, tag)]
"""
def ner_tagging(webpage_data):
  ner_tuple_list = stanford_tagger.tag(webpage_data.split())
  
  return ner_tuple_list

"""
Filters a Stanford NER tuple, grouping together neighboring words 
  with the same categories and removing useless categorized words.
@param ner_tuple_list:[(string, tag)]
@returns [(string, tag)]
"""
def reduce_neighbors(ner_tuple_list=[]):
  
  def reducer(filtered_list, ner_tuple):
    word, tag = ner_tuple
    
    if tag == 'O':
        return filtered_list

    if not filtered_list:
      filtered_list.append((word, tag))
      return filtered_list

    recent_filtered_word, recent_filtered_tag = filtered_list[-1]

    if recent_filtered_tag == tag:
      filtered_list.pop()
      filtered_list.append(("%s %s" % (recent_filtered_word, word), tag))
    else:
      filtered_list.append((word, tag))
    
    return filtered_list
  
  return _.reduce_(ner_tuple_list, reducer, [])

"""
Pick the most 'important' items of count size from ner_tuple_list,
  shortening it to count size. Only unique items are obtained.
@param ner_tuple_list:[(string, tag)]
@returns [(string, tag)]
"""
def pick_most_important(ner_tuple_list=[], count=0):
  
  def reducer(word_tagfrequency_kv, ner_tuple):
    word, tag = ner_tuple
    
    if word not in word_tagfrequency_kv:
      word_tagfrequency_kv[word] = {
        "tag": tag,
        "count": 1
      }
      return word_tagfrequency_kv
    
    word_tagfrequency_kv[word] = {
      "tag": tag,
      "count": word_tagfrequency_kv[word]["count"] + 1
    }
    return word_tagfrequency_kv
  
  word_tagfrequency_kv = _.reduce_(ner_tuple_list, reducer, {})
  
  sorted_list = sorted(
    word_tagfrequency_kv.items(), 
    key=lambda (key, value): value["count"], 
    reverse=True
  )
  sorted_ner_tuple_list = _.map_(
    sorted_list, 
    lambda (key,value): (key, value["tag"])
  )
  
  sorted_length = len(sorted_ner_tuple_list)
  if sorted_length > count:
    return _.drop_right(
      sorted_ner_tuple_list, 
      sorted_length - count
    )
  return sorted_ner_tuple_list
  