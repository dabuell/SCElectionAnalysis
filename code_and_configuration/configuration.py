""" This is the docstring.
"""
#import sys
from globalstuff import globalconverttimetoepoch

######################################################################
## CLASS FOR THE CONFIGURATION
class Configuration:
    """ This is the docstring.
    """
    ##################################################################
    ## initialization
    def __init__(self, configfilename):
        """ This is the docstring.
        """
        print("READ FROM '%s'" % (configfilename))
        filetoread = open(configfilename)
        self._lines = filetoread.readlines()
        if len(self._lines) < 6:
            print('ERROR: not enough configuration information')
            print('need date, open, close, late, and counties')
            exit(0)
        self._counties = []
        # here and below we trim away the newline
        self._datapath = self._lines[0].replace('\n', '')
        self._date = self._lines[1].replace('\n', '')
        self._openingtime = self._lines[2].replace('\n', '')
        self._closingtime = self._lines[3].replace('\n', '')
        self._earlytime = self._lines[4].replace('\n', '')
        self._latetime = self._lines[5].replace('\n', '')

        self._beginelectiondayepoch = globalconverttimetoepoch(self._date, '00:00:00')
        self._endelectiondayepoch = self._beginelectiondayepoch + 93600 # 2 am the next day

        for countysub in range(6, len(self._lines)):
            # here and below we trim away the newline
            if len(self._lines[countysub].strip()) == 0:
                break
            self._counties.append(self._lines[countysub].replace('\n', ''))

    ##################################################################
    ## initialization
    def __str__(self):
        local_s = 'CONFIGURATION\n'
        local_s += 'CONFIG:    DATAPATH:      %s\n' % (self._datapath)
        local_s += 'CONFIG:    DATE:          %s\n' % (self._date)
        local_s += 'CONFIG:    POLLS OPEN:    %s    EPOCH TIME: %s\n' % \
                    (self._openingtime, str(self._beginelectiondayepoch))
        local_s += 'CONFIG:    POLLS CLOSE:   %s    EPOCH TIME: %s\n' % \
                    (self._closingtime, str(self._endelectiondayepoch))
        local_s += 'CONFIG:    EARLY TIME IS: %s\n' % (self._earlytime)
        local_s += 'CONFIG:    LATE TIME IS:  %s\n' % (self._latetime)
        for county in self._counties:
            local_s += 'CONFIG:    COUNTY:        %s\n' % (county)
        return local_s

    ##################################################################
    ## get the beginning of the election day measured from the epoch
    def getbeginelectiondayepoch(self):
        """
        Accessor for election day start time measured from the epoch.
        """
        return self._beginelectiondayepoch

    ##################################################################
    ## get the closing time
    def getclosingtime(self):
        """
        Accessor for the closing time.
        """
        return self._closingtime

    ##################################################################
    ## get the list of counties for this computation
    def getcounties(self):
        """
        Accessor for the list of counties for this computation.
        """
        return self._counties

    ##################################################################
    ## get the datapath
    def getdatapath(self):
        """
        Accessor for the datapath.
        """
        return self._datapath

    ##################################################################
    ## get the date
    def getdate(self):
        """
        Accessor for the date.
        """
        return self._date

    ##################################################################
    ## get the time that is considered "early"
    def getearlytime(self):
        """
        Accessor for the time considered "early".
        """
        return self._earlytime

    ##################################################################
    ## get the election day ending time measured from the epoch
    def getendelectiondayepoch(self):
        """
        Accessor for election day end time measured from the epoch.
        """
        return self._endelectiondayepoch

#    ##################################################################
#    ## get the poll opening hour
#    def getopeninghour(self):
#        """
#        Accessor for the poll opening hour.
#        """
#        return self._openingtime.split(':')[0]

    ##################################################################
    ## get the time that is considered "late"
    def getlatetime(self):
        """
        Accessor for the time that is considered "late".
        """
        return self._latetime

    ##################################################################
    ##
    def getopeningtime(self):
        """
        Accessor for the opening time.
        """
        return self._openingtime

    ##################################################################
    ##
    def getyearfromdate(self):
        """
        Accessor for the year part of a date.
        """
        return self._date[0:4]
