#!/usr/bin/python2 -tt

import re
import math

import fewi
from xsdObjects import *


typeMap = {
    "base64Binary"       : re.compile(r'^[0-9a-zA-Z=/]*$', flags=re.M|re.S|re.U),
    "boolean"            : re.compile(r'(?:true|false)', flags=re.M|re.S|re.U),
    "date"               : re.compile(r'^-?[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9](?:[+-][0-9][0-9]:[0-9][0-9]|Z)?$', flags=re.M|re.S|re.U),
    "dateTime"           : re.compile(r'^-?[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9](?:\.[0-9]+)?(?:[+-][0-9][0-9]:[0-9][0-9]|Z)?$', flags=re.M|re.S|re.U),
    "decimal"            : re.compile(r'^-?[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "integer"            : re.compile(r'^-?[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "long"               : re.compile(r'^-?[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "int"                : re.compile(r'^-?[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "short"              : re.compile(r'^-?[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "byte"               : re.compile(r'^-?[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "nonNegativeInteger" : re.compile(r'^[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "positiveInteger"    : re.compile(r'^[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "unsignedLong"       : re.compile(r'^[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "unsignedInt"        : re.compile(r'^[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "unsignedShort"      : re.compile(r'^[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "unsignedByte"       : re.compile(r'^[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "nonPositiveInteger" : re.compile(r'^-[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "negativeInteger"    : re.compile(r'-^[0-9]+(?:\.[0-9]+)?$', flags=re.M|re.S|re.U),
    "double"             : re.compile(r'^(?:NaN|-?INF|-?[0-9]+(?:\.[0-9]+)?(?:[eE]-?[0-9]+)?)$', flags=re.M|re.S|re.U),
    "duration"           : re.compile(r'^P(?:[0-9]+Y)?(?:[0-9]+M)?(?:[0-9]+D)?T?(?:[0-9]+H)?(?:[0-9]+M)?(?:[0-9]+(?:\.[0-9]+)?S)?$', flags=re.M|re.S|re.U),
    "float"              : re.compile(r'^(?:NaN|-?INF|-?[0-9]+(?:\.[0-9]+)?(?:[eE]-?[0-9]+)?)$', flags=re.M|re.S|re.U),
    "gDay"               : re.compile(r'^---[0-9][0-9](?:[+-][0-9][0-9]:[0-9][0-9]|Z)?$', flags=re.M|re.S|re.U),
    "gMonth"             : re.compile(r'^--[0-9][0-9](?:[+-][0-9][0-9]:[0-9][0-9]|Z)?$', flags=re.M|re.S|re.U),
    "gMonthDay"          : re.compile(r'^[0-9][0-9]-[0-9][0-9](?:[+-][0-9][0-9]:[0-9][0-9]|Z)?$', flags=re.M|re.S|re.U),
    "gYear"              : re.compile(r'^-?[0-9]*[0-9][0-9][0-9][0-9](?:[+-][0-9][0-9]:[0-9][0-9]|Z)?$', flags=re.M|re.S|re.U),
    "gYearMonth"         : re.compile(r'^-?[0-9]*[0-9][0-9][0-9][0-9]-[0-9][0-9](?:[+-][0-9][0-9]:[0-9][0-9]|Z)?$', flags=re.M|re.S|re.U),
    "hexBinary"          : re.compile(r'^[0-9a-fA-F]*$', flags=re.M|re.S|re.U),
    "string"             : re.compile(r'.*', flags=re.M|re.S|re.U),
    "normalizedString"   : re.compile(r'.*', flags=re.M|re.S|re.U),
    "token"              : re.compile(r'.*', flags=re.M|re.S|re.U),
    "language"           : re.compile(r'.*', flags=re.M|re.S|re.U),
    "Name"               : re.compile(r'.*', flags=re.M|re.S|re.U),
    "NCName"             : re.compile(r'.*', flags=re.M|re.S|re.U),
    "ENTITY"             : re.compile(r'.*', flags=re.M|re.S|re.U),
    "ID"                 : re.compile(r'.*', flags=re.M|re.S|re.U),
    "IDREF"              : re.compile(r'.*', flags=re.M|re.S|re.U),
    "NMTOKEN"            : re.compile(r'.*', flags=re.M|re.S|re.U),
    "time"               : re.compile(r'^[0-9][0-9]:[0-9][0-9]:[0-9][0-9](?:\.[0-9]+)?(?:[+-][0-9][0-9]:[0-9][0-9]|Z)?$', flags=re.M|re.S|re.U)
}

def getMappedRegex(typeString):
    try:
        return typeMap[typeString]
    except KeyError:
        return None





class XSDConstructor(object):
    """
        Object for constructing contextual object models from parsed DOM object.
    """

    def __init__(self, treeModel):
        super(XSDConstructor, self).__init__()

        self.treeModel = treeModel
        self.finishedModel = None
        self.objectMap = {}
        self.objCount = 0


    def construct(self):
        # Get root node for a good start point.
        self.root = self.treeModel.getroot()

        self.finishedModel = self.buildTree(self.root)
        print '\tConstructed {} objects.'.format(self.objCount)


    def resolveType(self, elementType, name):
        if elementType is None:
            return None

        # Make sure you ignore elements that are typed by themselves
        # because that's a thing that's allowed apparently.
        elif name is not None and elementType.endswith(name):
            return 'SELFREF'

        elif elementType in self.objectMap:
            return self.objectMap[elementType]
        
        elif elementType in typeMap:
            return getMappedRegex(elementType)
        
        else:
            try:
                return self.buildTree(
                    self.treeModel.find(
                        ".//*[@name='{}']".format(
                            re.sub(r'.*:', '', elementType, count=1)
                        )
                    )
                )

            except Exception, e:
                fewi.addFEWI(
                    severity=fewi.Severity.FATAL,
                    cause='FATAL_TYPE_NOT_FOUND',
                    message='Could not find referenced type. Found: {}'.format(
                        re.sub(r'.*:', '', elementType, count=1)
                    )
                )

    def getAnyAttribs(self, attributes, excludeList):
        return [
            attributes[key] 
            for key in attributes.keys()
            if key not in excludeList
        ]


    def xmlToBool(self, xmlBool):
        return True if xmlBool == 'true' else False if xmlBool == 'false' else None

    def xmlToInt(self, xmlInt):
        return None if xmlInt is None else 'unbounded' if xmlInt == 'unbounded' else int(xmlInt)


    def buildTree(self, rootNode, parent=None):
        children = []

        for child in rootNode:
            children.append(self.buildTree(child, parent=rootNode))

        rootTag = rootNode.tag
        rootAttributes = rootNode.attrib
        rootObj = None

        if ('name' in rootAttributes) and (rootAttributes['name'] in self.objectMap):
            return

        if rootTag.endswith('all'):
            rootObj = All(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'maxOccurs', 'minOccurs']
                ),
                maxOccurs=self.xmlToInt(rootNode.get('maxOccurs')),
                minOccurs=self.xmlToInt(rootNode.get('minOccurs'))
            )

        elif rootTag.endswith('annotation'):
            rootObj = Annotation(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID']
                )
            )

        elif rootTag.endswith('any'):
            rootObj = Any(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'namespace', 'processContents', 'maxOccurs', 'minOccurs']
                ),
                namespace=rootNode.get('namespace'),
                processContents=rootNode.get('processContents'),
                maxOccurs=self.xmlToInt(rootNode.get('maxOccurs')),
                minOccurs=self.xmlToInt(rootNode.get('minOccurs'))
            )

        elif rootTag.endswith('anyAttribute'):
            rootObj = AnyAttribute(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'namespace', 'processContents']
                ),
                namespace=rootNode.get('namespace'),
                processContents=rootNode.get('processContents')
            )

        elif rootTag.endswith('appinfo'):
            rootObj = AppInfo(
                source=rootNode.get('source'),
                children=children
            )

        elif rootTag.endswith('attribute'):
            rootObj = Attribute(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'default', 'fixed', 'form', 'name', 'ref', 'type', 'use']
                ),
                default=rootNode.get('default'),
                fixed=rootNode.get('fixed'),
                form=rootNode.get('form'),
                name=rootNode.get('name'),
                ref=rootNode.get('ref'),
                elementType=self.resolveType(
                    rootNode.get('type'),
                    rootNode.get('name')
                ),
                use=rootNode.get('use')
            )

        elif rootTag.endswith('attributeGroup'):
            rootObj = AttributeGroup(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'name', 'ref']
                ),
                name=rootNode.get('name'),
                ref=rootNode.get('ref')
            )

        elif rootTag.endswith('choice'):
            rootObj = Choice(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'maxOccurs', 'minOccurs']
                ),
                maxOccurs=self.xmlToInt(rootNode.get('maxOccurs')),
                minOccurs=self.xmlToInt(rootNode.get('minOccurs'))
            )

        elif rootTag.endswith('complexContent'):
            rootObj = ComplexContent(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'mixed']
                ),
                mixed=rootNode.get('mixed')
            )

        elif rootTag.endswith('complexType'):
            rootObj = ComplexType(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'name', 'abstract', 'mixed', 'block', 'final']
                ),
                name=rootNode.get('name'),
                abstract=self.xmlToBool(
                    rootNode.get('abstract')
                ),
                mixed=self.xmlToBool(
                    rootNode.get('mixed')
                ),
                block=rootNode.get('block'),
                final=rootNode.get('final')
            )

        elif rootTag.endswith('documentation'):
            rootObj = Documentation(
                source=rootNode.get('source'),
                language=rootNode.get('language'),
                content=rootNode.get('content')
            )

        elif rootTag.endswith('element'):
            rootObj = Element(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = [
                        'ID',
                        'name',
                        'ref',
                        'type',
                        'substitutionGroup',
                        'default',
                        'fixed',
                        'form',
                        'maxOccurs',
                        'minOccurs',
                        'nillable',
                        'abstract',
                        'block',
                        'final'
                    ]
                ),
                name=rootNode.get('name'),
                ref=rootNode.get('ref'),
                elementType=self.resolveType(
                    rootNode.get('type'),
                    rootNode.get('name')
                ),
                substitutionGroup=rootNode.get('substitutionGroup'),
                default=rootNode.get('default'),
                fixed=rootNode.get('fixed'),
                form=rootNode.get('form'),
                maxOccurs=self.xmlToInt(rootNode.get('maxOccurs')),
                minOccurs=self.xmlToInt(rootNode.get('minOccurs')),
                nillable=self.xmlToBool(
                    rootNode.get('nillable')
                ),
                abstract=self.xmlToBool(
                    rootNode.get('abstract')
                ),
                block=rootNode.get('block'),
                final=rootNode.get('final')
            )

        elif rootTag.endswith('extension'):
            rootObj = Extension(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'base']
                ),
                base=rootNode.get('base')
            )

        elif rootTag.endswith('field'):
            rootObj = Field(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'xpath']
                ),
                xpath=rootNode.get('xpath')
            )

        elif rootTag.endswith('group'):
            rootObj = Group(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'name', 'ref', 'maxOccurs', 'minOccurs']
                ),
                name=rootNode.get('name'),
                ref=rootNode.get('ref'),
                maxOccurs=self.xmlToInt(rootNode.get('maxOccurs')),
                minOccurs=self.xmlToInt(rootNode.get('minOccurs'))
            )

        elif rootTag.endswith('import'):
            rootObj = Import(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'namespace', 'schemaLocation']
                ),
                namespace=rootNode.get('namespace'),
                schemaLocation=rootNode.get('schemaLocation')
            )

        elif rootTag.endswith('include'):
            rootObj = Include(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'schemaLocation']
                ),
                schemaLocation=rootNode.get('schemaLocation')
            )

        elif rootTag.endswith('key'):
            rootObj = Key(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'name']
                ),
                name=rootNode.get('name')
            )

        elif rootTag.endswith('keyref'):
            rootObj = KeyRef(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'name']
                ),
                name=rootNode.get('name'),
                refer=rootNode.get('refer')
            )

        elif rootTag.endswith('list'):
            rootObj = List(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'type']
                ),
                elementType=self.resolveType(
                    rootNode.get('type'),
                    rootNode.get('name')
                )
            )

        elif rootTag.endswith('notation'):
            rootObj = Notation(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'system', 'name', 'public']
                ),
                system=rootNode.get('system'),
                name=rootNode.get('name'),
                public=rootNode.get('public')
            )

        elif rootTag.endswith('redefine'):
            rootObj = Redefine(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'schemaLocation']
                ),
                schemaLocation=rootNode.get('schemaLocation')
            )

        elif rootTag.endswith('restriction'):
            rootObj = Restriction(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'base']
                ),
                base=rootNode.get('base'),

                # Be sure to remove namespace from beginning of tag
                parentType=re.sub(r'\{.+\}', '', parent.tag, count=1)
            )

        elif rootTag.endswith('schema'):
            rootObj = Schema(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = [
                        'ID',
                        'attributeFormDefault',
                        'elementFormDefault',
                        'blockDefault',
                        'finalDefault',
                        'targetNamespace',
                        'version',
                        'xmlns'
                    ]
                ),
                attributeFormDefault=rootNode.get('attributeFormDefault'),
                elementFormDefault=rootNode.get('elementFormDefault'),
                blockDefault=rootNode.get('blockDefault'),
                finalDefault=rootNode.get('finalDefault'),
                targetNamespace=rootNode.get('targetNamespace'),
                version=rootNode.get('version'),
                xmlns=rootNode.get('xmlns')
            )

        elif rootTag.endswith('selector'):
            rootObj = Selector(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'xpath']
                ),
                xPath=rootNode.get('xpath')
            )

        elif rootTag.endswith('sequence'):
            rootObj = Sequence(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'minOccurs', 'maxOccurs']
                ),
                minOccurs=self.xmlToInt(rootNode.get('minOccurs')),
                maxOccurs=self.xmlToInt(rootNode.get('maxOccurs'))
            )

        elif rootTag.endswith('simpleContent'):
            rootObj = SimpleContent(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID']
                )
            )

        elif rootTag.endswith('simpleType'):
            rootObj = SimpleType(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'name']
                ),
                name=rootNode.get('name')
            )

        elif rootTag.endswith('union'):
            rootObj = Union(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'memberTypes']
                ),
                memberTypes=rootNode.get('memberTypes')
            )

        elif rootTag.endswith('unique'):
            rootObj = Unique(
                ID=rootNode.get('ID'),
                children=children,
                attributes=self.getAnyAttribs(
                    attributes = rootAttributes,
                    excludeList = ['ID', 'name']
                ),
                name=rootNode.get('name')
            )

        elif rootTag.endswith('enumeration'):
            rootObj = Enumeration(rootNode.get('value'))

        elif rootTag.endswith('fractionDigits'):
            rootObj = FractionDigits(rootNode.get('value'))

        elif rootTag.endswith('length'):
            rootObj = Length(rootNode.get('value'))

        elif rootTag.endswith('maxExclusive'):
            rootObj = MaxExclusive(rootNode.get('value'))

        elif rootTag.endswith('maxInclusive'):
            rootObj = MaxInclusive(rootNode.get('value'))

        elif rootTag.endswith('maxLength'):
            rootObj = MaxLength(rootNode.get('value'))

        elif rootTag.endswith('minExclusive'):
            rootObj = MinExclusive(rootNode.get('value'))

        elif rootTag.endswith('minInclusive'):
            rootObj = MinInclusive(rootNode.get('value'))

        elif rootTag.endswith('minLength'):
            rootObj = MinLength(rootNode.get('value'))

        elif rootTag.endswith('pattern'):
            rootObj = Pattern(rootNode.get('value'))

        elif rootTag.endswith('totalDigits'):
            rootObj = TotalDigits(rootNode.get('value'))

        elif rootTag.endswith('whiteSpace'):
            rootObj = WhiteSpace(rootNode.get('value'))

        else:
            fewi.addFEWI(
                severity=fewi.Severity.FATAL,
                cause='CONSTRUCTION_ERROR',
                message='Could not model element tag found in DOM tree. Found {} tag.'.format(rootTag)
            )

        if 'name' in rootAttributes:
                self.objectMap[rootAttributes['name']] = rootObj

        self.objCount = self.objCount + 1

        return rootObj
