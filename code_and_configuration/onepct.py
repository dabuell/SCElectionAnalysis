""" This is the docstring.
"""
#import sys
#from collections import defaultdict

#from globalstuff import *
from globalstuff import DUMMYVOTECOUNT
from globalstuff import globalivos
from globalstuff import globaltostringvotecount

from oneivo import OneIvo

######################################################################
## CLASS FOR ONE PRECINCT
##
class OnePct:
    """ This is the docstring.
    """

    _registeredvoters = DUMMYVOTECOUNT # set from 30A file
    _votescast30atotal = DUMMYVOTECOUNT # set from 30A file
    _votescast30optical = DUMMYVOTECOUNT # set from 30A file
    _votescast30ivo = DUMMYVOTECOUNT # set from 30A file
    _votescast30flash = DUMMYVOTECOUNT # set from 30A file
    _votescast152 = DUMMYVOTECOUNT # set from 155 file
    _votescast155thispct = DUMMYVOTECOUNT # set from 155 file

    _createdfrom = 'zork' # says where the creation took place
    _pctname = 'PCTNAME' # should be set from 155 file, but maybe 30A?
    _pctnumber = 'NNNN' # should be set from 155 file, but maybe 30A?
    _turnout = 'turnout' # set from 30A file

    _ballotstyle = set()
    _ivos = set() # set from 155

    ##################################################################
    ## BOILERPLATE FUNCTIONS
    def __init__(self, pctnumber, pctname, createdfrom):
        """ This is the docstring.
        """
        self._registeredvoters = DUMMYVOTECOUNT

        # old code
#        self._votescast30atotal = DUMMYVOTECOUNT
#        self._votescast30aoptical = DUMMYVOTECOUNT
#        self._votescast30aivo = DUMMYVOTECOUNT
#        self._votescast30aflash = DUMMYVOTECOUNT

        # new code for 12 June 2018
        self._votescast30total = DUMMYVOTECOUNT
        self._votescast30ds850 = DUMMYVOTECOUNT
        self._votescast30m650 = DUMMYVOTECOUNT
        self._votescast30ds200 = DUMMYVOTECOUNT
        self._votescast30m100 = DUMMYVOTECOUNT
        self._votescast30ivo = DUMMYVOTECOUNT
        self._votescast30flash = DUMMYVOTECOUNT

        self._votescast152 = DUMMYVOTECOUNT
        self._votescast155 = DUMMYVOTECOUNT
        self._votescast155thispct = DUMMYVOTECOUNT

        self._createdfrom = createdfrom
        self._pctname = pctname
        self._pctnumber = pctnumber

        self._ballotstyle = set()
        self._closingpebs = set() # set from combining 152 and 155
        self._ivos = set() # set from 155
        self._openingpebs = set() # set from combining 152 and 155

    def __str__(self):
        """ This is the docstring.
        """
        local_s = ''
        local_s += '(%3s)' %  (self._createdfrom)
        local_s += ' %7s %-30s' %  (self._pctnumber, self._pctname)

        local_s += ' %6d (%s %s %s %s %s %s %s) %s %s' %  (self._registeredvoters, \
                          # old code
#                          globaltostringvotecount(self._votescast30atotal, 5), \
#                          globaltostringvotecount(self._votescast30aoptical, 5), \
#                          globaltostringvotecount(self._votescast30aivo, 5), \
#                          globaltostringvotecount(self._votescast30aflash, 5), \

                          # new code 12 June 2018
                          globaltostringvotecount(self._votescast30total, 5), \
                          globaltostringvotecount(self._votescast30ds850, 5), \
                          globaltostringvotecount(self._votescast30m650, 5), \
                          globaltostringvotecount(self._votescast30ds200, 5), \
                          globaltostringvotecount(self._votescast30m100, 5), \
                          globaltostringvotecount(self._votescast30ivo, 5), \
                          globaltostringvotecount(self._votescast30flash, 5), \
                          globaltostringvotecount(self._votescast155, 5), \
                          globaltostringvotecount(self._votescast155thispct, 5))
#        if self._votescast30aivo != self._votescast155:
        if (self._votescast30ivo < self._votescast155thispct) and (self._pctnumber < '0750'):
            local_s += ' ZORK fewer in 30A than 155'
        if (self._votescast30ivo > self._votescast155thispct) and (self._pctnumber < '0750'):
            local_s += ' ZORK more in 30A than 155'

        local_s += '\n    terminals: ('
        for ivo in sorted(self._ivos):
            local_s += ' %s' % (ivo)
        local_s += ') \n    open/close pebs: ('
        for peb in sorted(self._openingpebs):
            local_s += ' %s' % (peb)
        local_s += ') ('
        for peb in sorted(self._closingpebs):
            local_s += ' %s' % (peb)
        local_s += ')'

        return local_s

    ##################################################################
    ## ACCESSORS
    def getclosingpebs(self): return self._closingpebs
    def getcreatedfrom(self): return self._createdfrom
    def getivos(self): return self._ivos
    def getopeningpebs(self): return self._openingpebs
    def getpctname(self): return self._pctname
    def getvotescast30ivo(self): return self._votescast30ivo
    def getvotescast152(self): return self._votescast152
    def getvotescast155(self): return self._votescast155
    def getvotescast155thispct(self): return self._votescast155thispct

    ##################################################################
    ## MUTATORS

    ##################################################################
    ## OTHER FUNCTIONS

    def addtoclosingpebs(self, pebnumber):
        """ This is the docstring.
        """
        self._closingpebs.add(pebnumber)

    def addtoopeningpebs(self, pebnumber):
        """ This is the docstring.
        """
        self._openingpebs.add(pebnumber)

    def addtovotescast155(self, votecount, votecountthispct):
        """ This is the docstring.
        """
        if self._votescast155 == DUMMYVOTECOUNT:
            self._votescast155 = votecount
            self._votescast155thispct = votecountthispct
        else:
            self._votescast155 += votecount
            self._votescast155thispct += votecountthispct

    def updatefrom30a(self, registeredvoters, ballots, county):
        """ This is the docstring.
        """
        self._registeredvoters = registeredvoters

        # old code
#        if county == 'york':
#            self._votescast30atotal = ballots[0]
#            self._votescast30aoptical = ballots[1]
#            self._votescast30aivo = ballots[3]
#            self._votescast30aflash = ballots[4]
#        else:
#            self._votescast30atotal = ballots[0]
#            self._votescast30aoptical = ballots[1]
#            self._votescast30aivo = ballots[2]
#            if len(ballots) >= 4:
#                self._votescast30aflash = ballots[3]

        # new code from 12 June 2018 primary
        if county.lower() == 'fairfield':
            self._votescast30total = ballots[0]
            self._votescast30ds850 = 0
            self._votescast30m650 = 0
            self._votescast30ds200 = 0
            self._votescast30m100 = ballots[1]
            self._votescast30ivo = ballots[2]
            self._votescast30flash = ballots[3]
#        elif county.lower() == 'marlboro':
#            self._votescast30total = ballots[0]
#            self._votescast30ds850 = 0
#            self._votescast30m650 = 0
#            self._votescast30ds200 = 0
#            self._votescast30m100 = ballots[1]
#            self._votescast30ivo = ballots[2]
#            self._votescast30flash = ballots[3]
        elif county.lower() == 'anderson':
            self._votescast30total = ballots[0]
            self._votescast30ds850 = 0
            self._votescast30m650 = ballots[1]
            self._votescast30ds200 = 0
            self._votescast30m100 = 0
            self._votescast30ivo = ballots[2]
            self._votescast30flash = ballots[3]
        elif county.lower() == 'ellis':
            self._votescast30total = ballots[0]
            self._votescast30ds850 = ballots[1]
            self._votescast30m650 = ballots[2]
            self._votescast30ds200 = ballots[3]
            self._votescast30m100 = ballots[4]
            self._votescast30ivo = ballots[5]
#            self._votescast30flash = ballots[6]
        else:
            self._votescast30total = ballots[0]
            self._votescast30ds850 = ballots[1]
            self._votescast30m650 = ballots[2]
            self._votescast30ds200 = ballots[3]
            self._votescast30m100 = ballots[4]
            self._votescast30ivo = ballots[5]
            self._votescast30flash = ballots[6]

    def updatefrom155(self, ivonumber, ballotstyle):
        """ This is the docstring.
        """
        self._ballotstyle.add(ballotstyle)
        self._ivos.add(ivonumber)
        if ivonumber in globalivos:
            thisivo = globalivos[ivonumber]
        else:
            thisivo = OneIvo(ivonumber, '155')
            globalivos[ivonumber] = thisivo
            print('CREATED IVO 155: ', ivonumber)
#            print('ERROR PCT: ivonumber not found', ivonumber)
#            sys.exit(0)
#        print('PCT UPDATE: ', ivonumber, thisivo.getvotescast155())
#        self._votescast155 += thisivo.getvotescast155()

    ##
    ##################################################################

##
######################################################################
