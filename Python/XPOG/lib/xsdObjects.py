#!/usr/bin/python2 -tt

import utils
import fewi


def addAnnotationError(elementType):
    fewi.addFEWI(
        severity = fewi.Severity.WARNING,
        cause = 'SCHEMA_VALIDATION_ERROR',
        message = '{} element already contains Annotation elemen, second one will be ignored.'.format(elementType)
    )



class BaseObject(object):
    """
        The object that (nearly) all XSD elements inherit from.
    """

    def __init__(self, ID=None, children=[], attributes=None):
        self.ID = ID
        self.children = []
        self.addChild(utils.tameNoneList(children))
        self.attributes = utils.tameNoneList(attributes)
        self.isValid = True


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            self.children.extend(newChildren)

        else:
            self.children.append(newChildren)


    def __str__(self):
        return self.ID if self.ID is not None else 'Could not find identifier'



class All(BaseObject):
    """
        Specifies that the child elements can appear in any order and that each
        child element can occur zero or one time.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        maxOccurs=None,
        minOccurs=None
    ):
        self.hasAnnotation = False
        super(All, self).__init__(ID, children, attributes)

        if maxOccurs is None:
            self.maxOccurs = 1

        elif (isinstance(maxOccurs, int) and maxOccurs >= 0) or maxOccurs == 'unbounded':
            self.maxOccurs = maxOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'maxOccurs was: {}, must be an integer value greater than or equal to 0 or unbounded.'.format(maxOccurs)
            )
            self.isValid = False

        if minOccurs is None:
            self.minOccurs = 1

        elif isinstance(minOccurs, int) and minOccurs >= 0:
            self.minOccurs = minOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'minOccurs was: {}, must be an integer value greater than or equal to 0.'.format(minOccurs)
            )
            self.isValid = False



    def addChild(self, newChildren):
        # If we've been handed a list, break it up and add individual elements
        # for easier processing.
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            # Only allowed one annotation per All element, so check that we
            # haven't already found one.
            if self.hasAnnotation:
                addAnnotationError('All')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, Element):
            self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'All element contains sub-element that is not one of the following types: Annotation, Element. Founc {}'.format(type(newChildren))
            )
            self.isValid = False



class Annotation(BaseObject):
    """
        Top level element that specifies schema comments. The comments serve as
        inline documentation.
    """

    def __init__(self, ID=None, children=[], attributes=None):
        super(Annotation, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, (AppInfo, Documentation)):
            self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Annotation can only contain one of the following element types: AppInfo, Documentation. Found: {}'.format(type(newChildren))
            )
            self.isValid = False



class AnyBase(BaseObject):
    """
        Base object for Any and AnyAttribute, contains simple error checking and
        common attributes.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        namespace=None,
        processContents=None
    ):
        self.hasAnnotation = False
        super(Any, self).__init__(ID, children, attributes)
        self.namespace = namespace

        if processContents in ['lax', 'skip', 'strict']:
            self.processContents = processContents

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'processContents was: {}, must be one of the folowing values: {}'.format(processContents, str(['lax', 'skip', 'strict']))
            )
            self.isValid = False


    def addChild(self, newChildren):
        # If we've been handed a list, break it up and add individual elements
        # for easier processing.
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            # Only allowed one annotation per All element, so check that we
            # haven't already found one.
            if self.hasAnnotation:
                addAnnotationError(type(self))

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Any or AnyAttribute element contains sub-element that is not of type Annotation. Found {}'.format(type(newChildren))
            )
            self.isValid = False



class Any(AnyBase):
    """
        Enables the author to extend the XML document with elements not
        specified by the schema.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        namespace=None,
        processContents=None,
        maxOccurs=None,
        minOccurs=None
    ):
        super(Any, self).__init__(
            ID,
            children,
            attributes,
            namespace,
            processContents,
        )

        if maxOccurs is None:
            self.maxOccurs = 1

        elif (isinstance(maxOccurs, int) and maxOccurs >= 0) or maxOccurs == 'unbounded':
            self.maxOccurs = maxOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'maxOccurs was: {}, must be an integer value greater than or equal to 0 or unbounded.'.format(maxOccurs)
            )
            self.isValid = False

        if minOccurs is None:
            self.minOccurs = 1

        elif isinstance(minOccurs, int) and minOccurs >= 0:
            self.minOccurs = minOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'minOccurs was: {}, must be an integer value greater than or equal to 0.'.format(minOccurs)
            )
            self.isValid = False



class AnyAttribute(AnyBase):
    """
        Enables the author to extend the XML document with attributes not
        specified by the schema.
    """

    def __init__(self, ID=None, children=[], attributes=None, namespace=None, processContents=None):
        super(AnyAttribute, self).__init__(
            ID,
            children,
            attributes,
            namespace,
            processContents,
        )



class AppInfo(object):
    """
        Not based on BaseObject.

        Specifies information to be used by the application. This element must
        go within an annotation element.
    """

    def __init__(self, source=None, children=[]):
        super(AppInfo, self).__init__()
        self.source = source
        self.children = children
        self.isValid = True

    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            self.children.extend(newChildren)

        else:
            self.children.append(newChildren)



class Attribute(BaseObject):
    """
        Defines an attribute.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        default=None,
        fixed=None,
        form=None,
        name=None,
        ref=None,
        elementType=None,
        use=None
    ):
        self.hasAnnotation = False
        super(Attribute, self).__init__(ID, children, attributes)

        # Attribute has some odd rules so we will run through the validation for
        # them now.
        if default is not None and fixed is not None:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Attribute element is not allowed default and fixed value at the same time. Found default: {} and fixed: {}'.format(default, fixed)
            )
            self.isValid = False

        if name is not None and ref is not None:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Attribute element is not allowed name and ref values at the same time. Found name: {} and ref: {}'.format(name, ref)
            )
            self.isValid = False

        if ref is not None and (form is not None or elementType is not None):
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'If Attribute element contains a ref value then it cannot contain form or type values. Found ref: {}, form: {}, type: {}'.format(ref, form, elementType)
            )
            self.isValid = False

        self.default = default
        self.fixed = fixed
        self.form = form
        self.name = name
        self.ref = ref
        self.elementType = elementType
        self.use = use
        self.hasSimpleType = False


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError("Attribute")

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, SimpleType):
            if self.ref is not None:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'Attribute element cannot contain ref attribute and SimpleType element at the same time. Found ref: {} and SimpleType: {}'.format(ref, str(SimpleType))
                )
                self.isValid = False

            elif self.hasSimpleType:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'Attribute element already contains SimpleType element, second one will be ignored.'
                )
                self.isValid = False

            else:
                self.hasSimpleType = True
                self.children.append(newChildren)



class AttributeGroup(BaseObject):
    """
        Used to group a set of attribute declarations so that they can be
        incorporated as a group into complex type definitions.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        name=None,
        ref=None
    ):
        self.hasAnnotation = False
        super(AttributeGroup, self).__init__(ID, children, attributes)

        # Validation for AttributeGroup
        if name is not None and ref is not None:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'AttributeGroup cannot contain name and ref attributes at the same time. Found name: {} and ref: {}'.format(name, ref)
            )
            self.isValid = False

        self.name = name
        self.ref = ref
        self.hasAnyAttribute = False


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('AttributeGroup')
                
            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (Attribute, AttributeGroup)):
            self.children.append(newChildren)

        elif isinstance(newChildren, AnyAttribute):
            if self.hasAnyAttribute:
                fewi.addFEWI(
                    severity = fewi.Severity.WARNING,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'AttributeGroup already contains AnyAttribute element, the second one will be ignored.'
                )

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'AttributeGroup can only contain the following element types: Annotation, Attribute, AttributeGroup, AnyAttribute. Found: {}'.format(type(newChildren))
            )
            self.isValid = False


    def __str__(self):
        return self.ID if self.ID is not None else self.name if self.name is not None else 'Could not find identifier'



class Choice(BaseObject):
    """
        Allows any one of the sub-elements to be present within the containing
        element.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        maxOccurs=None,
        minOccurs=None,
    ):
        self.hasAnnotation = False
        super(Choice, self).__init__(ID, children, attributes)

        if maxOccurs is None:
            self.maxOccurs = 1

        elif (isinstance(maxOccurs, int) and maxOccurs >= 0) or maxOccurs == 'unbounded':
            self.maxOccurs = maxOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'maxOccurs was: {}, must be an integer value greater than or equal to 0 or unbounded.'.format(maxOccurs)
            )
            self.isValid = False

        if minOccurs is None:
            self.minOccurs = 1

        elif isinstance(minOccurs, int) and minOccurs >= 0:
            self.minOccurs = minOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'minOccurs was: {}, must be an integer value greater than or equal to 0.'.format(minOccurs)
            )
            self.isValid = False



    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Choice')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (Element, Group, Choice, Sequence, Any)):
            self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Choice can only contain one of the following element types: Annotation, Element, Group, Choice, Sequence, Any. Found: {}'.format(type(newChildren))
            )
            self.isValid = False



class ComplexContent(BaseObject):
    """
    Defines extensions or restrictions on a complex type that contains mixed
    content or elements only.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        mixed=None
    ):
        self.hasAnnotation = False
        super(ComplexContent, self).__init__(ID, children, attributes)
        self.mixed = False if mixed is None else mixed
        self.hasNonAnnotation = False


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(self, newChildren)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('ComplexContent')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (Restriction, Extension)):
            if self.hasNonAnnotation:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'ComplexContent cannot contain more than one non-Annotation sub-element.'
                )
                self.isValid = False

            else:
                self.hasNonAnnotation = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'ComplexContent can only contain the following element types: Annotation, Restriction, Extension. Found: {}'.format(type(newChildren))
            )
            self.isValid = False



class ComplexType(BaseObject):
    """
        Defines a complex type. A complex type element is an XML element that
        contains other elements and/or attributes.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        name=None,
        abstract=None,
        mixed=None,
        block=None,
        final=None
    ):
        # This object has a lot of optional children that appear a maximum of
        # once in weird orders so here are some flags to help simplify the
        # checks later.
        self.hasAnnotation = False
        self.hasSimpleContent = False
        self.hasComplexContent = False
        self.hasGroup = False
        self.hasAll = False
        self.hasChoice = False
        self.hasSequence = False
        self.hasAnyAttribute = False

        self.name = name
        self.abstract = False if abstract is None else abstract
        self.mixed = False if mixed is None else mixed
        self.block = block
        self.final = final
        super(ComplexType, self).__init__(ID, children, attributes)



    def addChild(self, newChildren):
        allowedChildren = (
            Annotation,
            SimpleContent,
            ComplexContent,
            Group,
            All,
            Choice,
            Sequence,
            Attribute,
            AttributeGroup,
            AnyAttribute
        )

        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('ComplexType')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, SimpleContent):
            if self.hasSimpleContent:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'ComplexType cannot contain more than one SimpleContent element.'
                )
                self.isValid = False

            else:
                if self.mixed:
                    fewi.addFEWI(
                        severity = fewi.Severity.ERROR,
                        cause = 'SCHEMA_VALIDATION_ERROR',
                        message = 'ComplexType is not allowed mixed to be true with a SimpleContent sub-element.'
                    )
                    self.isValid = False

                else:
                    self.hasSimpleContent = True
                    self.children.append(newChildren)

        elif isinstance(newChildren, ComplexContent):
            if self.hasComplexContent:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'ComplexType cannot contain more than one ComplexContent element.'
                )
                self.isValid = False

            else:
                self.hasComplexContent = True
                self.children.append(newChildren)

        elif isinstance(newChildren, Group):
            if self.hasGroup:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'ComplexType cannot contain more than one Group element.'
                )
                self.isValid = False

            else:
                self.hasGrou = True
                self.children.append(newChildren)

        elif isinstance(newChildren, All):
            if self.hasAll:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'ComplexType cannot contain more than one All element.'
                )
                self.isValid = False

            else:
                self.hasAll = True
                self.children.append(newChildren)

        elif isinstance(newChildren, Choice):
            if self.hasChoice:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'ComplexType cannot contain more than one Choice element.'
                )
                self.isValid = False

            else:
                self.hasChoice = True
                self.children.append(newChildren)

        elif isinstance(newChildren, Sequence):
            if self.hasSequence:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'ComplexType cannot contain more than one Sequence element.'
                )
                self.isValid = False

            else:
                self.hasSequence = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (Attribute, AttributeGroup)):
            self.children.append(newChildren)

        elif isinstance(newChildren, AnyAttribute):
            if self.hasAnyAttribute:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'ComplexType cannot contain more than one AnyAttribute element.'
                )
                self.isValid = False

            else:
                self.hasAnyAttribute = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'ComplexType can only contain the following element types: {}. Found: {}'.format(allowedChildren, type(newChildren))
            )
            self.isValid = False



class Documentation(object):
    """
        Used to enter text for comments into a schema. This element must go
        inside an annotation element.
    """

    def __init__(self, source=None, language=None, content=None):
        self.source = source
        self.language = language
        self.content = content

    def addChild(self, newContent):
        self.content.append(newContent)



class Element(BaseObject):
    """
        Defines a basic element.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        name=None,
        ref=None,
        elementType=None,
        substitutionGroup=None,
        default=None,
        fixed=None,
        form=None,
        maxOccurs=None,
        minOccurs=None,
        nillable=None,
        abstract=None,
        block=None,
        final=None
    ):
        self.hasAnnotation = False
        self.hasChildType = False
        self.name = name
        self.ref = ref
        self.elementType = elementType
        self.substitutionGroup = substitutionGroup
        self.default = default
        self.fixed = fixed
        self.form = form
        super(Element, self).__init__(ID, children, attributes)

        if maxOccurs is None:
            self.maxOccurs = 1

        elif (isinstance(maxOccurs, int) and maxOccurs >= 0) or maxOccurs == 'unbounded':
            self.maxOccurs = maxOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'maxOccurs was: {}, must be an integer value greater than or equal to 0 or unbounded.'.format(maxOccurs)
            )
            self.isValid = False

        if minOccurs is None:
            self.minOccurs = 1

        elif isinstance(minOccurs, int) and minOccurs >= 0:
            self.minOccurs = minOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'minOccurs was: {}, must be an integer value greater than or equal to 0.'.format(minOccurs)
            )
            self.isValid = False

        self.nillable = False if nillable is None else nillable
        self.abstract = False if abstract is None else abstract
        self.block = block
        self.final = final



    def addChild(self, newChildren):
        allowedChildren = (
            Annotation,
            SimpleType,
            ComplexType,
            Unique,
            Key,
            KeyRef
        )

        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Element')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (SimpleType, ComplexType)):
            if self.hasChildType:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'Element can only contain one SimpleType, one ComplexType, or neither.'
                )
                self.isValid = False

            else:
                self.hasChildType = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (Unique, Key, Ref)):
            self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Element can only contain the following element types: {}. Found: {}'.format(allowedChildren, ype(newChildren))
            )
            self.isValid = False



class Extension(BaseObject):
    """
        Extends an existing SimpleType or ComplexType element.
    """

    def __init__(self, ID=None, children=[], attributes=None, base=None):
        self.hasAnnotation = False
        self.hasSequenceContents = False
        self.hasAnyAttribute = False
        self.base = base
        super(Extension, self).__init__(ID, children, attributes)



    def addChild(self, newChildren):
        allowedChildren = (
            Annotation,
            Group,
            All,
            Choice,
            Sequence,
            Attribute,
            AttributeGroup,
            AnyAttribute
        )

        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Extension')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (Group, All, Choice, Sequence)):
            if self.hasSequenceContents:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'Extension can only contain one of the following element types: Group, All, Choice, Sequence.'
                )
                self.isValid = False

            else:
                self.hasSequence = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (Attribute, AttributeGroup)):
            self.children.append(newChildren)

        elif isinstance(newChildren, AnyAttribute):
            if self.hasAnyAttribute:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'ComplexType cannot contain more than one AnyAttribute element.'
                )
                self.isValid = False

            else:
                self.hasAnyAttribute = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Extension can only contain the following element types: {}. Found: {}'.format(allowedChildren, type(newChildren))
            )
            self.isValid = False



class Field(BaseObject):
    """
        Specifies an XPath expression that specifies the value used to define an
        identityconstraint.
    """

    def __init__(self, ID=None, children=[], attributes=None, xpath=None):
        self.hasAnnotation = False
        self.xpath = xpath
        super(Field, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Field')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Field can only contain Annotation elements. Found: {}'.format(type(newChildren))
            )
            self.isValid = False



class Group(BaseObject):
    """
        Used to define a group of elements to be used in ComplexType
        definitions.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        name=None,
        ref=None,
        maxOccurs=None,
        minOccurs=None
    ):
        self.hasAnnotation = False
        self.hasSequenceContents = False
        super(Group, self).__init__(ID, children, attributes)

        if name is not None and ref is not None:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Group cannot have a name and ref attribute at the same time.'
            )
            self.isValid = False

        else:
            self.name = name
            self.ref = ref

        if maxOccurs is None:
            self.maxOccurs = 1

        elif (isinstance(maxOccurs, int) and maxOccurs >= 0) or maxOccurs == 'unbounded':
            self.maxOccurs = maxOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'maxOccurs was: {}, must be an integer value greater than or equal to 0 or unbounded.'.format(maxOccurs)
            )
            self.isValid = False

        if minOccurs is None:
            self.minOccurs = 1

        elif isinstance(minOccurs, int) and minOccurs >= 0:
            self.minOccurs = minOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'minOccurs was: {}, must be an integer value greater than or equal to 0.'.format(minOccurs)
            )
            self.isValid = False



    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Group')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (All, Choice, Sequence)):
            if self.hasSequenceContents:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'Group can only contain one of th following element types: All, Choice, Sequence.'
                )
                self.isValid = False

            else:
                self.hasSequenceContents = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Group can only contain the following elements: Annotation, All, Choice, Sequence. Found: {}'.format(type(newChildren))
            )
            self.isValid = False



class Import(BaseObject):
    """
        Used to add multiple schemaswith different target namespace to a
        document.
    """

    def __init__(self, ID=None, children=[], attributes=None, namespace=None, schemaLocation=None):
        self.hasAnnotation = False
        self.namespace = namespace
        self.schemaLocation = schemaLocation
        super(Import, self).__init__(ID, children, attributes)



    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Import')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Import can only contain Annotation elements. Found: {}'.format(type(newChildren))
            )
            self.isValid = False



class Include(BaseObject):
    """
        Used to add multiple schemas with the same target namespace to a
        document.
    """

    def __init__(self, schemaLocation, ID=None, children=[], attributes=None):
        self.hasAnnotation = False
        self.schemaLocation = schemaLocation
        super(Include, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Include')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Include can only contain Annotation elements. Found: {}'.format(type(newChildren))
            )
            self.isValid = False



class KeyBase(BaseObject):
    """
        Base object for Key and KeyRef
    """

    def __init__(self, name, ID=None, children=[], attributes=None):
        self.hasAnnotation = False
        self.hasSelector = False
        self.hasField = False
        self.name = name
        super(Key, self).__init__(ID, children, attributes)



    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Key')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, Selector):
            if self.hasSelector:
                fewi.addFEWI(
                    severity = fewi.Severity.WARNING,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = '{} can only contain one Selector element. Second one shall be ignored.'.format(type(self))
                )

            else:
                self.hasSelector = True
                self.children.append(newChildren)

        elif isinstance(newChildren, Field):
            self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = '{} can only contain the following elements: Annotation, Selector, Field. Found: {}'.format(type(self), type(newChildren))
            )
            self.isValid = False



class Key(KeyBase):
    """
        Specifies an attribute or element value as a key (unique, non-nullable,
        and always present) within the containing element in an instance
        document.

        The key must contain the following in order:
            - One Selector element
            - One or more field elements
    """

    def __init__(self, name, ID=None, children=[], attributes=None):
        super(Key, self).__init__(name, ID, children, attributes)



class KeyRef(BaseObject):
    """
        Specifies that an attribute or element value corresonds to those of the
        specified key or unique element.

        The keyref must contain the following in order:
            - One Selector element
            - One or more Field elements
    """

    def __init__(self, name, refer, ID=None, children=[], attributes=None):
        self.refer = refer
        super(KeyRef, self).__init__(name, ID, children, attributes)



class List(BaseObject):
    """
        Defines a SimpleType element as a list of values of a specified data
        type.
    """

    def __init__(self, ID=None, children=[], attributes=None, elementType=None):
        self.hasAnnotation = False
        self.hasSimpleType = False
        self.elementType = elementType
        super(List, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('List')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, SimpleType):
            if self.hasSimpleType:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'List element cannot contain more than one SimpleType.'
                )
                self.isValid = False

            elif self.elementType is not None:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'List cannot contain type attribute and SimpleType element.'
                )
                self.isValid = False

            else:
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'List can only contain the following elements: Annotation, SimpleType. Found: {}'.format(type(newChildren))
            )



class Notation(BaseObject):
    """
        Describes the format of non-XML data within an XML document.
    """

    def __init__(
        self,
        name,
        public,
        ID=None,
        children=[],
        attributes=None,
        system=None
    ):
        self.hasAnnotation = False
        self.name = name
        self.public = public
        self.system = system
        super(Notation, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Notation')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Notation can only contain Attribute elements. Found: {}'.format(type(newChildren))
            )



class Redefine(BaseObject):
    """
        Redefines simple and complex types, groups, and attribute groups from an
        external schema.
    """

    def __init__(self, schemaLocation, ID=None, children=[], attributes=None):
        self.schemaLocation = schemaLocation
        super(Redefine, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        allowedChildren = (
            Annotation,
            SimpleType,
            ComplexType,
            Group,
            AttributeGroup
        )

        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, allowedChildren):
            self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Redefine can only contain the following elements: {}. Found: {}'.format(allowedChildren, type(newChildren))
            )
            self.isValid = False



class Restriction(BaseObject):
    """
        Defines restrictions on a SimpleType, SimpleContent, ComplexContent
        definition.
    """

    def __init__(self, base, parentType, ID=None, children=[], attributes=None):
        self.hasAnnotation = False
        self.hasSimpleType = False
        self.hasMainContents = False
        self.hasAnyAttribute = False
        self.parentType = parentType
        self.base = base
        super(Restriction, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif self.parentType == 'simpleType':
            if isinstance(newChildren, Annotation):
                if self.hasAnnotation:
                    addAnnotationError('Restriction')

                else:
                    self.hasAnnotation = True
                    self.children.append(newChildren)

            elif isinstance(newChildren, SimpleType):
                if self.hasSimpleType:
                    fewi.addFEWI(
                        severity = fewi.Severity.ERROR,
                        cause = 'SCHEMA_VALIDATION_ERROR',
                        message = 'Restriction element inside SimpleType can only contain at most one SimpleType element.'
                    )
                    self.isValid = False

                else:
                    self.hasSimpleType = True
                    self.children.append(newChildren)

            elif isinstance(newChildren, (MinInclusive, MaxInclusive, MinExclusive, MaxExclusive, TotalDigits, FractionDigits, Length, MinLength, MaxLength, Enumeration, WhiteSpace, Pattern)):
                self.children.append(newChildren)

            else:
                fewi.addFEWI(
                    severity =fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'Restriction element inside SimpleType can only contain the following:' +
                    " Annotation," +
                    " SimpleType," +
                    " MinInclusive," +
                    " MaxInclusive," +
                    " MinExclusive," +
                    " MaxExclusive," +
                    " TotalDigits," +
                    " FractionDigits," +
                    " Length," +
                    " MinLength," +
                    " MaxLength," +
                    " Enumeration," +
                    " WhiteSpace," +
                    " Pattern." +
                    ' Found: {}'.format(type(newChildren))
                )
                self.isValid = False

        elif self.parentType == 'simpleContent':
            if isinstance(newChildren, Annotation):
                if self.hasAnnotation:
                    addAnnotationError('Restriction')

                else:
                    self.hasAnnotation = True
                    self.children.append(newChildren)

            elif isinstance(newChildren, SimpleType):
                if self.hasSimpleType:
                    fewi.addFEWI(
                        severity = fewi.Severity.ERROR,
                        cause = 'SCHEMA_VALIDATION_ERROR',
                        message = 'Restriction element inside SimpleContent can only contain at most one SimpleType element.'
                    )
                    self.isValid = False

                else:
                    self.hasSimpleType = True
                    self.children.append(newChildren)

            elif isinstance(newChildren, (
                    MinInclusive,
                    MaxInclusive,
                    MinExclusive,
                    MaxExclusive,
                    TotalDigits,
                    FractionDigits,
                    Length,
                    MinLength,
                    MaxLength,
                    Enumeration,
                    WhiteSpace,
                    Pattern
                )
            ):
                self.children.append(newChildren)

            elif isinstance(newChildren, (Attribute, AttributeGroup)):
                self.children.append(newChildren)

            elif isinstance(newChildren, AnyAttribute):
                if self.hasAnyAttribute:
                    fewi.addFEWI(
                        severity = fewi.Severity.ERROR,
                        cause = 'SCHEMA_VALIDATION_ERROR',
                        message = 'Restriction element inside SimpleContent can only contain at most one AnyAttribute element.'
                    )
                    self.isValid = False

            else:
                fewi.addFEWI(
                    severity =fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'Restriction element inside SimpleContent can only contain the following:' +
                    " Annotation," +
                    " SimpleType," +
                    " MinInclusive," +
                    " MaxInclusive," +
                    " MinExclusive," +
                    " MaxExclusive," +
                    " TotalDigits," +
                    " FractionDigits," +
                    " Length," +
                    " MinLength," +
                    " MaxLength," +
                    " Enumeration," +
                    " WhiteSpace," +
                    " Pattern," +
                    " Attribute," +
                    " AttributeGroup," +
                    " AnyAttribute. Found: {}'.format(type(newChildren))"
                )

        elif self.parentType == 'complexContent':
            if isinstance(newChildren, Annotation):
                if self.hasAnnotation:
                    addAnnotationError('Restriction')

                else:
                    self.hasAnnotation = True
                    self.children.append(newChildren)

            elif isinstance(newChildren, (Group, All, Choice, Sequence)):
                if self.hasMainContents:
                    fewi.addFEWI(
                        severity = fewi.Severity.ERROR,
                        cause = 'SCHEMA_VALIDATION_ERROR',
                        message = 'Restriction element inside ComplexContent can only have at most one of the following: Group, All, Choice, Sequence.'
                    )
                    self.isValid = False

                else:
                    self.hasMainContents = True
                    self.children.append(newChildren)

            elif isinstance(newChildren, (Attribute, AttributeGroup)):
                self.children.append(newChildren)

            elif isinstance(newChildren, AnyAttribute):
                if self.hasAnyAttribute:
                    fewi.addFEWI(
                        severity = fewi.Severity.ERROR,
                        cause = 'SCHEMA_VALIDATION_ERROR',
                        message = 'Restriction can only contain at most one AnyAttribute element.'
                    )
                    self.isValid = False

            else:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'Restriction element inside ComplexContent can only contain the following elements: (Annotation, Group, All, Choice, Sequence, Attribute, AttributeGroup, AnyAttribute). Found: {}'.format(type(newChildren))
                )
                self.isValid = False

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Restriction element can only be contained within one of the following: SimpleType, SimpleContent, ComplexContent. Found: {}'.format(self.parentType)
            )
            self.isValid = False



class Schema(BaseObject):
    """
        Defines the root element of the schema.
    """

    def __init__(
        self,
        ID=None,
        children=[],
        attributes=None,
        attributeFormDefault=None,
        elementFormDefault=None,
        blockDefault=None,
        finalDefault=None,
        targetNamespace=None,
        version=None,
        xmlns=None
    ):
        self.attributeFormDefault = 'unqualified' if attributeFormDefault is None else attributeFormDefault
        self.elementFormDefault = 'unqualified' if elementFormDefault is None else elementFormDefault
        self.blockDefault = blockDefault
        self.finalDefault = finalDefault
        self.targetNamespace = targetNamespace
        self.version = version
        self.xmlns = xmlns
        super(Schema, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        allowedChildren = (
            Include,
            Import,
            Redefine,
            Annotation,
            SimpleType,
            ComplexType,
            Group,
            AttributeGroup,
            Element,
            Attribute,
            Notation,
            Annotation
        )

        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, allowedChildren):
            self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Schema element can only contain the following: {}. Found: {}'.format(str(allowedChildren), type(newChildren))
            )
            self.isValid = False



class Selector(BaseObject):
    """
        Specifies an XPath expression that selects a set of elements for an
        identity constraint (Unique, Key, KeyRef elements).
    """

    def __init__(self, xPath, ID=None, children=[], attributes=None):
        self.hasAnnotation = False
        self.xPath = xPath
        super(Selector, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Selector')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Selector can only contain Annotation elements. Found: {}'.format(type(newChildren))
            )



class Sequence(BaseObject):
    """
        Specifies that the child elements must appear in a sequence. Each child
        element can occur from 0 to any number of times.
    """

    def __init__(self, ID=None, children=[], attributes=None, minOccurs=None, maxOccurs=None):
        self.hasAnnotation = False
        super(Sequence, self).__init__(ID, children, attributes)

        if maxOccurs is None:
            self.maxOccurs = 1

        elif (isinstance(maxOccurs, int) and maxOccurs >= 0) or maxOccurs == 'unbounded':
            self.maxOccurs = maxOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'maxOccurs was: {}, must be an integer value greater than or equal to 0 or unbounded.'.format(maxOccurs)
            )
            self.isValid = False

        if minOccurs is None:
            self.minOccurs = 1

        elif isinstance(minOccurs, int) and minOccurs >= 0:
            self.minOccurs = minOccurs

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'minOccurs was: {}, must be an integer value greater than or equal to 0.'.format(minOccurs)
            )
            self.isValid = False



    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Sequence')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (Element, Group, Choice, Sequence, Any)):
            self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Sequence element can only contain the following elements: Annotation, Element, Group, Choice, Sequence, Any. Found: {}'.format(type(newChildren))
            )
            self.isValid = False



class SimpleContent(BaseObject):
    """
        Contains extensions or restrictions on a text-only ComplexType or on a
        SimpleType as content and contains no elements.
    """

    def __init__(self, ID=None, children=None, attributes=None):
        self.hasAnnotation = False
        self.hasContent = False
        super(SimpleContent, self).__init__(ID, children, attributes)



    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('SimpleContent')

            else:
                self.hasAnnotation = True,
                self.children.append(newChildren)

        elif isinstance(newChildren, (Restriction, Extension)):
            if self.hasContent:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'SimpleContent element must contain exactly one of either Restriction or Extension.'
                )
                self.isValid = False

            else:
                self.hasContent = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'SimpleContent can only contain the following elements: Annotation, Restriction, Extension. Found: {}'.format(type(newChildren))
            )
            self.isValid = False



class SimpleType(BaseObject):
    """
        Defines a simple type and specifies the constraints and information
        about the values of attributes or text-only information.
    """

    def __init__(self, ID=None, children=[], attributes=None, name=None):
        self.hasAnnotation = False
        self.hasContent = False
        self.name = name
        super(SimpleType, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('SimpleType')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, (Restriction, List, Union)):
            if self.hasContent:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'SimpleType element must contain one of either of the following: Restriction, List, Union'
                )
                self.isValid = False

            else:
                self.hasContent = True
                self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'SimpleType can only contain the following elements: Annotation, Restriction, List, Union. Found: {}'.format(type(newChildren))
            )



class Union(BaseObject):
    """
        Defines a SimpleType as a collection (union) of values from specified
        simple data types.
    """

    def __init__(self, ID=None, children=[], attributes=None, memberTypes=None):
        self.hasAnnotation = False
        self.memberTypes = memberTypes
        super(Union, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Union')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, SimpleType):
            self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Union element can only contain the following elements: Annotation, SimpleType. Found: {}'.format(newChildren)
            )



class Unique(BaseObject):
    """
        Defines that an element or an attribute value must be unique within the
        scope. The Unique element must contain the following (in order):
         - one and only one Selector element
         - one or more field elements
    """

    def __init__(self, name, ID=None, children=[], attributes=None):
        self.hasAnnotation = False
        self.hasSelector = False
        self.name = name
        super(Unique, self).__init__(ID, children, attributes)


    def addChild(self, newChildren):
        if isinstance(newChildren, list):
            for child in newChildren:
                self.addChild(child)

        elif isinstance(newChildren, Annotation):
            if self.hasAnnotation:
                addAnnotationError('Unique')

            else:
                self.hasAnnotation = True
                self.children.append(newChildren)

        elif isinstance(newChildren, Selector):
            if self.hasSelector:
                fewi.addFEWI(
                    severity = fewi.Severity.ERROR,
                    cause = 'SCHEMA_VALIDATION_ERROR',
                    message = 'Unique element must contain only one Selector element.'
                )
                self.isValid = False

            else:
                self.hasSelector = True
                self.children.append(newChildren)

        elif isinstance(newChildren, Field):
            self.children.append(newChildren)

        else:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Unique element can only contain the following: Annotation, Selector, Field. Found: {}'.format(newChildren)
            )
            self.isValid = False



class BaseConstraint(object):
    """
        Base object for constraints used in Restriction element.
    """

    def __init__(self, value):
        self.value = value
        self.isValid = True



class Enumeration(BaseConstraint):
    """
        Defines a list of acceptable values.
    """

    def __init__(self, value):
        super(Enumeration, self).__init__(value)



class FractionDigits(BaseConstraint):
    """
        Specifies the maximum number of decimal places allowed. Must be equal to
        or greater than zero.
    """

    def __init__(self, value):
        super(FractionDigits, self).__init__(value)

        if self.value < 0:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'FractionDigits value must be greater than or equal to zero.'
            )
            self.isValid = False



class Length(BaseConstraint):
    """
        Specifies the exact number of characters or list items allowed. Must be
        equal to or greater than zero.
    """

    def __init__(self, value):
        super(Length, self).__init__(value)

        if self.value < 0:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'Length value must be greater than or equal to zero.'
            )
            self.isValid = False



class MaxExclusive(BaseConstraint):
    """
        Specifies the upper bounds for numeric values exclusively (the value
        must be less than this).
    """

    def __init__(self, value):
        super(MaxExclusive, self).__init__(value)



class MaxInclusive(BaseConstraint):
    """
        Specifies the upper bounds for numeric values inclusively (the value
        must be less than or equal to this).
    """

    def __init__(self, value):
        super(MaxInclusive, self).__init__(value)



class MaxLength(BaseConstraint):
    """
        Specifies the maximum number of characters or list items allowed. Must
        be equal to or greater than zero.
    """

    def __init__(self, value):
        super(MaxLength, self).__init__(value)

        if self.value < 0:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'MaxLength value must be greater than or equal to zero.'
            )
            self.isValid = False



class MinExclusive(BaseConstraint):
    """
        Specifies the lower bounds for numeric values exclusively (the value
        must be greater than this).
    """

    def __init__(self, value):
        super(MinExclusive, self).__init__(value)



class MinInclusive(BaseConstraint):
    """
        Specifies the lower bounds for numeric values inclusively (the value
        must be greater than or equal to this).
    """

    def __init__(self, value):
        super(MinInclusive, self).__init__(value)



class MinLength(BaseConstraint):
    """
        Specifies the minimum number of characters or list items allowed. Must
        be equal to or greater than zero.
    """

    def __init__(self, value):
        super(MinLength, self).__init__(value)

        if self.value < 0:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'MinLength value must be greater than or equal to zero.'
            )
            self.isValid = False



class Pattern(BaseConstraint):
    """
        Defines the exact sequence of characters that are acceptable.
    """

    def __init__(self, value):
        super(Pattern, self).__init__(value)



class TotalDigits(BaseConstraint):
    """
        Specifies the maximum number of digites allowed. Mus be greater than
        zero.
    """

    def __init__(self, value):
        super(TotalDigits, self).__init__(value)

        if self.value <= 0:
            fewi.addFEWI(
                severity = fewi.Severity.ERROR,
                cause = 'SCHEMA_VALIDATION_ERROR',
                message = 'TotalDigits value must be greater than zero.'
            )
            self.isValid = False



class WhiteSpace(BaseConstraint):
    """
        Specifies how white spece characters (line feeds, tabs, spaces, and
        carriage returns) are handled.
    """

    def __init__(self, value):
        super(WhiteSpace, self).__init__(value)
