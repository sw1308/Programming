#!/usr/bin/python2 -tt

import os
import sys
import argparse
import importlib

from lib import xsdIngest, xsdConstruct, xsdAnalyse, fewi



class ProgramInfo(object):
    SHORT_NAME = 'XPOG'
    NAME = 'XSD Python Object Generator'
    VERSION = 0.1



class XPOG(object):
    """
        Entry point for XPOG, begins by initialising arguments and continues from there.
    """

    def __init__(self):
        self.inputFiles = None
        self.parsedFiles = []
        self.constructedModels = []
        self.outputModels = []
        self.outputDir = None
        self.lineEndings = None

        self.parseArgs()

        self.processXSD()

        # Processing is complete, print status and fewi messages
        statusMessage = 'Proccessing completed.\n{}'.format('' if len(fewi.fewiList) == 0 else 'The following messages were generated during runtime:')

        print statusMessage

        for message in fewi.fewiList:
            print message


    def parseArgs(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="""\
                XPOG XSD Python Object Generator
    ------------------------------------------------------------
    Processes XML schema and outputs python object libraries in
    order to programmatically write out schematically valid XML.
    ------------------------------------------------------------
            """
        )

        # Setup arguments
        parser.add_argument('INPUT',
            nargs='+',
            help='Specify input XSD to ingest, can be multiple files if -multiple-input is set.'
        )

        parser.add_argument(
            '-d', '--documentation',
            action='store_true',
            help='Output python documentation discovered from the schema.'
        )

        parser.add_argument(
            '-l', '--line-endings',
            choices=['UNIX', 'WINDOWS'],
            default='UNIX',
            help='Specify line endings style for output, UNIX for LF style and  WINDOWS for CRLF style. Defaults to UNIX.'
        )


        parser.add_argument(
            '-m', '--minimize',
            type=int,
            choices=range(4),
            default='0',
            help='Specify level of minimization to perform on object model during analyse phase.'
        )

        parser.add_argument('-o', '--output',
            default = os.getenv('PWD'),
            metavar='DIR',
            help='Save output files to specified directory. Defaults to current directory.'
        )

        parser.add_argument(
            '-t', '--type-check',
            action='store_true',
            help='Generated objects will perform type checking on their inputs to enforce schema type correctness.'
        )

        parser.add_argument('-v', '--version',
            action='store_true',
            help='Print version information and exit.'
        )

        # Collect arguments that have been used
        argv = parser.parse_args()

        if argv.version:
            print '{} ({}) version {}'.format(ProgramInfo.NAME, ProgramInfo.SHORT_NAME, ProgramInfo.VERSION)
            sys.exit(0)

        self.inputFiles = argv.INPUT
        self.outputDir = argv.output
        self.lineEndings = argv.line_endings
        self.minimize = argv.minimize
        self.documentation = argv.documentation


    def processXSD(self):
        for filename in self.inputFiles:
            print 'Beginning to process file: {}'.format(filename)
            try:
                print '> Parsing XSD'
                with open(filename, 'r') as file:
                    ingestor = xsdIngest.XSDIngestor(file)
                    ingestor.parseFile()
                    self.parsedFiles.append(ingestor.parsedFile)
                print '< Parsing XSD'

            except Exception, e:
                fewi.addFEWI(
                    severity = fewi.Severity.FATAL,
                    cause = 'FILE_ERROR',
                    message = str(e)
                )

        for tree in self.parsedFiles:
            try:
                print '> Constructing contextual model from DOM tree'

                constructor = xsdConstruct.XSDConstructor(tree)
                constructor.construct()
                self.constructedModels.append(constructor.finishedModel)

                print '< Constructing contextual model from DOM tree'

            except Exception, e:
                fewi.addFEWI(
                    severity = fewi.Severity.FATAL,
                    cause = 'CONSTRUCTION_ERROR',
                    message = str(e)
                )

        for model in self.constructedModels:
            try:
                print '> Analysing contextual model'
                analyser = xsdAnalyse.XSDAnalyser(model)
                analyser.analyse(
                    miniLevel=self.minimize,
                    outputDocs=self.documentation
                )
                # self.outputModels.append(analyser.analysedOutput)

                print '< Analysing contextual model'

            except Exception, e:
                fewi.addFEWI(
                    severity = fewi.Severity.FATAL,
                    cause = 'ANALYSE_ERROR',
                    message = str(e)
                )



if __name__ == '__main__':
    XPOG()
