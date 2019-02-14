""" This is the docstring.
"""
from globalstuff import DUMMYIVO
from globalstuff import globalpebs
from globalstuff import globalivos

from oneivo import OneIvo
from onepeb import OnePEB

######################################################################
## CLASS FOR THE 68A FILE
class F68A:
    """ This is the docstring.
    """
#    _DUMMYIVO = DUMMYIVO
#    _DUMMYPEB = DUMMYPEB

    ######################################################################
    ## BOILERPLATE FUNCTIONS
    def __init__(self):
        """ This is the docstring.
        """
        self._dummyivo = DUMMYIVO
        self._filename = ''

    def __str__(self):
        """ This is the docstring.
        """
        local_s = 'F68A: '
        local_s += '\n'
#        local_s += 'EVENTCOUNT: %7d\n' % (self._eventcount)
        return local_s
    ## END OF BOILERPLATE FUNCTIONS
    ######################################################################

    ######################################################################
    ## READDATA: READ THE DATA FILE AND PROCESS IMMEDIATE ISSUES
    def readdata(self, prefix, date):
        """ This is the docstring.
        """
        print('F68A: prefix and date', prefix, date)

        self._filename = prefix + 'EL68A'
        filetoread = open(self._filename)

        _previousivo = ''
        _previouspeb = ''
        _firstline = True
        for line in filetoread:

            ##########################################################
            ## three kinds of lines we want to look for

            if 'Audit Data collected for' in line:
                line = line.strip()
                thisdatetime = line[0:15].strip()
                thisivonumber = line[-7:]
#                print('AUDIT DATA X%sX Z%sZ %s' % (thisdatetime, thisivonumber, line))
                if thisivonumber in globalivos:
                    thisivo = globalivos[thisivonumber]
                else:
                    print('NEW IVO IN 68A', thisivonumber)
                    thisivo = OneIvo(thisivonumber, '68A')
                thisivo.addtomemorycollectiontime(thisdatetime)
                globalivos[thisivonumber] = thisivo

            if 'PEB votes retrieved for' in line:
                line = line.strip()
                thisdatetime = line[0:15].strip()
                thispebnumber = line[-6:]
#                print('PEB DATA X%sX Z%sZ %s' % (thisdatetime, thispebnumber, line))
                if thispebnumber in globalpebs:
                    thispeb = globalpebs[thispebnumber]
                else:
                    print('NEW PEB IN 68A', thispebnumber)
                    thispeb = OnePEB(thispebnumber, 'XXX', '68A')
                thispeb.addtovotecollectiontime(thisdatetime)
                thispeb.setfoundin68a(True)
                globalpebs[thispebnumber] = thispeb
#                print('PEB VOTES', line)

            if 'cands' in line:
                print('ERROR: CANDS ', line)

    ## END OF READDATA
    ######################################################################
