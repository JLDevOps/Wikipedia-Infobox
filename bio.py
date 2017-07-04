import urllib2, json, re, nltk
import mwparserfromhell
from infobox import wiki_info, parse_infobox

'''
    This file is for the scraping of the BIO section of the Wikipedia page
'''

if __name__ == '__main__':
    sentence = """At eight o'clock on Thursday morning ... New York didn't feel very good."""
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    entities = nltk.chunk.ne_chunk(tagged)
    print(entities)





