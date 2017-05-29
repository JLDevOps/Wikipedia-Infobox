import unittest, csv
from age import wikiAge, _parseInfobox

with open('names.csv', 'rb') as csvfile:
	fileReader = csv.reader(csvfile, delimiter=',')
	for row in fileReader:
		person = wikiAge(row[0], function=_parseInfobox)
		try:
  			for key in person:
  				print 'Key:%s  Value: %s'%(key,person[key])
  		except Exception as e:
  			pass






##Unit tests for the names and birthdays##
# class nameTest(unittest.TestCase):

#     def testOne(self):
#         self.failUnless(IsOdd(1))

#     def testTwo(self):
#         self.failIf(IsOdd(2))

#     def testThree(self):
#     	self.failIf()

# def main():
#     unittest.main()

# if __name__ == '__main__':

#     main()