import unittest, csv
from infobox import wikiAge, _parseInfobox

''' CSV Reader to test the infobox.py file for a list of People's names on Wikipedia '''
with open('names.csv', 'rb') as csvfile:
	fileReader = csv.reader(csvfile, delimiter=',')
	for row in fileReader:
		person = wikiAge(row[0], function=_parseInfobox)
		try:
  			for key in person:
  				print 'Key:%s  Value: %s'%(key,person[key])
  		except Exception as e:
  			pass



''' Unit tests for the names and information '''
''' Not finished writing '''

# class nameTest(unittest.TestCase):

#     def testOne(self):
#     
# def main():
#     unittest.main()

# if __name__ == '__main__':
#     main()