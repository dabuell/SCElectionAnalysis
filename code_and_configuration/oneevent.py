""" This is the docstring.
"""
#import sys
#from collections import defaultdict

#from globalstuff import *
from globalstuff import globaltextforcode

######################################################################
## CLASS FOR ONE EVENT
##
class OneEvent:
    """ This is the docstring.
    """

    ##################################################################
    ## BOILERPLATE FUNCTIONS
    def __init__(self, ivonumber, pebnumber, pebtype, date152, time152, code152):
        """ This is the docstring.
        """
        self._ivonumber = ivonumber
        self._pebnumber = pebnumber
        self._pebtype = pebtype
        self._date152 = date152
        self._time152 = time152
        self._code152 = code152

    def __str__(self):
        """ This is the docstring.
        """
        s_1 = '%7s%8s' %  (self._ivonumber, self._pebnumber)
        s_2 = '%5s%13s' %  (self._pebtype, self._date152)
        s_3 = '%9s%10s' %  (self._time152, self._code152)

        s_4 = ' %s' %(globaltextforcode[self._code152])

        local_s = s_1 + s_2 + s_3 + s_4
        return local_s

    ##################################################################
    ## ACCESSORS
    def getivonumber(self):
        """ This is the docstring.
        """
        return self._ivonumber
    def getpebnumber(self):
        """ This is the docstring.
        """
        return self._pebnumber
    def getpebtype(self):
        """ This is the docstring.
        """
        return self._pebtype
    def getdate152(self):
        """ This is the docstring.
        """
        return self._date152
    def gettime152(self):
        """ This is the docstring.
        """
        return self._time152
    def getcode152(self):
        """ This is the docstring.
        """
        return self._code152

    ##################################################################
    ## MUTATORS

    ##################################################################
    ## GENERAL FUNCTIONS
