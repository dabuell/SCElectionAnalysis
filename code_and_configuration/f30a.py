""" This is the docstring.
"""
#import sys
#from collections import defaultdict

from globalstuff import globalcontestcandidate
from globalstuff import globalpcts
from globalstuff import globalupdate30Aresults

#from oneevent import OneEvent
#from oneivo import OneIvo
#from onepeb import OnePEB

from onepct import OnePct

######################################################################
## CLASS FOR THE 30A FILE
class F30A:
    """ This is the docstring.
    """
    ######################################################################
    ## BOILERPLATE FUNCTIONS
    def __init__(self, prefix, date, county):
        """ This is the docstring.
        """
#        self._dummyivo = DUMMYIVO

        # this to keep pylint happy
        self._ballots = []
        self._filename = ''
        self._pctname = ''
        self._pctnumber = ''
        self._registered = 0

        self.readdata(prefix, date, county)

    def __str__(self):
        """ This is the docstring.
        """
        local_s = 'F30A: '
        local_s += '\n'
        return local_s
    ## END OF BOILERPLATE FUNCTIONS
    ######################################################################

    ######################################################################
    ## LOOK UP CANDIDATE NAMES
    def lookupcandidatenames(self, county, line):
        """ This is the docstring.
        """
#        print('LINE IS', self._pctnumber, line)
        for concand in globalcontestcandidate:
#            localcandidate = cand.replace('_', ' ')
            if 'NOVEMBER' in line:
                return
            if 'November' in line:
                return
            if ' No. ' in line:
                return
            if (county == 'Charleston') and ('North Area' in line):
                return
            if (county == 'Charleston') and ('Charleston' in line):
                return
            if (county == 'Greenwood') and ('Greenwood' in line):
                return
            if (county == 'Greenville') and ('Greenville' in line):
                return
#            if ('hampton' == county) and (' North' in line):
#                return
            if (county == 'richland') and ('Statewide' in line):
                return
            if self._pctname in line:
                return
            concandsplit = concand.split()
#            localcontest = concandsplit[0]
            localcandidate = concandsplit[1].replace('_', ' ')
            if localcandidate in line:
#                print('FOUND IN LINE %s : %s : %s' % (self._pctnumber, concand, line))
#                globalupdatecandidatecontestfrom30A(county, self._pctnumber, cand, line)
                globalupdate30Aresults(county, self._pctnumber, concand, line)

        return

    ## END OF LOOK UP CANDIDATE NAMES
    ######################################################################

    ######################################################################
    ## READDATA: READ THE DATA FILE AND PROCESS IMMEDIATE ISSUES
    def readdata(self, prefix, date, county):
        """ This is the docstring.
        """
        print('F30A: prefix and date', prefix, date)

        filetoread = open(prefix + 'EL30A')

        lines = []
        for line in filetoread:
            lines.append(line)

        linelimit = len(lines)
#        print('LINELIMIT', linelimit)
        linesub = 0
        while linesub < linelimit:
            line = lines[linesub]

            if len(line) < 4:
                linesub += 1
                continue
            if len(line.split()) < 2:
                linesub += 1
                continue
            possiblepctnumber = line[0:4]
            if (possiblepctnumber >= '0000') and (possiblepctnumber <= '9999'):
                self._pctnumber = possiblepctnumber
                self._pctname = line[4:].strip()
                if self._pctnumber not in globalpcts:
                    print('NEW PCT %s %s' % (self._pctnumber, self._pctname))
                    onepct = OnePct(self._pctnumber, self._pctname, '30A')
                else:
                    onepct = globalpcts[self._pctnumber]

            # here's the new 12 June 2018 kluge to get the numbers
            if 'BALLOTS CAST - TOTAL' in line:
                line = line.replace('.', ' ')
                line = line.replace('BALLOTS CAST - TOTAL', ' ')
                line = line.replace(',', '') # commas in numbers

#                linesplit = line.split()
                self._ballots = []
                for item in line.split():
                    self._ballots.append(int(item))
                if (self._pctnumber >= '0000') and (self._pctnumber <= '9999'):
                    onepct.updatefrom30a(self._registered, self._ballots, county)
                    globalpcts[self._pctnumber] = onepct
            linesub += 1

    ## END OF READDATA
    ######################################################################

## END OF 30A
##########################################################################
