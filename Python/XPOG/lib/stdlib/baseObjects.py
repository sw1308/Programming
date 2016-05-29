#!/usr/bin/python2 -tt

import unittest
import utils



class BaseObject(object):
    """
        Standard base object for output libraries, this class contains the
        printout code for writing XML to file.
    """

    def __init__(self):
        super(BaseObject, self).__init__()
        self.TAG = 'ABSTRACT-OBJECT'
        self.content = []
        self.attribs = {}
        self.parent = None


    def el(self, TAG, content=None, attribs={}):
        attribString = '' if len(attribs) == 0 else ' '

        for keyval in attribs:
            attribString = attribString + '{}="{}"'.format(keyval, attribs[keyval])

        openingTag = '<{}{}>'.format(TAG, attribString)
        closingTag = '</{}>'.format(TAG)
        emptyTag = '<{}{} />'.format(TAG, attribString)

        content = utils.tameNoneList(content)

        if len(content) > 0:
            xmlContent = ''

            for element in content:
                xmlContent = xmlContent + str(element)

            return openingTag + xmlContent + closingTag

        else:
            return emptyTag


    def __str__(self):
        return '<!-- ABSTRACT-OBJECT WAS CREATED -->'



class testBaseObject(unittest.TestCase):
    @unittest.skip("Skipping class definition.")
    class testObject(BaseObject):
        def __init__(self, TAG, content=None, attribs={}):
            super(testBaseObject.testObject, self).__init__()

            self.TAG = TAG
            self.content = content
            self.attribs = attribs

        def __str__(self):
            return self.el(
                self.TAG,
                self.content,
                self.attribs
            )


    def testSimple(self):
        testObj = self.testObject('TESTXML')

        self.assertEqual(
            str(testObj),
            '<TESTXML />'
        )

    def testAttribs(self):
        testObj = self.testObject('TESTXML', attribs={'ATTR':'testAttribute'})

        self.assertEqual(
            str(testObj),
            '<TESTXML ATTR="testAttribute" />'
        )

    def testContent(self):
        bobContent = self.testObject('STRING', content='bob')
        benContent = self.testObject('STRING', content='ben')
        intContent = self.testObject('INT', content=1)

        testObj = self.testObject(
            'TESTXML',
            content=[
                bobContent,
                benContent,
                intContent
            ]
        )

        self.assertEqual(
            str(testObj),
            '<TESTXML>'+
                '<STRING>bob</STRING>'+
                '<STRING>ben</STRING>'+
                '<INT>1</INT>'+
            '</TESTXML>'
        )

    def testComplex(self):
        bobContent = self.testObject('PERSON', content='bob')
        benContent = self.testObject('PERSON', content='ben')
        
        peopleContent = self.testObject(
            'PEOPLE',
            content=[
                bobContent,
                benContent
            ]
        )

        intContent = self.testObject('COUNT', attribs={'numOf':'PEOPLE'}, content=2)

        testObj = self.testObject(
            'CENSUS',
            content=[
                peopleContent,
                intContent
            ],
            attribs={'DATE':'11/04/16'}
        )

        self.assertEqual(
            str(testObj),
            '<CENSUS DATE="11/04/16">'+
                '<PEOPLE>'+
                    '<PERSON>bob</PERSON>'+
                    '<PERSON>ben</PERSON>'+
                '</PEOPLE>'+
                '<COUNT numOf="PEOPLE">2</COUNT>'+
            '</CENSUS>'
        )



if __name__ == '__main__':
    unittest.main()
