""" This is the docstring.
"""
#import sys
#from collections import defaultdict

from globalstuff import globalcontestcandidate
from globalstuff import DUMMYVOTECOUNT
from globalstuff import globalpcts
from globalstuff import globalivos
from globalstuff import globalmakekeyforvotes
from globalstuff import globalvotes

from f155functions import getpctnumberandname
from f155functions import skipthisline

from oneivo import OneIvo
from onepct import OnePct

######################################################################
## CLASS FOR THE 155 FILE
class F155:
    """ This is the docstring.
    """
    ######################################################################
    ## BOILERPLATE FUNCTIONS
    def __init__(self):
        """ This is the docstring.
        """
        self._ballotcount = DUMMYVOTECOUNT # included in code

    def __str__(self):
        """ This is the docstring.
        """
        local_s = 'F155: '
        local_s += 'BALLOTCOUNT: %d\n' % (self._ballotcount)
        return local_s
    ## END OF BOILERPLATE FUNCTIONS
    ######################################################################

    ######################################################################
    ## ACCESSORS
    def getballotcount155(self):
        """ This is the docstring.
        """
        return self._ballotcount
    ## END OF ACCESSORS
    ######################################################################

    ######################################################################
    ## READDATA: READ THE DATA FILE AND PROCESS IMMEDIATE ISSUES
    def readdata(self, prefix, date):
        """ This is the docstring.
        """
        self._ballotcount = 0

        pctnumber = 'NNNN' # included in code
        pctname = 'PCTNAME' # included in code
        ballotstyle = ''
        candidate = ''
        ivonumber = ''
        newballot = ''
        sequence = ''
        print('F155: prefix and date', prefix, date)

        # open the file for reading
        filetoread = open(prefix + 'EL155', encoding='ISO-8859-2')

        ##########################################################
        ## run the loop on lines in the 155 file
#        linenumber = 0
        firstline = True
        for line in filetoread:
#            linenumber += 1
#            print('LINE %s' % (line))

            ## we read and trash the first line
            if firstline:
                firstline = False
                continue

            if skipthisline(line):
                continue

            ## pick up the pct from the header line on each page
            ## The following two lines are wrong for South Carolina as of 12 June 2018
#            if 'RUN DATE' in line:
#                pctnumber, pctname = getpctnumberandname(line)
            if 'PRECINCT' in line:
                pctnumber, pctname = getpctnumberandname(line)

            ##########################################################
            ## now we actually read and process the vote lines
            line = line.replace('\n', '')
            ivonumber = line[0:7]
            ballotstyle = line[10:12]
            newballot = line[13:14]
            sequence = line[14:19]
            if len(sequence.strip()) == 0:
                sequence = '00'

            candidate = '_'.join(line[20:54].split())

            contest = '_'.join(line[60:].split())

            ## all south carolina serial numbers start with a '5'
            ## so we skip over any line that does not start with a '5'
            if not ivonumber.startswith('5'):
                continue

#            print 'IVONUMBER', ivonumber
            ## we now have a valid input line from a vote

            if 'W/I' not in candidate:
                globalcontestcandidate.add(contest + ' ' + candidate)

            ## reformat pctnumber to be four characters with leading zeros
            ## then get the pct or else create a new one
            pctnumber = '0000' + pctnumber
            pctnumber = pctnumber[-4:]
            if pctnumber in globalpcts:
                thispct = globalpcts[pctnumber]
            else:
                thispct = OnePct(pctnumber, pctname, '155')
            ## now we have 'thispct'

            ## get the ivo or else create a new one
            if ivonumber in globalivos:
                thisivo = globalivos[ivonumber]
            else:
                thisivo = OneIvo(ivonumber, '155')
            ## now we have 'thisivo'

            if newballot == '*':
                self._ballotcount += 1

            ## update 'foundin155', 'votescast155', absentee-ness
            ## pct numbers, and ballot style numbers
            thisivo.updatefrom155(newballot, pctnumber, ballotstyle)

            ## update ivo numbers and ballot style
            thispct.updatefrom155(ivonumber, ballotstyle)

            key = globalmakekeyforvotes(pctnumber, ivonumber, \
                                        ballotstyle, sequence, \
                                        candidate, contest)
            globalvotes[key] += 1

            ## put back the ivo and pct into the dictionaries
            globalivos[ivonumber] = thisivo
            globalpcts[pctnumber] = thispct

            ## end of reading the vote lines
            ##########################################################

        return

    ## END OF READDATA
    ######################################################################
