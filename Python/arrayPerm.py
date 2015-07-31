from collections import defaultdict

def isPermutation(array1, array2):
	if len(array1) != len(array2):
		return False

	arrayCount1 = defaultdict(int)
	arrayCount2 = defaultdict(int)

	for item in array1:
		arrayCount1[item] += 1

	for item in array2:
		arrayCount2[item] += 1

	if arrayCount1.keys() == arrayCount2.keys():
		if cmp(arrayCount1, arrayCount2) == 0:
			return True

	return False

def isPermutationTest():
	testArray1 = ['a', 'b', 'd', 'a']
	testArray2 = ['b', 'a', 'a', 'd']
	testArray3 = ['a', 'b', 'c', 'd']
	testArray4 = ['a', 'b', 'd', 'a', 'b']

	if isPermutation(testArray1, testArray2) == True:
		if isPermutation(testArray1, testArray3) == False:
			if isPermutation(testArray1, testArray4) == False:
				print 'All tests passed!'
			else:
				print 'Different length array test failed!'
		else:
			print 'Non-permutation test failed!'
	else:
		print 'Permutation test failed!'

if __name__ == '__main__':
	isPermutationTest()