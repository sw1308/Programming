#!/usr/bin/python2 -tt

"""
    Standard utility library for XPOG libraries. Contains some useful functions
    that will be used throughout the library.
"""
import re
import unittest

# Common list operations
def isPermutation(list1, list2):
    """
        Returns True if list1 and list2 contain the same elements exclusively.
    """
    if len(list1) == len(list2):
        return sorted(list1) == sorted(list2)

    else:
        return False



class testIsPermutation(unittest.TestCase):
    def testDifferentSize(self):
        testList1 = [1, 2, 3]
        testList2 = [1, 2, 3, 4]

        self.assertFalse(isPermutation(testList1, testList2))


    def testDifferent(self):
        testList1 = [1, 2, 3, 4, 5]
        testList2 = [6, 7, 8, 9, 0]

        self.assertFalse(isPermutation(testList1, testList2))


    def testIdentical(self):
        testList1 = [1, 2, 3, 4, 5]
        testList2 = [1, 2, 3, 4, 5]

        self.assertTrue(isPermutation(testList1, testList2))


    def testPerm(self):
        testList1 = [1, 2, 3, 4, 5]
        testList2 = [2, 5, 1, 4, 3]

        self.assertTrue(isPermutation(testList1, testList2))


def unique(l):
    """
        Returns a list l with every duplicate item removed.
    """

    return list(set(l))



class testUnique(unittest.TestCase):
    def testUnique(self):
        testList = ['a', 'b', 'c']



        self.assertTrue(
            isPermutation(
                unique(testList),
                testList
            )
        )


    def testNonUnique(self):
        testList = ['a', 'a', 'a', 'b']

        self.assertEqual(
            unique(testList),
            ['a', 'b']
        )


def union(list1, list2):
    """
        Returns a mathematical union between two lists.
    """

    return list(set(list1) | set(list2))



class testUnion(unittest.TestCase):
    def testDifferent(self):
        testList1 = [1, 2, 3]
        testList2 = [4, 5, 6]

        self.assertEqual(
            union(testList1, testList2),
            [1, 2, 3, 4, 5, 6]
        )


    def testOverlap(self):
        testList1 = [1, 2, 3]
        testList2 = [3, 4, 5]

        self.assertEqual(
            union(testList1, testList2),
            [1, 2, 3, 4, 5]
        )


    def testSame(self):
        testList1 = [1, 2, 3]
        testList2 = [1, 2, 3]

        self.assertEqual(
            union(testList1, testList2),
            [1, 2, 3]
        )


def intersect(list1, list2):
    """
        Returns a mathematical intersection between two lists.
    """

    return list(set(list1) & set(list2))



class testIntersect(unittest.TestCase):
    def testSame(self):
        testList1 = [1, 2, 3]
        testList2 = [1, 2, 3]

        self.assertEqual(
            intersect(testList1, testList2),
            [1, 2, 3]
        )


    def testOverlap(self):
        testList1 = [1, 2, 3]
        testList2 = [2, 3, 4]

        self.assertEqual(
            intersect(testList1, testList2),
            [2, 3]
        )


    def testDifferent(self):
        testList1 = [1, 2, 3]
        testList2 = [4, 5, 6]

        self.assertEqual(
            intersect(testList1, testList2),
            []
        )


def flattenList(nestedList):
    """
        Returns a flattened version of an arbitrarily nested list or tuple.
    """

    ret = []

    if isinstance(nestedList, (list, tuple)):
        for item in nestedList:
            ret = ret + flattenList(item)

    else:
        ret.append(nestedList)

    return ret



class testFlattenList(unittest.TestCase):
    def testNonList(self):
        testItem = 'test'

        self.assertEqual(flattenList(testItem), ['test'])


    def testFlatList(self):
        testItem = ['test1', 'test2', 'test3']

        self.assertEqual(
            flattenList(testItem),
            ['test1', 'test2', 'test3']
        )


    def testNestedList(self):
        testItem = [['test1'], 'test2', [['test3'], 'test4']]

        self.assertEqual(
            flattenList(testItem),
            ['test1', 'test2', 'test3', 'test4']
        )


    def testTuples(self):
        testItem = [['test1'], 'test2', [[('test3a', 'test3b')], 'test4']]

        self.assertEqual(
            flattenList(testItem),
            ['test1', 'test2', 'test3a', 'test3b', 'test4']
        )


    def testNonePreserve(self):
        testItem = [['test1'], 'test2', [[('test3a', None)], 'test4']]

        self.assertEqual(
            flattenList(testItem),
            ['test1', 'test2', 'test3a', None, 'test4']
        )


def tameNoneList(maybeList):
    """
        Flattens list, removes all None values and always returns a list.
    """

    ret = []

    if isinstance(maybeList, (list, tuple)):
        for item in flattenList(maybeList):
            if item is not None:
                ret.append(item)

    # If maybeList is not None
    elif maybeList:
        ret.append(maybeList)

    return ret



class testTameNoneList(unittest.TestCase):
    def testNone(self):
        testItem = '1'

        self.assertEqual(tameNoneList(testItem), ['1'])


    def testSimpleList(self):
        testItem = ['1', '2', '3']

        self.assertEqual(
            tameNoneList(testItem),
            ['1', '2', '3']
        )


    def testNoneList(self):
        testItem = ['1', None, '3']

        self.assertEqual(
            tameNoneList(testItem),
            ['1', '3']
        )


    def testNoneNestedList(self):
        testItem = [['test1'], 'test2', [[('test3a', None)], 'test4']]

        self.assertEqual(
            tameNoneList(testItem),
            ['test1', 'test2', 'test3a', 'test4']
        )


def prettyXML(xmlString):
    lineDepth = 0
    xmlOpenTag = re.compile(r'(<[\w-]+\s*[\w="]*>)')
    xmlContent = re.compile(r'(.*?)<')
    xmlCloseTag = re.compile(r'(</[\w-]+>)')
    xmlEmptyTag = re.compile(r'(<[\w-]+\s*[\w="]*\s?/>)')
    outputString = ""

    while len(xmlString) > 0:
        openTagMatch = xmlOpenTag.match(xmlString)
        closeTagMatch = xmlCloseTag.match(xmlString)
        emptyTagMatch = xmlEmptyTag.match(xmlString)
        contentMatch = xmlContent.match(xmlString)

        if emptyTagMatch is not None:
            for depth in xrange(lineDepth):
                outputString += "    "

            outputString += xmlString[0:len(emptyTagMatch.group(1))]
            outputString += '\n'
            xmlString = xmlString[len(emptyTagMatch.group(1)):]

        elif openTagMatch is not None:
            for depth in xrange(lineDepth):
                outputString += "    "

            outputString += xmlString[0:len(openTagMatch.group(1))]
            outputString += '\n'
            lineDepth += 1
            xmlString = xmlString[len(openTagMatch.group(1)):]

        elif closeTagMatch is not None:
            lineDepth -= 1

            for i in xrange(lineDepth):
                outputString += "    "

            outputString += xmlString[0:len(closeTagMatch.group(1))]
            outputString += '\n'
            xmlString = xmlString[len(closeTagMatch.group(1)):]

        else:
            for i in xrange(lineDepth):
                outputString += "    "

            outputString += xmlString[0:len(contentMatch.group(1))]
            outputString += '\n'
            xmlString = xmlString[len(contentMatch.group(1)):]


    return outputString


class testPrettyXML(unittest.TestCase):
    def testNone(self):
        self.assertEqual(
            prettyXML(''),
            ''
        )

    def testEmpty(self):
        self.assertEqual(
            prettyXML('<element />'),
            '<element />\n'
        )

    def testElement(self):
        self.assertEqual(
            prettyXML(
                '<element>bibble</element>'
            ),
            '<element>\n' +
            '    bibble\n' +
            '</element>\n'
        )

    def testContainer(self):
        self.assertEqual(
            prettyXML(
                '<upper>' +
                    '<lower>bibble</lower>' +
                    'bobble' +
                '</upper>'
            ),
            '<upper>\n' +
            '    <lower>\n' +
            '        bibble\n' +
            '    </lower>\n' +
            '    bobble\n' +
            '</upper>\n'
        )

    def testNested(self):
        self.assertEqual(
            prettyXML(
                '<outer>' +
                    '<middle>' +
                        '<inner>bibble</inner>' +
                        'bobble' +
                    '</middle>' +
                    'bubble'
                '</outer>'
            ),
            '<outer>\n' +
            '    <middle>\n' +
            '        <inner>\n' +
            '            bibble\n' +
            '        </inner>\n' +
            '        bobble\n' +
            '    </middle>\n' +
            '    bubble\n' +
            '</outer>\n'
        )


if __name__ == '__main__':
    unittest.main()
