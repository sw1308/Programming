import sys
import xml.etree.ElementTree as ET

from arrayPerm import isPermutation

#-------------------------------------------------------------------------------
# Test for equivalence of n depth element trees

def isXMLPermutation(root1, root2):
	if isElementPermutation(root1, root2) == True:
		tags1 = []
		tags2 = []

		for child in root1.getchildren():
			tags1.append(child.tag)

		for child in root2.getchildren():
			tags2.append(child.tag)

		if isPermutation(tags1, tags2) == True:
			if len(root1) > 0 and len(root2) > 0:
				perm = True

				for child in root1.getchildren():
					print 'iterating over children'
					if isXMLPermutation(child, root2.find(child.tag)) == False:
						perm = False

				if perm:
					return True
				else:
					return False

			elif len(root1) != len(root2):
				print 'children are different lengths'
				return False
			else:
				print 'reached leaf nodes'
				return True
		else:
			return False
	else:
		return False

#-------------------------------------------------------------------------------
# Test for equivalence of single depth elements

def isElementPermutation(element1, element2):
	if element1.tag != element2.tag:
		return False

	if cmp(element1.attrib, element2.attrib) != 0:
		return False

	if len(element1) == 0 and len(element2) == 0:
		if element1.text != element2.text:
			return False

	return True

#-------------------------------------------------------------------------------
# Run main setup for testing

if __name__ == '__main__':
	if len(sys.argv) > 1:
		xmlFiles = sys.argv[1:]
	else:
		xmlFiles = []
		xmlFiles.append(raw_input('Enter first xml file: '))
		xmlFiles.append(raw_input('Enter second xml file: '))

	trees = []

	for fileName in xmlFiles:
		if fileName[-3:] != 'xml':
			raise StandardError('File name %s is not an xml file.' % fileName)
		else:
			trees.append(ET.parse(fileName))

	results = []

	for tree in trees[1:]:
		results.append(isXMLPermutation(trees[0].getroot(), tree.getroot()))

	print results

# TODO print results	
	# for index in len()
	# if isXMLPermutation(trees[0], tree) == True:
	# 	print 'File %s is equivalent to %s' % (file, xmlFiles[0])
	# else:
	# 	print 'File %s is NOT equivalent to %s' % (file, xmlFiles[0])