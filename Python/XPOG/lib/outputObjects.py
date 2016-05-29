#!/usr/bin/python2 -tt

import unittest
from string import Template

import utils

with open('stdlib/classTemplate.py', 'r') as templateFile:
    classTemplate = Template(templateFile.read())

with open('stdlib/unitTestTemplate.py', 'r') as templateFile:
    unitTestTemplate = Template(templateFile.read())

with open('stdlib/testFunctions.py', 'r') as templateFile:
    testFunction = Template(templateFile.read())

class outputClass(object):
    """
        Standard representation object for outputting class definition to a
        file.

        This object is intended to be built from information in the object model
        output by the XSDConstructor. The idea is that the str() method for
        these objects will print out a complete class definition and set of
        unittests for a single xsd object.
    """

    def __init__(
        self,
        className,
        classTag,
        parentType,
        docstring='No provided documentation',
        requiredArgs=[],
        optionalArgs=[],
        attributes={}
    ):
        self.className = className
        self.classTag = classTag
        self.parentType = parentType
        self.docstring = docstring
        self.requiredArgs = utils.tameNoneList(requiredArgs)
        self.optionalArgs = utils.tameNoneList(optionalArgs)
        self.attributes = attributes

    def __str__(self):
        argString = ''
        parentArgString = ''
        dataInstantiationBlock = ''
        elementData = '[\n'
        elementAttribs = '{'

        if len(self.requiredArgs) > 0:
            argString = ', '
            for arg in self.requiredArgs:
                argString += arg + ', '
                elementData += '                ' + arg + ',\n'

                if self.parentType is not None:
                    if arg not in self.parentType.requiredArgs:
                        dataInstantiationBlock += '            self.{} = {}\n'.format(arg, arg)

        if len(self.optionalArgs ) > 0:
            if argString == '':
                argString = ', '

            for arg in self.optionalArgs:
                argString += arg + '=None, '
                elementData += '                ' + arg + ',\n'

                if self.parentType is not None:
                    if arg not in self.parentType.optionalArgs:
                        dataInstantiationBlock += '            self.{} = {}\n'.format(arg, arg)

        if self.parentType is not None:
            if len(self.parentType.requiredArgs) > 0 or len(self.parentType.optionalArgs) > 0:
                for arg in self.parentType.requiredArgs + self.parentType.optionalArgs:
                    parentArgString += arg + ', '

        # Clean up the last comma at the end of argStrings
        argString = argString[:-2]
        parentArgString = parentArgString[:-2]
        if elementData == '[\n':
            elementData = elementData[:-1] + ']'
        else:
            elementData = elementData[:-2] + '\n            ]'

        for attr in self.attributes:
            elementAttribs += '{}:{}, '.format(attr[0], attr[1])

        # Clean up the last comma and close the curly braces
        if elementAttribs == '{':
            elementAttribs += '}'
        else:
            elementAttribs = elementAttribs[:-2] + '}'


        classDefinition = classTemplate.substitute(
            elementName = self.className,
            typedBy = self.parentType.className if self.parentType is not None else 'Object',
            annotation = self.docstring,
            elementTag = self.classTag,
            args = argString,
            parentArgs = parentArgString,
            typeChecks = '',
            dataInstantiation = dataInstantiationBlock,
            elementData = elementData,
            elementAttribs = elementAttribs
        )

        return classDefinition


# This is needed as a starting point for all generated objects, this doesn't
# really do anything on it's own.
baseObject = outputClass('baseObject', 'ABSTRACT-CLASS', None)



class testOutputClass(unittest.TestCase):
    def testDefault(self):
        testObj = outputClass('testClass', 'TEST-CLASS', baseObject)

        self.assertEqual(
            str(testObj),
            'class testClass(baseObject):\n' +
            '    """\n' +
            '        No provided documentation\n' +
            '    """\n' +
            '    self.TAG = \'TEST-CLASS\'\n' +
            '    def __init__(self):\n' +
            '        super(testClass, self).__init__()\n' +
            '\n' +
            '\n' +
            '\n' +
            '    def __str__(self):\n' +
            '        return self.el(\n' +
            '            TAG=\'TEST-CLASS\',\n' +
            '            content=[],\n' +
            '            attribs={}\n' +
            '        )\n'
        )

    def testComplex(self):
        testObj = outputClass(
            className = 'testClass',
            classTag = 'TEST-CLASS',
            parentType = baseObject,
            docstring = 'This is a complex object, contains all the stuff',
            requiredArgs = [
                'req1',
                'req2',
            ],
            optionalArgs = [
                'opt1',
                'opt2'
            ],
            attributes = [
                ('attr1','val1'),
                ('attr2','val2'),
                ('attr3','val3'),
                ('attr4','val4'),
            ]
        )

        self.assertEqual(
            str(testObj),
            'class testClass(baseObject):\n' +
            '    """\n' +
            '        This is a complex object, contains all the stuff\n' +
            '    """\n' +
            '    self.TAG = \'TEST-CLASS\'\n' +
            '    def __init__(self, req1, req2, opt1=None, opt2=None):\n' +
            '        super(testClass, self).__init__()\n' +
            '\n' +
            '            self.req1 = req1\n' +
            '            self.req2 = req2\n' +
            '            self.opt1 = opt1\n' +
            '            self.opt2 = opt2\n' +
            '\n' +
            '\n' +
            '    def __str__(self):\n' +
            '        return self.el(\n' +
            '            TAG=\'TEST-CLASS\',\n' +
            '            content=[\n' +
            '                req1,\n' +
            '                req2,\n' +
            '                opt1,\n' +
            '                opt2\n' +
            '            ],\n' +
            '            attribs={attr1:val1, attr2:val2, attr3:val3, attr4:val4}\n' +
            '        )\n'
        )


if __name__ == '__main__':
    unittest.main()
