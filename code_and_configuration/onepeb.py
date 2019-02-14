""" This is the docstring.
"""
#import sys
#from collections import defaultdict

#from globalstuff import *
from globalstuff import globalivos

######################################################################
## CLASS FOR ONE PEB
##
class OnePEB:
    """ This is the docstring.
    """

    ##################################################################
    ## BOILERPLATE FUNCTIONS
    def __init__(self, pebnumber, pebtype, createdfrom):
        """ This is the docstring.
        """
        self._foundin68a = False # set from 68A file
        self._foundin152 = False # set from 152 file
        self._usedforclosing = False # set from 152 file

        self._createdfrom = createdfrom # says where the creation of this instance took place
        self._pebnumber = pebnumber # set from 152 file
        self._pebtype = pebtype # set from 152 file

        self._ivoset = set() # set from 152 file
        self._pcts = set() # set from 152 file HOW CAN THIS BE SET FROM 152?
        self._votecollectiontime = [] # set from 68A file

    def __str__(self):
        local_s = ''
        local_s += '(%3s)' %  (self._createdfrom)
        local_s += ' %7s %4s' %  (self._pebnumber, self._pebtype)
        if self._usedforclosing:
            local_s += ' CLO-T'
        else:
            local_s += ' CLO-F'

        if self._foundin152:
            local_s += ' 152-T'
        else:
            local_s += ' 152-F'

        if self._foundin68a:
            local_s += ' 68A-T'
        else:
            local_s += ' 68A-F'

        # we need to process this now and append after the next loop
        local_ss = ' ('
        for ivonumber in sorted(self._ivoset):
            local_ss += ' %s' % (ivonumber)
            ivo = globalivos[ivonumber]
            for pct in ivo.getpctnumbers():
                self._pcts.add(pct)
        local_ss += ')'

        local_s += ' ('
        for pct in sorted(self._pcts):
            local_s += ' %s' % (pct)
        local_s += ')'

        local_s += local_ss

        local_s += ' ('
        for time in self._votecollectiontime:
            local_s += ' %s' % (time)
        local_s += ')'

        return local_s

    ##################################################################
    ## ACCESSORS
    def getcreatedfrom(self): return self._createdfrom
    def getfoundin68a(self): return self._foundin68a
    def getfoundin152(self): return self._foundin152
    def getusedforclosing(self): return self._usedforclosing
    def getpebnumber(self): return self._pebnumber
    def getpebtype(self): return self._pebtype
    def getvotecollectiontime(self): return self._votecollectiontime

    ##################################################################
    ## MUTATORS
    def setfoundin68a(self, what):
        """ This is the docstring.
        """
        self._foundin68a = what

    def setfoundin152(self, what):
        """ This is the docstring.
        """
        self._foundin152 = what

    def setusedforclosing(self, what):
        """ This is the docstring.
        """
        self._usedforclosing = what

    ##################################################################
    ## OTHER FUNCTIONS

    ## called from oneivo; this peb shows up in an event for this ivo
    def addtoivoset(self, newentry):
        """ This is the docstring.
        """
        self._ivoset.add(newentry)

    ## called from 68A code
    def addtovotecollectiontime(self, newentry):
        """ This is the docstring.
        """
        self._votecollectiontime.append(newentry)
    ##

    ## called from the 'write' function
    def headerstring(self):
        """ This is the docstring.
        """
        sss = 'PEB LEGEND:\n'
        sss += '     Created from\n'
        sss += '     PEB number\n'
        sss += '     PEB type\n'
        sss += '     Used for closing (T/F)\n'
        sss += '     Found in 152 (T/F)\n'
        sss += '     Found in 68A (T/F)\n'
        sss += '     Pcts for this PEB\n'
        sss += '     Ivos for this PEB\n'
        sss += '     Data upload time from 68A\n'
        return sss
    ##
    ##################################################################

##
######################################################################
