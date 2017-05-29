import urllib2, json, pprint, re, datetime
import mwparserfromhell

def _parseDate(wikiDate):
  ''' Given the JSON data from InfoBox():
      Input: JSON Data from InfoBox() that located Birth_Date and Death_Date
      Output: Birth_Date and Death_Date in the format, MM - DD - YYYY
  '''
  template = mwparserfromhell.parse("%s"%wikiDate.value)
  try:

    try:
      ## This parses and separates the year, month, and day into separate entities to combine -- MM - DD - YYYY ##
      d = map(template.filter_templates()[0].get, [1,2,3])
      d = [int('%s'%x.value) for x in d]
      dateFinal = str(d[1]) +"-"+ str(d[2]) +"-"+ str(d[0])
      return dateFinal
    except Exception as e:
      ## This exception is used if there is only a Year for the Person ###
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
  ''' Given the JSON data from InfoBox():
      Input: JSON Data from InfoBox() that located Birth_Place and Death_Place
      Output: Birth_Place and Death_Place strings
  '''
  template = mwparserfromhell.parse("%s"%wikiPlace.value)
  tempPhase = re.sub('[\(\)\{\}<>\[\]\|\n]', '', str(template))
  tempPhase2 = re.sub('nowrap', '', str(tempPhase))
  tempFinal= re.sub('br/', '', str(tempPhase2))
  return (str(tempFinal))

def _parseInfobox(page):
  ''' Given the JSON data from WikiAge():
      Input: JSON Data from WikiAge(), locates the Infobox heading
      Output: Selected information from each specific function

      Ex. Key:birth_date  Value: 2-15-1564
          Key:death_place  Value:  Arcetri, Grand Duchy of Tuscany, Italy
          Key:death_date  Value: 1-8-1642
          Key:birth_place  Value:  Pisa, Duchy of Florence, Italy
          Key:name  Value:  Galileo Galilei
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

        for place in ['birth_place', 'death_place']:
          try:
            item = _parsePlace(template.get(place))
          except ValueError as e:
            item = None
          output[place] = item
        
        
        return output
        
    raise ValueError('Missing InfoBox')

  except Exception as e:
    ## Uncommented for Now for Testing ##
    # print "Failed to Properly Parse Infobox for Information"
    # raise e
    pass


def wikiAge(wikiTitle, function=None):
  ''' Parse a wikipedia url to run a function on the data '''

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
    ## Uncommented for Now for Testing ##
    # print 'Failed to Process Wikipedia Information -- Make sure the link is registering'
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


