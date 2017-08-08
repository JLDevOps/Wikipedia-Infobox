import urllib2, json, re, nltk
import mwparserfromhell
from infobox import wiki_info, parse_infobox

'''
    This file is for the scraping of the BIO section of the Wikipedia page
'''

def extract_entity_names(t):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

def parse_key_word(preprocess_sentence, keyword):
    sentence_list = []
    for sentence in preprocess_sentence.split('.'):
        if keyword in sentence:
            sentence_list.append(sentence)
    return sentence_list

def nltk_process(sentence):
    process_sent = nltk.sent_tokenize(sentence)
    tokenized_sent = [nltk.word_tokenize(sentence) for sentence in process_sent]
    tagged_sent = [nltk.pos_tag(sentence) for sentence in tokenized_sent]
    chunked_sent = nltk.ne_chunk_sents(tagged_sent, binary=True)
    entity_names = []
    for tree in chunked_sent:
        entity_names.extend(extract_entity_names(tree))
    # Print unique entity names
    print set(entity_names)

if __name__ == '__main__':
    sentence = "Pettis was born in Zaragoza, Spain, Spain, Spain, Spain to a French mother and an American father. His father born as an geologist and civil engineer. He spent his childhood in Peru, Pakistan, Morocco and Haiti, before returning to Spain for High School. Pettis entered Columbia University in 1976.[4] Pettis received a Masters of International Affairs in 1981 and a Masters of Business Administration in 1984, both from Columbia University."
    location_sent = parse_key_word(sentence, "born")
    counter = 0
    print len(location_sent)
    for index in location_sent:
        print nltk_process(location_sent[counter])
        counter+=1
    #process_sent = nltk_process(location_sent)





