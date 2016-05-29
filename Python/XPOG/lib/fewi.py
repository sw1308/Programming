#!/usr/bin/python -tt

import sys

fewiList = []



class Severity(object):
    UNKNOWN, FATAL, ERROR, WARNING, INFO = range(5)
    
    sevMap = {
        UNKNOWN : 'UNKNOWN',
        FATAL : 'FATAL',
        ERROR : 'ERROR',
        WARNING : 'WARNING',
        INFO : 'INFO'
    }

    # Really python, I have to do this?
    @staticmethod
    def tostring(severity):
        return Severity.sevMap[severity]



def addFEWI(severity=Severity.UNKNOWN, cause='UNKNOWN', message=None):
    """
        If fewi severity is FATAL or UNKNOWN, reports the error immediately and exits,
        otherwise adds message to fewi list and resumes.
    """

    fewiString = '{}\n\tCause: {}\n\t\t{}'.format(Severity.tostring(severity), cause, message)

    if severity < Severity.ERROR:
        print fewiString
        sys.exit(1)
    
    else:
        fewiList.append(fewiString)
        return True
