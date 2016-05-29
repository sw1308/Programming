#!/usr/bin/python2 -tt

from xml.etree import ElementTree



class ParseError(Exception):
    def __init__(self, message):
        self.message = message


    def __str__(self):
        return repr(self.message)



class XSDIngestor(object):
    def __init__(self, fileObject=None):
        self.cleanupAfter = False
        self.parsedFile = None

        # We were not given a fileObject so we will have to get our own.
        if not fileObject:
            filename = raw_input('Please input the name of the XSD file you would like to be parsed: ')
            self.cleanupAfter = True

            try:
                fileObject = open(filename)
            except Exception, e:
                raise e

        self.inputFile = fileObject


    def parseFile(self):
        try:
            self.parsedFile = ElementTree.parse(self.inputFile)

        except Exception, e:
            raise ParseError(str(e))

        finally:
            if self.cleanupAfter:
                self.inputFile.close()


    def getParseResult(self):
        return self.parseResult


if __name__ == '__main__':
    ingestor = XSDIngestor()
    ingestor.parseFile()
