""" This is the docstring.
"""
#import sys
from collections import defaultdict

#from globalstuff import *
from globalstuff import DUMMYCLOSETIME
from globalstuff import DUMMYDATE
from globalstuff import DUMMYIVO
from globalstuff import DUMMYOPENTIME
from globalstuff import DUMMYPEB
from globalstuff import DUMMYTIME
from globalstuff import globalconverttimetoepoch
from globalstuff import globalcreatetimeblocks
from globalstuff import globalpebs
from globalstuff import globaltostringvotecount

from onepeb import OnePEB

######################################################################
## CLASS FOR ONE IVO
##
class OneIvo:
    """ This is the docstring.
    """

    # BOOLEANS
    # note that an ivo can be both absentee and not if used, e.g.,
    # for early voting and at hq on election day
    _absentee = False # set from 155 file
    _foundin152 = False # set from 152 file
    _foundin155 = False # set from 155 file
    _foundin68a = False # set from 68A file
    _notabsentee = False # set from 155 file
    _timeresetonelectionday = False # set from 152 file

    # INTEGERS
    _votescast152 = 0 # set from 152
    _votescast155 = 0 # set from 155
    _votescastlate152 = 0 # set from 152

    # STRINGS
    _createdfrom = 'zork' # says where the creation took place
    _ivonumber = DUMMYIVO # set at creation
    _pebnumberclosing = DUMMYPEB # set from 152
    _pebnumberopening = DUMMYPEB # set from 152

    # LISTS
#    _activeintervals = [] # computed from 152 events
    _datetimeclosing = [DUMMYDATE, DUMMYCLOSETIME] # set from 152
    _datetimeopening = [DUMMYDATE, DUMMYOPENTIME] # set from 152
    _firstvote = [DUMMYDATE, DUMMYTIME] # set from 152
    _lastvote = [DUMMYDATE, DUMMYTIME] # set from 152
#    _eventcalibrate = [] # computed from 152 events
#    _eventDIE = [] # computed from 152 events
#    _eventIPS = [] # computed from 152 events
#    _eventmemorycard = [] # computed from 152 events
    _events = [] # computed from 152 events
#    _eventsettimeanddate = [] # computed from 152 events
    _memorycollectiontime = [] # computed from 68A
    _votetimes = [] # set from 152

    # CONTAINERS
#    _anomalies = defaultdict(str) # set from ???
    _ballotstyles = set() # set from 155
    _eventcounts = defaultdict(int) # set from 152
    _pctnumbers = set() # set from 155
    _votetimeblocks = defaultdict(int)
    _votescast155bypct = defaultdict(int) # set from 155

    ##################################################################
    ## BOILERPLATE FUNCTIONS
    def __init__(self, ivonumber, createdfrom):
        """ This is the docstring.
        """
        self._absentee = False
        self._notabsentee = False
        self._foundin152 = False
        self._foundin155 = False
        self._timeresetonelectionday = False

        self._votescast152 = 0
        self._votescast155 = 0
        self._votescastlate152 = 0

        self._createdfrom = createdfrom
        self._firstvote = [DUMMYDATE, DUMMYTIME]
        self._ivonumber = ivonumber
        self._lastvote = [DUMMYDATE, DUMMYTIME]
        self._pebnumberclosing = DUMMYPEB
        self._pebnumberopening = DUMMYPEB

        self._activeintervals = [] # computed from 152 events
        self._datetimeclosing = [DUMMYDATE, DUMMYCLOSETIME] # set from 152
        self._datetimeopening = [DUMMYDATE, DUMMYOPENTIME] # set from 152
        self._eventcalibrate = [] # computed from 152 events
        self._eventDIE = [] # computed from 152 events
        self._eventIPS = [] # computed from 152 events
        self._eventmemorycard = [] # computed from 152 events
        self._events = [] # computed from 152 events
        self._eventsettimeanddate = [] # computed from 152 events
        self._memorycollectiontime = [] # computed from 68A
        self._votetimes = []

        self._anomalies = defaultdict(str) # set from ???
        self._ballotstyles = set() # set from 155
        self._eventcounts = defaultdict(int) # set from 152
        self._pctnumbers = set() # set from 155
        self._votescast155bypct = defaultdict(int) # set from 155

        # to keep pylint happy
        self._configdate = ''
        self._configopening = ''

    def __str__(self):
        """ This is the docstring.
        """
        slist = self.buildstrings()
        local_s = ''
        for slistsub in range(0, len(slist)):
            local_s += slist[slistsub]
            if slistsub != len(slist)-1:
                local_s += '\n'
        return local_s

    def buildstrings(self):
        """ This is the docstring.
        """
        slist = []
        if 0 == len(self._pctnumbers):
            slist.append(self.buildonestring('NNNN'))
        else:
            for pctnumber in sorted(self._pctnumbers):
                slist.append(self.buildonestring(pctnumber))

        return slist

    def headerstring(self):
        """ This is the docstring.
        """
        sss = 'IVO LEGEND:\n'
        sss += '     Created from 152 or 155\n'
        sss += '     Pct number\n'
        sss += '     Found in 152 (Y/N)\n'
        sss += '     Found in 155 (Y/N)\n'
        sss += '     Ivo serial number\n'
        sss += '     PEB used for opening\n'
        sss += '     Opening date/time\n'
        sss += '     Date/time of first vote\n'
        sss += '     PEB used for closing\n'
        sss += '     Closing date/time\n'
        sss += '     Date/time of last vote\n'
        sss += '     Number of vote events 152\n'
        sss += '     Number of vote events 155\n'
        sss += '     Number of vote events 155 by precinct\n'
        sss += '     Number of late vote events 152\n'
        sss += '     Pct numbers\n'
        sss += '     Ballot styles\n'
        sss += '     Memory collection times\n'
        return sss

    def buildonestring(self, pctnumber):
        """ This is the docstring.
        """
        local_s = ''
        local_s += '(%3s)' %  (self._createdfrom)

        if len(self._pctnumbers) > 1:
            local_s += ' M '
        else:
            local_s += '   '
        local_s += ' %s' %  (pctnumber)

        if self._foundin152:
            local_s += ' Y'
        else:
            local_s += ' N'
        if self._foundin155:
            local_s += ' Y '
        else:
            local_s += ' N '

        local_s += ' %7s' %  (self._ivonumber)
        local_s += ' ( %s' % (self._pebnumberopening)
        if self._timeresetonelectionday:
            local_s += ' R '
        else:
            local_s += ' x '
        local_s += '%s %s  %s %s)' % (self._datetimeopening[0], self._datetimeopening[1], \
                              self._firstvote[0], self._firstvote[1])
        local_s += ' ( %s' % (self._pebnumberclosing)
        local_s += ' %s %s  %s %s)' % (self._lastvote[0], self._lastvote[1], \
                               self._datetimeclosing[0], self._datetimeclosing[1])

        local_s += ' %s' %  (globaltostringvotecount(self._votescast152, 7))
        local_s += ' %s' %  (globaltostringvotecount(self._votescast155, 7))
        local_s += ' %s' %  (globaltostringvotecount(self._votescast155bypct[pctnumber], 7))
        local_s += ' %s' %  (globaltostringvotecount(self._votescastlate152, 7))
        local_s += ' ('
        for pctnumber in sorted(self._pctnumbers):
            local_s += ' %s' %  (pctnumber)
        local_s += ') ( '
        for style in sorted(self._ballotstyles):
            local_s += ' %s' %  (style)
        local_s += ')'
        local_s += ' %s' %  (self._memorycollectiontime)

        return local_s

    ##################################################################
    ## ACCESSORS
    def getabsentee(self): return self._absentee
    def getnotabsentee(self): return self._notabsentee
    def getfoundin152(self): return self._foundin152
    def getfoundin155(self): return self._foundin155
    def gettimeresetelectionday(self): return self._timeresetonelectionday

    def getvotescast152(self): return self._votescast152
    def getvotescast155(self): return self._votescast155
    def getvotescast155bypct(self, pctnumber): return self._votescast155bypct[pctnumber]
    def getvotescastlate152(self): return self._votescastlate152

    def getcreatedfrom(self): return self._createdfrom
    def getfirstvote(self): return self._firstvote
    def getivonumber(self): return self._ivonumber
    def getlastvote(self): return self._lastvote
    def getpebnumberclosing(self): return self._pebnumberclosing
    def getpebnumberopening(self): return self._pebnumberopening

    def getactiveintervals(self): return self._activeintervals
    def getdatetimeclosing(self): return self._datetimeclosing
    def getdatetimeopening(self): return self._datetimeopening
    def geteventcalibrate(self): return self._eventcalibrate
    def geteventDIE(self): return self._eventDIE
    def geteventIPS(self): return self._eventIPS
    def geteventmemorycard(self): return self._eventmemorycard
    def getevents(self): return self._events
    def geteventsettimeanddate(self): return self._eventsettimeanddate
    def getmemorycollectiontime(self): return self._memorycollectiontime

    def getabanomalies(self): return self._anomalies
    def getballotstyles(self): return self._ballotstyles
    def geteventcounts(self): return self._eventcounts
    def getpctnumbers(self): return self._pctnumbers
    def getvotetimeblocks(self): return self._votetimeblocks

    ##################################################################
    ## MUTATORS

    ##################################################################
    ## OTHER FUNCTIONS

    ##################################################################
    ## add to the events list for this ivo
    def addtoevents(self, event):
        """ This is the docstring.
        """
        self._events.append(event)

    ##################################################################
    ## add to the memory card collection times for this ivo
    def addtomemorycollectiontime(self, datetime):
        """ This is the docstring.
        """
        self._memorycollectiontime.append(datetime)

    ##################################################################
    ## reformat the date from mm:dd:yyyy to yyyy_mm_dd
    def reformatdate(self, date):
        """ This is the docstring.
        """
#        print('DATE', self.__str__())
        if 'dummy' in date:
            return '1970_01_01'
#        datesplit = date.split('/')
        datesplit = date.split('-')  # Really? This had to be changed?!
#        print('DATE', date, datesplit)

        # dates used to be as follows
#        month = datesplit[0]
#        day = datesplit[1]
#        year = datesplit[2]

        # dates as of 12 June 2018 now done this way
        year = datesplit[0]
        month = datesplit[1]
        day = datesplit[2]

        return year + '_' + month + '_' + day

#    ##################################################################
#    ## reformat the date from mm:dd:yyyy to yyyy_mm_dd
#    def reformatdateKANSAS(self, date):
#        """ This is the docstring.
#        """
#        print('DATE', self.__str__())
#        if 'dummy' in date:
#            return '1970_01_01'
#        datesplit = date.split('/')
##        datesplit = date.split('-')  # Really? This had to be changed?!
##        print('DATE', date, datesplit)
#
#        # dates used to be as follows
##        month = datesplit[0]
##        day = datesplit[1]
##        year = datesplit[2]
#
#        # dates as of 12 June 2018 now done this way
#        year = datesplit[0]
#        month = datesplit[1]
#        day = datesplit[2]
#
#        return year + '_' + month + '_' + day

#    ##################################################################
#    ## tostring the events list
#    def tostringevents(self):
#        """ This is the docstring.
#        """
#        local_s = ''
#        local_s += 'EVENTS FOR IVO %s\n' % (self._ivonumber)
#        for event in self._events:
#            local_s += '%s\n' % (event)
#        return local_s

#    ##################################################################
#    ## tostring the ivos
#    ## this function is here to allow for labels prepending the output line
#    def tostring(self, label):
#        """ This is the docstring.
#        """
#        slist = self.buildstrings()
#        local_s = ''
#        for item in slist:
#            local_s += '%s %s: %s\n' % (label, self._ivonumber, item)
#        return local_s

    ##################################################################
    ## update this ivo from the 155 file
    def updatefrom155(self, newballot, pctnumber, ballotstyle):
        """ This is the docstring.
        """
        self._foundin155 = True
        if '*' == newballot:
            self._votescast155 += 1
            self._votescast155bypct[pctnumber] += 1

        if pctnumber < '0750':
            self._notabsentee = True
        else:
            self._absentee = True

        self._pctnumbers.add(pctnumber)
        self._ballotstyles.add(ballotstyle)

    ##################################################################
    ## update this ivo from the events list from the 152 file
    def updateivofromevents(self, date, configuration):
        """ This is the docstring.
        """
#        print('UPDATE IVO FROM EVENTS', self._ivonumber)
        self._configdate = configuration.getdate()
        self._configopening = configuration.getopeningtime()

        timeblockdata = []
        for event in self._events:

#            print('EVENT', event)
            ivonumber = event.getivonumber()
            pebnumber = event.getpebnumber()
            date152 = event.getdate152()
            reformatteddate152 = self.reformatdate(date152)
#            reformatteddate152 = self.reformatdateKANSAS(date152) # specificllay for Ellis County 
            time152 = event.gettime152()
            code152 = event.getcode152()

            ##########################################################
            ## this ivo is in the 152 file, or else we would not get
            ## to this part of the program
            self._foundin152 = True
            self._eventcounts[code152] += 1

            ##########################################################
            ## update the reset of date and time
            if code152 == '0000117':
                openingtimeepoch = globalconverttimetoepoch(self._configdate, self._configopening)
                thiseventtimeepoch = globalconverttimetoepoch(reformatteddate152, time152)
    #            print('TIMERESET', self._ivonumber, self._configdate,
    #                   self._configopening, reformatteddate152, time152,
    #                   openingtimeepoch, thiseventtimeepoch)
                if thiseventtimeepoch >= openingtimeepoch:
    #                print('YES RESET')
                    self._timeresetonelectionday = True

            ##########################################################
            ## add to or update the PEB dictionary
            ## and record open and close peb
            if pebnumber in globalpebs:
                thispeb = globalpebs[pebnumber]
            else:
                pebtype = event.getpebtype()
                thispeb = OnePEB(pebnumber, pebtype, '155')
            thispeb.setfoundin152(True)

            if '0001672' == code152:
                self._pebnumberopening = pebnumber
                self._datetimeopening = [reformatteddate152, time152]
#                print('USEDFOROPENING %s %s' % (ivonumber, pebnumber))

            if '0001673' == code152:
                thispeb.setusedforclosing(True)
                self._pebnumberclosing = pebnumber
                self._datetimeclosing = [reformatteddate152, time152]
#                print('USEDFORCLOSING %s %s' % (ivonumber, pebnumber))

            thispeb.addtoivoset(ivonumber)

            globalpebs[pebnumber] = thispeb

            ##########################################################
            ## record first and last vote and vote counts
            ## and create the time block data for votes cast
            votecastcodes = ['0001510', '0001511', '0001512', \
                             '0002900', '0002901', '0002902', '0002903', '0002905', \
                             '0002906', '0002908', '0002909', '0002911', '0002912', \
                             '0002915']
            if code152 in votecastcodes:
                self._votescast152 += 1
                self._votetimes.append([reformatteddate152, time152])
                self._lastvote = [reformatteddate152, time152]
                if DUMMYDATE == self._firstvote[0]:
                    self._firstvote = [reformatteddate152, time152]
                ## it would be here that we add to the late vote count

            ##########################################################
            ## create the time block data
            if code152 in votecastcodes:
#                if self._ivonumber == '5125222':
#                    print 'PROCESS VOTE EVENT', reformatteddate152, time152, code152
                votetime = globalconverttimetoepoch(reformatteddate152, time152)
                timeblockdata.append(votetime - configuration.getbeginelectiondayepoch())

#        label = 'VOTE TIME BLOCK %s: ' % (self._ivonumber)
#        print('TIME BLOCK DATA %s: ' % (timeblockdata))
        self._votetimeblocks = globalcreatetimeblocks(timeblockdata)
#        print globaldisplaytimeblocks(self._votetimeblocks, self._votescast152, label)
    ##
    ##################################################################
##
######################################################################
