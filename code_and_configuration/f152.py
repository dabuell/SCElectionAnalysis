""" This is the docstring.
"""
#import sys
#from collections import defaultdict

from globalstuff import globalivos
from globalstuff import globalpebs
from globalstuff import globaltextforcode

from f152functions import skipthisline

from oneevent import OneEvent
from onepeb import OnePEB
from oneivo import OneIvo

######################################################################
## CLASS FOR THE 152 FILE
class F152:
    """ This is the docstring.
    """
    ######################################################################
    ## BOILERPLATE FUNCTIONS
    def __init__(self, infilenameprefix, theconfig):
        """ This is the docstring.
        """
        self._eventcount = 0

        self.readdata(infilenameprefix, theconfig.getdate())

    def __str__(self):
        """ This is the docstring.
        """
        s_local = 'F152: '
        s_local += 'EVENTCOUNT: %7d\n' % (self._eventcount)
        return s_local
    ## END OF BOILERPLATE FUNCTIONS
    ######################################################################

    ######################################################################
    ## READDATA: READ THE DATA FILE
    def readdata(self, prefix, thedate):
        """ This is the docstring.
        """
        print('F152: prefix and date', prefix, thedate)

        filetoread = open(prefix + 'EL152')

        firstline = True
#        linecounter = 0
        for line in filetoread:
#            print('BEFORE %6d %5d %s' % (linecounter, len(line),line))

            ##########################################################
            ## get the different fields from the lines of 152
            line = line.replace('\n', '')
            if firstline:
                firstline = False
                continue
            if skipthisline(line):
                continue

            if line[0:7].strip() != '':
                ivonumber = line[0:7].strip()

            if line[7:15].strip() != '':
                pebnumber = line[7:15].strip()

            ## now get the data from the rest of the line
            pebtype = line[15:20].strip()
            date152 = line[20:33].strip()
            time152 = line[33:42].strip()
            code152 = line[42:52].strip()
            text152 = line[52:].strip()

            ##########################################################
            ## add to or update the PEB dictionary
            if pebnumber in globalpebs:
                thispeb = globalpebs[pebnumber]
            else:
                thispeb = OnePEB(pebnumber, pebtype, '152')
            thispeb.setfoundin152(True)

            globalpebs[pebnumber] = thispeb

            ##########################################################
            ## create the events
            thisevent = OneEvent(ivonumber, pebnumber, \
                                 pebtype, date152, time152, code152)

            ## store text for codes so we don't need to dup the text
            ## don't worry about overwriting
            globaltextforcode[code152] = text152

            ##########################################################
            ## add to or update the ivo dictionary
            if ivonumber in globalivos:
                thisivo = globalivos[ivonumber]
            else:
                thisivo = OneIvo(ivonumber, '152')
#                print('NEW 152 IVO: %s: %s' % (ivonumber, thisivo))

            self._eventcount += 1
            thisivo.addtoevents(thisevent)

            globalivos[ivonumber] = thisivo
    ## END OF READDATA
    ######################################################################

#    ######################################################################
#    ## TOSTRINGEVENTLOG: output the entire event log as a string
#    def tostringeventlog(self):
#        """ This is the docstring.
#        """
#        s_local = 'EVENT LOG INFORMATION'
#        for event in self._eventlog:
#            s_local += '%s\n' % (event)
#        s_local += 'END OF EVENT LOG INFORMATION'
#        return s_local
#    ## END OF TOSTRINGEVENTLOG
#    ######################################################################
## END OF F152
##########################################################################
