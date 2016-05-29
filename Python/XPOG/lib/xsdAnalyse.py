#!/usr/bin/python2 -tt

import fewi

class XSDAnalyser(object):
    """

        Analyse generated object model and generate libraries.

        Analyse phase
        ------------------------------------------------------------------------
        Performs minimization and optimization on object model to try and reduce
        the number of output objects (depending on CLI args).

        --minimize
            0 - No minimization

                XSDAnalyser will not reduce the number of output objects or
                files, this can result in unpredictably large libraries with
                multiple small files, each with one object in.

            1 - Flatten empty containers

                XSDAnalyser will attempt to reduce constructor complexity by
                flattening containers down to python lists if the container
                meets the following criteria:
                    - All elements in the container are the same type.
                    - The container only holds elements. If it contains three
                      objects and a string, then it will not qualify.

            2 - Reduce library size

                After performing the steps in 1, XSDAnalyser will attempt to
                reduce the number of output files by aggregating objects with
                similar inherited types into the same file. If there is a type
                with less than 5 objects inheriting from it, then XSDAnalyser
                shall continue moving up the type inheritance tree until that
                number becomes greater than 5, or until it cannot find a higher
                inheritance type.

            3 - Extreme

                After performing the steps in 1, XSDAnalyser will place all
                objects into a single file instead of in seperate folders.

        --Documentation
            Whether or not XSDAnalyser will output python documentation
            (discovered from annotation and documentation elements from the
            schema).

    """

    def __init__(self, inputModel):
        super(XSDAnalyser, self).__init__()

        self.inputModel = inputModel
        self.analysedOutput = None


    def getOptionalArgs(self, element):
        optionalList = []

        for child in element.children:
            if hasattr(child, 'minOccurs') and child.minOccurs == 0:
                optionalList.append(child.name)


    def analyse(self, miniLevel, outputDocs):
        pass
