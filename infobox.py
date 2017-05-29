import urllib2, json, pprint, re, datetime
import mwparserfromhell

def _parseDate(wikiDate):
  template = mwparserfromhell.parse("%s"%wikiDate.value)
  try:
    try:
      d = map(template.filter_templates()[0].get, [1,2,3])
      d = [int('%s'%x.value) for x in d]
      dateFinal = str(d[1]) +"-"+ str(d[2]) +"-"+ str(d[0])
      return dateFinal
    except Exception as e:
      d = map(template.filter_templates()[0].get, [1])
      d = [int('%s'%x.value) for x in d]
      dateFinal = str(d[0])
      return dateFinal
  except Exception as e:
    tempTest = re.sub('\n', '', str(template))
    return str(tempTest)
  else:
    d = None
    return d

def _parsePlace(wikiPlace):
  template = mwparserfromhell.parse("%s"%wikiPlace.value)
  tempTest = re.sub('[\(\)\{\}<>\[\]\|\n]', '', str(template))
  tempFinal = re.sub('nowrap', '', str(tempTest))
  tempFinal2 = re.sub('br/', '', str(tempFinal))
  return (str(tempFinal2))

def _parseInfobox(page):
  '''Parse out the nice mediawiki markdown to get birth and death
  Input:
    mediawiki unicode page string
  Returns:
    a dictionary with name(string), birth_date:DateTime, death_date:DateTime
  '''
        
  try:
    code = mwparserfromhell.parse(page)
    for template in code.filter_templates():
      if 'Infobox' in template.name or 'infobox' in template.name:

        output = {}

        try:
          output['name'] = "%s"%template.get('name').value
        except ValueError as e:
          output['name'] = "%s"%template.get('birth_name').value

        # print "Name was found"

        for date in ['birth_date', 'death_date']:
          try:
            item = _parseDate(template.get(date))
          except ValueError as e:
            item = None
          output[date] = item

        for birthPlace in ['birth_place']:
          try:
            item = _parsePlace(template.get(birthPlace))
          except ValueError as e:
            item = None
          output[birthPlace] = item

        for deathPlace in ['death_place']:
          try:
            item = _parsePlace(template.get(deathPlace))
          except ValueError as e:
            item = None
          output[deathPlace] = item
        
        
        return output
        
    raise ValueError('Missing InfoBox')

  except Exception as e:
    # print "Failed to parse find infobox or something else"
    # raise e
    pass


def wikiAge(wikiTitle, function=None):
  ''' Parse a wikipedia url to run a function on the data
  Input:
    wikiTitle : Title of a wiki page for an individual with born and died date
    function : a python function which operates on a mediawikipage
  Output:
    Person Dictionary with ['name', 'birth_date', 'death_date'

  Example:
    person = wikiDate('Albert_Einstein', function=_parseInfobox)
    assert person['name'] == 'Albert Einstein'
    assert person['birth_date'] == datetime.date(1879, 03, 14) # '14 March 1879'
    assert person['death_date'] == datetime.date(1955, 04, 18) # '18 April 1955'
  '''
  URLTEMPLATE = 'http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content'
  try:
    pageJson = urllib2.urlopen(URLTEMPLATE%(wikiTitle)).readlines()[0]
  except Exception as e:
    print "Failed to Read page: %s"%(URLTEMPLATE%(wikiTitle))
    raise e

  try:
    page = json.loads(pageJson)
    page = page['query']['pages']
    pageid = page.keys()[0]
    page = page[pageid]['revisions'][0]['*'] 
    
    return function(page)

  except Exception as e:
    # print 'Failed to process Page -- Probably means that the wiki page was missing something important'
    # raise e
    pass

# Test Cases to Use (Uncomment for use)
# if __name__ == '__main__':

#   person = wikiAge('Michael_Pettis', function=_parseInfobox)
#   try:
#     for key in person:
#       print 'Key:%s  Value: %s'%(key,person[key])
#   except Exception as e:
#     pass
#   person = wikiAge('Galileo_Galilei', function=_parseInfobox)
#   for key in person:
#     print 'Key:%s  Value: %s'%(key,person[key])

  # person = wikiAge('Lawrence_Summers', function=_parseInfobox)
  # for key in person:
  #   print 'Key:%s  Value: %s'%(key,person[key])

