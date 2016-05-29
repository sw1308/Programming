#XSD Python Object Generator
[TOC]

##Introduction

Welcome! This is the docuentation for XPOG, below is the important
informtion about how to use it and how it works.


##Terminology

In this document I will be using several pieces of terminology defined here:

>DOM Tree - The Document Object Model representing the entire input XSD file.
Object Model - The internal python representation of the DOM Tree.
Context Model - The result of the analysis phase on the Object Model, contains some implementation information.
Library Files/Objects - The resultant python files and objects that XPOG produces.


##Usage

XPOG is used through the command line. It requires python2.7 to be installed on
the system that it is being used on. XPOG assumes that python is located at
`/usr/bin/python2` however it can be invoked with `python2` or `python` if the
appropriate paths have been set up.


###Arguments

####-h --help

Displays the following message:

```
usage: XPOG.py [-h] [-d] [-l {UNIX,WINDOWS}] [-m {0,1}] [-o DIR] [-t] [-v]
               INPUT [INPUT ...]

                XPOG XSD Python Object Generator
    ------------------------------------------------------------
    Processes XML schema and outputs python object libraries in
    order to programmatically write out schematically valid XML.
    ------------------------------------------------------------
            

positional arguments:
  INPUT                 Specify input XSD to ingest, can be multiple files if
                        -multiple-input is set.

optional arguments:
  -h, --help            show this help message and exit
  -d, --documentation   Output python documentation discovered from the
                        schema.
  -l {UNIX,WINDOWS}, --line-endings {UNIX,WINDOWS}
                        Specify line endings style for output, UNIX for LF
                        style and WINDOWS for CRLF style. Defaults to UNIX.
  -m {0,1,2,3}, --minimize {0,1,2,3}
                        Specify level of minimization to perform on object
                        model during analyse phase.
  -o DIR, --output DIR  Save output files to specified directory. Defaults to
                        current directory.
  -t, --type-check      Generated objects will perform type checking on their
                        inputs to enforce schema type correctness.
  -v, --version         Print version information and exit.
```


####-d --documentation

Whether or not XSDAnalyser will output python documentation, discovered from
annotation and documentation elements from the schema. Empty documentation will
still be output if this flag is not set, under the assumption that the user will
fill out documentation themselves.

For example, consider the following XSD (An element from AUTOSAR 4.2.2 Schema):

```xml
<xsd:attribute name="S" type="AR:STRING--SIMPLE">
 <xsd:annotation>
  <xsd:documentation>
   Checksum calculated by the user's tool environment for an ArObject. May be
   used in an own tool environment to determine if an ArObject has changed. The
   checksum has no semantic meaning for an AUTOSAR model and there is no
   requirement for AUTOSAR tools to manage the checksum.
  </xsd:documentation>
  <xsd:appinfo source="tags">
   mmt.qualifiedName="ARObject.checksum";pureMM.maxOccurs="1";pureMM.minOccurs="
   0";xml.attribute="true";xml.name="S"
  </xsd:appinfo>
 </xsd:annotation>
</xsd:attribute>
```

With `--documentation` set this would be output:

```python
    class STRING__SIMPLE(BaseObject):
        """
            Checksum calculated by the user's tool environment for an ArObject. May be
            used in an own tool environment to determine if an ArObject has changed. The
            checksum has no semantic meaning for an AUTOSAR model and there is no
            requirement for AUTOSAR tools to manage the checksum.
        """
        ...
```

However without it we would get this:

```python
    class STRING__SIMPLE(BaseObject):
        """
        """
        ...
```


####-l --line-endings

Simply specifies which line endings to use when outputting the library files.
Can be either UNIX or WINDOWS, defaults to UNIX.


####-m --minimize

Tells the analyser (discussed later in the document) how much optimisation to
perform on the object model. This can be an integer in the range 0 - 3, default
is 0.

 - 0 (No Minimization)
 - 1 (Flatten Empty Lists)
 - 2 (Reduce Library Size)
 - 3 (Extreme)

These options are decribed in more detail the Analyse phase section.


####-o --output

Defines the output directory in which XPOG will write the library files. This can be
defined relative to the current working directory or as an absolute path.
Defaults to current working directory.


####-t --type-check

When this flag is set, XPOG will output library objects that check for type
correctness. As an example, if a library object contains a list of elements of
type `boolean` then it shall iterate through that list once it is populated to
ensure that all elements in the list adhere to the xsd schema definition for
boolean (i.e. `true` or `false`). This is important for certain built-in types
as well as schema defined types due to certain built-ins (dateTime, duration,
etc.) requiring specific formats.


####-v --version

Print version information and exit.


##Phases

The main run-time consists of four phases:

 1. Parse Phase
 2. Construction Phase
 3. Analyse Phase
 4. Output Phase

 These phases are described below:

###Parse

This phase is a pretty basic one, it simply uses `xml.etree` to ingest the XSD
file and generate a DOM tree for it. This tree is ten passed back to the main
thread for further processing.

The important code for parsing is done here:

```python
    def parseFile(self):
        try:
            self.parsedFile = ElementTree.parse(self.inputFile)

        except Exception, e:
            raise ParseError(str(e))
```

The code itself if fairly straightforward as we just beed the basic DOM tree and
nothing else.


###Construct

This phase requires some more complicated processing, it pulls in
`lib.xsdObjects` as a repository for notable elements in xsd trees. We then
create one xsdObject for each element we find in the tree.

```python
    if ('name' in rootAttributes) and (rootAttributes['name'] in self.objectMap):
            return

    if rootTag.endswith('any'):
        rootObj = Any(
            ID=rootNode.get('ID'),
            children=children,
            attributes=self.getAnyAttribs(
                attributes = rootAttributes,
                excludeList = ['ID', 'maxOccurs', 'minOccurs']
            ),
            maxOccurs=self.xmlToInt(rootNode.get('maxOccurs')),
            minOccurs=self.xmlToInt(rootNode.get('minOccurs'))
        )

    ...
```

The first `if` statement is important to ensure that we don't generate
duplicates of objects we have already come across. This can happen if you have
an `element` that's typed by some `simpleType`, we would resolve the type
reference, but if we encounter that `simpleType` again then we don't want to
have to build a second version of that object.

The second `if` statement is essentially one very large `if elif` statement
that constructs each object based on it's element tag.

Below is a brief sample of `lib.xsdObjects`:

```python
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
```

xsdConstruct also contains some regexes for built-in types, these are necessary
for type-checking in the output library:

```python
typeMap = {
    "base64Binary"       : re.compile(r'^[0-9a-zA-Z=/]*$', flags=re.M|re.S|re.U),
    "boolean"            : re.compile(r'(?:true|false)', flags=re.M|re.S|re.U),
    ...
}

```


###Analyse

This is where the complicated processing happens. In this phase we take the
object model generated in the construction phase and analyse it's structure in
an attempt to reduce it's size and complexity. We also convert the object model
into a more contextual model that contains implementation information ready for
the output phase.

There are a couple of phases of optimization and minimization that this phase
can run through, these are the following:

 - No minimisation
    This makes the phase quite a bit quicker as we don't need to do anthing past
    literally outputting the necessary model.

 - Flatten Empty Lists
    This tries to reduce the complexity of object instantiation by finding
    compound lists and containers that all contain the same type and flattening
    it into a single list.

 - Reduce Library Size

    This tries to group items in the model together into the same files in an
    attempt to reduce the number of folders and files that get output.

 - Extreme
    This method will output all objects into the same file after performing the
    other minimizations. This creates a singe python output file that can be
    imported from to gain access to every library object.

The Analyse phase can also output any annotation it finds as documentation.


###Output
