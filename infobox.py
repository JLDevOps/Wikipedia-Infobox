import urllib2, json, re
import mwparserfromhell


def parse_date(wiki_date):
    '''
      Given the JSON data from InfoBox():
      Input: JSON Data from InfoBox() that located Birth_Date and Death_Date
      Output: Birth_Date and Death_Date in the format, MM - DD - YYYY
    '''
    template = mwparserfromhell.parse("%s" % wiki_date.value)
    try:
        try:
            # This parses and separates the year, month, and day into separate entities to combine -- MM - DD - YYYY #
            d = map(template.filter_templates()[0].get, [1, 2, 3])
            d = [int('%s' % x.value) for x in d]
            dateFinal = str(d[1]) + "-" + str(d[2]) + "-" + str(d[0])
            return dateFinal
        except ValueError as e:
            # This exception is used if there is only a Year for the Person #
            d = map(template.filter_templates()[0].get, [1])
            d = [int('%s' % x.value) for x in d]
            dateFinal = str(d[0])
            return dateFinal
    except Exception as e:
        print "ERROR: " + wiki_date + "not found in the infobox."
        raise e


def parse_place(wiki_place):
    '''
      Given the JSON data from InfoBox():
      Input: JSON Data from InfoBox() that located Birth_Place and Death_Place
      Output: Birth_Place and Death_Place strings
    '''
    template = mwparserfromhell.parse("%s" % wiki_place.value)
    try:
        template = re.sub('[\{\}<>\[\n]', '', str(template))
        [town, city, country] = template.split(',')

        try:
            town = re.sub('nowrap\|', '', town)
            town = re.sub('\|.*?\]', '', town)
            town = re.sub('[\(\[].*?[\)\]]', '', town)
            town = re.sub('].*?', '', town)
            town = re.sub('br/', '', town)
        except Exception as e:
            print "ERROR: Information regarding the person's town could not be found"
            raise e

        try:
            city = re.sub('nowrap\|', '', city)
            city = re.sub('\|.*?\]', '', city)
            city = re.sub('[\(\[].*?[\).*?\]]', '', city)
            city = re.sub('].*?', '', city)
            city = re.sub('\)', '', city)
            city = re.sub('br/', '', city)
        except Exception as e:
            print "ERROR: Information regarding the person's city could not be found"
            raise e
        try:
            country = re.sub('nowrap\|', '', country)
            country = re.sub('\|.*?\]', '', country)
            country = re.sub('[\(\[].*?[\)\]]', '', country)
            country = re.sub('].*?', '', country)
            country = re.sub('br/', '', country)
        except Exception as e:
            print "ERROR: Information regarding the person's country could not be found"
            raise e

        address = town + ", " + city + ", " + country
        return address
    except Exception as e:
        print "ERROR: " + wiki_place + " could not be parsed or found in the infobox."
        raise e


def parse_infobox(page):
    '''
      Given the JSON data from WikiAge():
      Input: JSON Data from WikiAge(), locates the Infobox heading
      Output: Selected information from each specific function

      Ex. Key:birth_date  Value: 2-15-1564
          Key:death_place  Value:  Arcetri, Grand Duchy of Tuscany, Italy
          Key:death_date  Value: 1-8-1642
          Key:birth_place  Value:  Pisa, Duchy of Florence, Italy
          Key:name  Value:  Galileo Galilei
    '''
    #print page
    test_value= re.findall('(?<=birth_place = )(.*)', page, re.UNICODE)

    test_encode = unicode(str(test_value), "utf-8")
    print (test_encode)


    try:
        code = mwparserfromhell.parse(page)
        for template in code.filter_templates():
            if 'Infobox' in template.name or 'infobox' in template.name:

                output = {}

                try:
                    try:
                        output['name'] = "%s" % template.get('name').value
                    except ValueError as e:
                        output['name'] = "%s" % template.get('birth_name').value
                except ValueError as e:
                    print "ERROR: Name was not Found"
                    raise e

                for date in ['birth_date', 'death_date']:
                    try:
                        item = parse_date(template.get(date))
                    except ValueError as e:
                        item = None
                    output[date] = item

                for place in ['birth_place', 'death_place']:
                    try:
                        item = parse_place(template.get(place))
                    except ValueError as e:
                        item = None
                    output[place] = item

                return output

        raise ValueError('Missing InfoBox')

    except Exception as e:
        ## Uncommented for Testing ##
        # print "Failed to Properly Parse Infobox for Information"
        # raise e
        pass


def wiki_info(wiki_title, function=None):
    ''' Parse a wikipedia url to run a function on the data '''

    url_template = 'http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content'
    wiki_title = wiki_title.replace(" ", "_")
    try:
        page_json = urllib2.urlopen(url_template % wiki_title).readlines()[0]
    except Exception as e:
        print "ERROR: Failed to open link to Wikipedia page: %s" % (url_template % wiki_title)
        raise e

    try:
        page = json.loads(page_json)
        page = page['query']['pages']
        page_id = page.keys()[0]
        page = page[page_id]['revisions'][0]['*']
        return function(page)
    except Exception as e:
        print 'ERROR: Failed to parse the Wikipedia information'
        raise e


#Test Cases to Use (Uncomment for use)
if __name__ == '__main__':
    person = wiki_info('Albert Einstein', function=parse_infobox)
    try:
        for key in person:
            print 'Key:%s  Value: %s' % (key, person[key])
    except Exception as e:
        pass
    person = wiki_info('Mark Zuckerberg', function=parse_infobox)
    try:
        for key in person:
            print 'Key:%s  Value: %s' % (key, person[key])
    except Exception as e:
        pass
