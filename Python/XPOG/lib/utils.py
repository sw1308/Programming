#!/usr/bin/python2 -tt

import unittest


def flattenList(nestedList):
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


if __name__ == '__main__':
    unittest.main()
