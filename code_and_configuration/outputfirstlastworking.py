""" This is the docstring.
"""
#import sys
#from collections import defaultdict

#import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt

#from globalstuff import *
from globalstuff import DUMMYDATE
from globalstuff import globalconverttimetoepoch
from globalstuff import globalcreatetimeblocks
from globalstuff import globaldisplaytimeblocks
from globalstuff import globalivos

######################################################################
## CLASS FOR FIRSTLASTWORKING
class FirstLastWorking:
    """ This is the docstring.
    """

    ##################################################################
    ## init
    def __init__(self):
        """ This is the docstring.
        """
        self._beginelectiondayepoch = ''
        self._endelectiondayepoch = ''

    ##################################################################
    ## WRITECLOSINGTIMES: write the closing times histogram counts
    def writeclosingtimes(self, filenameprefix, county):
        """ This is the docstring.
        """
        local_s = ''

        nocloseignorecount = 0
        earlyignorecount = 0
        lateignorecount = 0
        earlys = ''
        lates = ''
        nocloses = ''
        closetimes = []
        for ivonumber, ivo in sorted(globalivos.items()):
            ivoclosingtime = ivo.getdatetimeclosing()
            if ivoclosingtime[0] == DUMMYDATE:
                nocloses += 'NO CLOSING IGNORE %s\n' % (ivo)
                nocloseignorecount += 1
                continue
            thistime = globalconverttimetoepoch(ivoclosingtime[0], ivoclosingtime[1])
            if thistime <= self._beginelectiondayepoch:
                earlys += 'EARLY CLOSING IGNORE %s\n' % (ivo)
                earlyignorecount += 1
            elif thistime >= self._endelectiondayepoch:
                lates += 'LATE CLOSING IGNORE %s\n' % (ivo)
                lateignorecount += 1
            else:
                closetimes.append(thistime - self._beginelectiondayepoch)

        closetimes = sorted(closetimes)
        local_s += nocloses
        local_s += '\n'
        local_s += earlys
        local_s += '\n'
        local_s += lates
        local_s += '\n'

        considercount = len(globalivos) - nocloseignorecount - earlyignorecount - lateignorecount
        local_s += 'Total ivo count ignored (no close): %3d\n' % (nocloseignorecount)
        local_s += 'Total ivo count ignored (early):    %3d\n' % (earlyignorecount)
        local_s += 'Total ivo count ignored (late):     %3d\n' % (lateignorecount)
        local_s += 'Total ivo count considered: %d\n\n' % (considercount)

        timeblocks = globalcreatetimeblocks(closetimes)
        local_s += '%s' % (globaldisplaytimeblocks(timeblocks, \
                           considercount, 'CLOSING TIME'))
        local_s += '\n'

        return local_s

    ## END OF WRITECLOSINGTIMES
    ##################################################################

    ##################################################################
    ## WRITEFIRSTVOTETIMES: write the first vote times histogram counts
    def writefirstvotetimes(self, filenameprefix, county):
        """ This is the docstring.
        """
        local_s = ''

        novotesignorecount = 0
        earlyignorecount = 0
        lateignorecount = 0
        novotess = ''
        earlys = ''
        lates = ''
        firstvotetimes = []
        for ivonumber, ivo in sorted(globalivos.items()):
            ivofirstvote = ivo.getfirstvote()
            if (DUMMYDATE == ivofirstvote[0]) or (DUMMYDATE == ivofirstvote[1]):
                novotess += 'NO VOTES IGNORE %s\n' % (ivo)
                novotesignorecount += 1
                continue
            thistime = globalconverttimetoepoch(ivofirstvote[0], ivofirstvote[1])
            if thistime <= self._beginelectiondayepoch:
                earlys += 'EARLY FIRST VOTE IGNORE %s\n' % (ivo)
                earlyignorecount += 1
            elif thistime >= self._endelectiondayepoch:
                lates += 'LATE FIRST VOTE IGNORE %s\n' % (ivo)
                lateignorecount += 1
            else:
                firstvotetimes.append(thistime - self._beginelectiondayepoch)

        firstvotetimes = sorted(firstvotetimes)
        local_s += novotess
        local_s += '\n'
        local_s += earlys
        local_s += '\n'
        local_s += lates
        local_s += '\n'

        considercount = len(globalivos) - earlyignorecount - lateignorecount - novotesignorecount
        local_s += 'Total ivo count ignored (no votes): %3d\n' % (novotesignorecount)
        local_s += 'Total ivo count ignored (early):    %3d\n' % (earlyignorecount)
        local_s += 'Total ivo count ignored (late):     %3d\n' % (lateignorecount)
        local_s += 'Total ivo count considered: %d\n\n' % (considercount)

        timeblocks = globalcreatetimeblocks(firstvotetimes)
        local_s += '%s' % (globaldisplaytimeblocks(timeblocks, \
                           considercount, 'FIRST VOTE TIME'))
        local_s += '\n'

        return local_s

    ## END OF WRITEFIRSTVOTETIMES
    ##################################################################

    ##################################################################
    ## WRITELASTVOTETIMES: write the last vote times histogram counts
    def writelastvotetimes(self, filenameprefix, county):
        """ This is the docstring.
        """
        local_s = ''

        novotesignorecount = 0
        earlyignorecount = 0
        lateignorecount = 0
        novotess = ''
        earlys = ''
        lates = ''
        lastvotetimes = []
        for ivonumber, ivo in sorted(globalivos.items()):
            ivolastvote = ivo.getlastvote()
            if (DUMMYDATE == ivolastvote[0]) or (DUMMYDATE == ivolastvote[1]):
                novotess += 'NO VOTES IGNORE %s\n' % (ivo)
                novotesignorecount += 1
                continue
            thistime = globalconverttimetoepoch(ivolastvote[0], ivolastvote[1])
            if thistime <= self._beginelectiondayepoch:
                earlys += 'EARLY LAST VOTE IGNORE %s\n' % (ivo)
                earlyignorecount += 1
            elif thistime >= self._endelectiondayepoch:
                lates += 'LATE LAST VOTE IGNORE %s\n' % (ivo)
                lateignorecount += 1
            else:
                lastvotetimes.append(thistime - self._beginelectiondayepoch)

        lastvotetimes = sorted(lastvotetimes)
        local_s += novotess
        local_s += '\n'
        local_s += earlys
        local_s += '\n'
        local_s += lates
        local_s += '\n'

        considercount = len(globalivos) - earlyignorecount - \
                            lateignorecount - novotesignorecount
        local_s += 'Total ivo count ignored (no votes): %3d\n' % \
                                                    (novotesignorecount)
        local_s += 'Total ivo count ignored (early):    %3d\n' % \
                                                    (earlyignorecount)
        local_s += 'Total ivo count ignored (late):     %3d\n' % \
                                                    (lateignorecount)
        local_s += 'Total ivo count considered: %d\n\n' % (considercount)

        timeblocks = globalcreatetimeblocks(lastvotetimes)
        local_s += '%s' % (globaldisplaytimeblocks(timeblocks, \
                           considercount, 'LAST VOTE TIME'))
        local_s += '\n'

        return local_s

    ## END OF WRITELASTVOTETIMES
    ##################################################################

    ##################################################################
    ## WRITEOPENINGTIMES: write the opening times histogram counts
    def writeopeningtimes(self, filenameprefix, county):
        """ This is the docstring.
        """
        local_s = ''

        noopenignorecount = 0
        earlyignorecount = 0
        lateignorecount = 0
        earlys = ''
        lates = ''
        noopens = ''
        opentimes = []
        for ivonumber, ivo in sorted(globalivos.items()):
            ivoopeningtime = ivo.getdatetimeopening()
            if ivoopeningtime[0] == DUMMYDATE:
                noopens += 'NO OPENING IGNORE %s\n' % (ivo)
                noopenignorecount += 1
                continue
            thistime = globalconverttimetoepoch(ivoopeningtime[0], ivoopeningtime[1])
            if thistime <= self._beginelectiondayepoch:
                earlys += 'EARLY OPENING IGNORE %s\n' % (ivo)
                earlyignorecount += 1
            elif thistime >= self._endelectiondayepoch:
                lates += 'LATE OPENING IGNORE %s\n' % (ivo)
                lateignorecount += 1
            else:
                opentimes.append(thistime - self._beginelectiondayepoch)

        opentimes = sorted(opentimes)
        local_s += noopens
        local_s += '\n'
        local_s += earlys
        local_s += '\n'
        local_s += lates
        local_s += '\n'

        considercount = len(globalivos) - noopenignorecount - earlyignorecount - lateignorecount
        local_s += 'Total ivo count ignored (noopen): %3d\n' % (noopenignorecount)
        local_s += 'Total ivo count ignored (early): %3d\n' % (earlyignorecount)
        local_s += 'Total ivo count ignored (late):  %3d\n' % (lateignorecount)
        local_s += 'Total ivo count considered: %d\n\n' % (considercount)

        timeblocks = globalcreatetimeblocks(opentimes)
        local_s += '%s' % (globaldisplaytimeblocks(timeblocks, \
                           considercount, 'OPENING TIME'))
        local_s += '\n'

#        num_bins = 13
#        thetitle = 'Ivo opening times -- %s' % (county)
#        n, bins, patches = plt.hist(opentimes, num_bins, normed=0, facecolor='green', alpha=0.5)
#        plt.xlabel('Opening Times')
#        plt.ylabel('Ivos Open')
#        plt.title(thetitle)
#        plt.subplots_adjust(left=0.15)
#        plt.show()

        return local_s

    ## END OF WRITEOPENINGTIMES
    ##################################################################

    ##################################################################
    ## WRITEWORKING: write the counts of working ivos over time
    def writeworking(self, filenameprefix, county):
        """ This is the docstring.
        """
        local_s = ''

        timeblocks = globalcreatetimeblocks([])
#        print 'ZORK', sorted(timeblocks)

        for ivonumber, ivo in sorted(globalivos.items()):
            ivotimeblocks = ivo.getvotetimeblocks()
            for time, count in sorted(ivotimeblocks.items()):
#                if time == '24:00':
#                    print 'ZORK', time, count
                if count > 0:
                    timeblocks[time] += 1
#                    print 'ZZZZ', time, count, timeblocks[time]

        label = 'WORKING '
        for block, count in sorted(timeblocks.items()):
            local_s += '%s %s : %6d\n' % (label, block, count)
        local_s += '\n'

        return local_s

    ## END OF WRITEWORKING
    ##################################################################

    ##################################################################
    ## writefirstlastworking: write the firstlastworking file
    def writefirstlastworking(self, filenameprefix, county, configuration):
        """ This is the docstring.
        """
        stars = '********** ********** ********** ********** ********** **********'

#        self._electiondate = configuration.getdate()

        # base begin time is midnight plus one second on election day
        # base end time is 2am the day after election day
        self._beginelectiondayepoch = configuration.getbeginelectiondayepoch()
        self._endelectiondayepoch = configuration.getendelectiondayepoch()

        outfile = open(filenameprefix+'FirstLastWorking.txt', 'w')
        outfile.write('FirstLastWorking data for %s\n\n' % (county))
        outfile.write('%s\n\n' % (stars))

        outfile.write('%s' % (self.writeopeningtimes(filenameprefix, county)))
        outfile.write('%s\n\n' % (stars))

        outfile.write('%s' % (self.writeclosingtimes(filenameprefix, county)))
        outfile.write('%s\n\n' % (stars))

        outfile.write('%s' % (self.writefirstvotetimes(filenameprefix, county)))
        outfile.write('%s\n\n' % (stars))

        outfile.write('%s' % (self.writelastvotetimes(filenameprefix, county)))
        outfile.write('%s\n\n' % (stars))

        outfile.write('%s' % (self.writeworking(filenameprefix, county)))
        outfile.write('%s\n\n' % (stars))

    ## END OF WRITEFIRSTLASTWORKING
    ##################################################################
##
## END OF FIRSTLASTWORKING
######################################################################
