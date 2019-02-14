""" This is the docstring.
"""
#import sys
from collections import defaultdict

#from globalstuff import *
from globalstuff import DUMMYCLOSETIME
from globalstuff import DUMMYDATE
from globalstuff import DUMMYOPENTIME
#from globalstuff import DUMMYVOTECOUNT
from globalstuff import globalconverttimetoepoch
from globalstuff import globalgettotal152
from globalstuff import globalgettotal155
from globalstuff import globalgetpctsmissingfrom155
from globalstuff import globalgetpctsmissingmemorycarddata
from globalstuff import globalivos
from globalstuff import globalpcts
from globalstuff import globalpebs

######################################################################
## CLASS FOR EXCEPTIONS REPORT
class Exceptions:
    """ This is the docstring.
    """

    ##################################################################
    ## convert a 'set' to a 'str'
    def convertsettostring(self, theset):
        """ This is the docstring.
        """
        local_s = ''
        for item in sorted(theset):
            local_s += ' %s' % (item)
        return local_s

    ##################################################################
    ## get the mem card first collection times by date/frequency
    def getfirstcollectiontimes(self):
        """ This is the docstring.
        """
        collectionfreq = defaultdict(int)
        for ivonumber, ivo in sorted(globalivos.items()):
            colltime = ivo.getmemorycollectiontime()
            if 0 == len(colltime):
                firstcolltime = 'NULL NULL'
            else:
                firstcolltime = colltime[0]
            firstcolldate = firstcolltime.split()[0]
            collectionfreq[firstcolldate] += 1

        local_s = ''
        for time, count in sorted(collectionfreq.items()):
            local_s += '%7d %10s\n' % (count, time)
        return local_s

    ##################################################################
    ## get the ivos with early closing times
    def getivosearlyclose(self, date, earlytime):
        """ This is the docstring.
        """
        earlylist = []
#        print 'epoch conversion', date, earlytime
        earlytimeepoch = globalconverttimetoepoch(date, earlytime)

        for ivonumber, ivo in sorted(globalivos.items()):
            datetime = ivo.getdatetimeclosing()
            pctnumbersset = ivo.getpctnumbers()
            pctnumberslist = [] # convert set to list for sorting
            for pctnumber in pctnumbersset:
                pctnumberslist.append(pctnumber)

            pctnumberslist = sorted(pctnumberslist)
            if 0 == len(pctnumberslist):
                pctnumberslist.append('NNNN')

            earlykey = pctnumberslist[0]
            if datetime[0] == DUMMYDATE:
                continue
            if ('NNNN' != earlykey) and (earlykey >= '0750'): continue
            thistimeepoch = globalconverttimetoepoch(datetime[0], datetime[1])
#            if (datetime[0] != date) or (datetime[1] < earlytime):
            if thistimeepoch < earlytimeepoch:
                earlylist.append([earlykey, 'EARLY CLOSETIME %s\n' % (ivo)])

        count = 0
        local_s = ''
        local_s += 'Ivos with early closing time\n'
        for key, value in sorted(earlylist):
            local_s += value
            count += 1
        local_s += 'Number of such ivos: %d\n\n' % (count)

        return local_s

    ##################################################################
    ## get the ivos with early open times
    def getivosearlyopen(self, date, earlytime):
        """ This is the docstring.
        """
        earlylist = []
        earlytimeepoch = globalconverttimetoepoch(date, earlytime)

        for ivonumber, ivo in sorted(globalivos.items()):
            datetime = ivo.getdatetimeopening()
            pctnumbersset = ivo.getpctnumbers()
            pctnumberslist = [] # convert set to list for sorting
            for pctnumber in sorted(pctnumbersset):
                pctnumberslist.append(pctnumber)

            pctnumberslist = sorted(pctnumberslist)
            if 0 == len(pctnumberslist):
                pctnumberslist.append('NNNN')

            earlykey = pctnumberslist[0]
            if datetime[0] == DUMMYDATE:
                continue
            if ('NNNN' != earlykey) and (earlykey >= '0750'):
                continue
            thistimeepoch = globalconverttimetoepoch(datetime[0], datetime[1])
#            if (datetime[0] != date) or (datetime[1] < earlytime):
            if thistimeepoch < earlytimeepoch:
                earlylist.append([earlykey, 'EARLY OPENTIME %s\n' % (ivo)])

        count = 0
        local_s = ''
        local_s += 'Ivos with early opening time\n'
        for key, value in sorted(earlylist):
            local_s += value
            count += 1
        local_s += 'Number of such ivos: %d\n\n' % (count)

        return local_s

    ##################################################################
    ## get the ivos with late closing times
    def getivoslateclose(self, date, latevotetime):
        """ This is the docstring.
        """
        latelist = []
        latetimeepoch = globalconverttimetoepoch(date, latevotetime)

        for ivonumber, ivo in sorted(globalivos.items()):
            datetime = ivo.getdatetimeclosing()
            pctnumbersset = sorted(ivo.getpctnumbers())
            pctnumberslist = [] # convert set to list for sorting
            for pctnumber in sorted(pctnumbersset):
                pctnumberslist.append(pctnumber)

            pctnumberslist = sorted(pctnumberslist)
            if 0 == len(pctnumberslist):
                pctnumberslist.append('NNNN')

            latekey = pctnumberslist[0]
            if datetime[0] == DUMMYDATE:
                continue
            if ('NNNN' != latekey) and (latekey >= '0750'):
                continue
            thistimeepoch = globalconverttimetoepoch(datetime[0], datetime[1])
#            if (datetime[0] != date) or (datetime[1] > latevotetime):
            if thistimeepoch > latetimeepoch:
                latelist.append([latekey, \
                                  'LATE CLOSETIME %s\n' % (ivo)])

        count = 0
        local_s = ''
        local_s += 'Ivos with late closing time\n'
        for key, value in sorted(latelist):
            local_s += value
            count += 1
        local_s += 'Number of such ivos: %d\n\n' % (count)

        return local_s

    ##################################################################
    ## get the ivos with late open times
    def getivoslateopen(self, date, openingtime):
        """ This is the docstring.
        """
        latelist = []
        openingtimeepoch = globalconverttimetoepoch(date, openingtime)

        for ivonumber, ivo in sorted(globalivos.items()):
            datetime = ivo.getdatetimeopening()
            pctnumbersset = sorted(ivo.getpctnumbers())
            pctnumberslist = [] # convert set to list for sorting
            for pctnumber in sorted(pctnumbersset):
                pctnumberslist.append(pctnumber)

            pctnumberslist = sorted(pctnumberslist)
            if 0 == len(pctnumberslist):
                pctnumberslist.append('NNNN')

            latekey = pctnumberslist[0]
            if datetime[0] == DUMMYDATE:
                continue
            if ('NNNN' != latekey) and (latekey >= '0750'):
                continue
            thistimeepoch = globalconverttimetoepoch(datetime[0], datetime[1])
#            if (datetime[0] != date) or (datetime[1] > openingtime):
            if thistimeepoch > openingtimeepoch:
                latelist.append([latekey, \
                                  'LATE OPENTIME %s\n' % (ivo)])

        count = 0
        local_s = ''
        local_s += 'Ivos with late opening time\n'
        for key, value in sorted(latelist):
            local_s += value
            count += 1
        local_s += 'Number of such ivos: %d\n\n' % (count)

        return local_s

    ##################################################################
    ## get the ivos with no open or close times
    def getivosnoopenclose(self):
        """ This is the docstring.
        """
        notimelist = []

        for ivonumber, ivo in sorted(globalivos.items()):
            datetime = ivo.getdatetimeopening()
            if (datetime[0] == DUMMYDATE) or (datetime[1] == DUMMYOPENTIME):

                notimelist.append('NO OPENTIME %s' % (ivo))
        local_s = ''
        local_s += 'Ivos with no opening time\n'
        for item in notimelist:
            local_s += item
        local_s += 'Number of such ivos: %d\n\n' % (len(notimelist))

        notimelist = []
        for ivonumber, ivo in sorted(globalivos.items()):
            datetime = ivo.getdatetimeclosing()
            if (datetime[0] == DUMMYDATE) or (datetime[1] == DUMMYCLOSETIME):
                notimelist.append('NO CLOSETIME %s' % (ivo))

        local_s = ''
        local_s += 'Ivos with no closing time\n'
        for item in notimelist:
            local_s += item
        local_s += 'Number of such ivos: %d\n\n' % (len(notimelist))

        return local_s

    ##################################################################
    ## get the ivos not in the 68a
    def getivosnotin68a(self):
        """ This is the docstring.
        """
        local_s = ''
        count = 0
        for ivonumber, ivo in sorted(globalivos.items()):
            if 0 == len(ivo.getmemorycollectiontime()):
                local_s += '%s\n' % (ivo)
        local_s += 'Number of such ivos: %d\n' % (count)

        return local_s

    ##################################################################
    ## get the pcts with multiple pebs used for closing
    def getmultiplepebs(self):
        """ This is the docstring.
        """
        local_s = ''

        count = 0
        for pctnumber, pct in sorted(globalpcts.items()):
            closingpebs = pct.getclosingpebs()
            if len(closingpebs) > 1:
                count += 1
                openingpebs = sorted(pct.getopeningpebs())
                ivos = sorted(pct.getivos())
                local_s += '%s %s\n' % (pctnumber, pct.getpctname())
                local_s += '     (%s)\n' % (self.convertsettostring(ivos))
                local_s += '     (%s) (%s)\n' % \
                                      (self.convertsettostring(openingpebs), \
                                      self.convertsettostring(closingpebs))
        local_s += 'Number of such pcts: %d\n' % (count)

        return local_s

    ##################################################################
    ## get the ivos opened and closed with different PEBs
    def getopencloseexceptions(self):
        """ This is the docstring.
        """
        local_s = ''

        count = 0
        for ivonumber, ivo in sorted(globalivos.items()):
            openingpeb = ivo.getpebnumberopening()
            closingpeb = ivo.getpebnumberclosing()
            if openingpeb != closingpeb:
                pctnumbers = ivo.getpctnumbers()
                count += 1
                local_s += 'Opening PEB %s not closing PEB %s (%s)\n' % \
                            (openingpeb, closingpeb, \
                            self.convertsettostring(pctnumbers))
        local_s += 'Number of such ivos: %d\n' % (count)

        return local_s

#    ##################################################################
#    ## get the pcts missing from the 155
#    def getpctsmissingfrom155(self):
#        """ This is the docstring.
#        """
#        local_s = ''
#
#        count = 0
#        for pctnumber, pct in sorted(globalpcts.items()):
#            if pctnumber >= '0750':
#                continue
#            votes155 = pct.getvotescast155thispct()
#            if DUMMYVOTECOUNT == pct.getvotescast155():
#                local_s += 'PCT MISSING %s %s xxxxx vote(s)\n' % \
#                            (pctnumber, pct.getpctname())
#                count += 1
#        local_s += 'Number of such pcts: %d\n' % (count)
#
#        return local_s
#
#    ##################################################################
#    ## get the pcts missing memory card data
#    def getpctsmissingmemorycarddata(self):
#        """ This is the docstring.
#        """
#        local_s = ''
#
#        count = 0
#        for pctnumber, pct in sorted(globalpcts.items()):
#            if pctnumber >= '0750':
#                continue
#            votes30aivo = pct.getvotescast30aivo()
#            votes155thispct = pct.getvotescast155thispct()
#            if DUMMYVOTECOUNT == votes155thispct:
#                votes155thispct = 0
#            if votes30aivo != votes155thispct:
#                local_s += 'DATA MISSING: %s %-30s: 155 file is missing %6d vote(s)\n' % \
#                            (pctnumber, pct.getpctname(), \
#                             votes30aivo-votes155thispct)
#                count += 1
#        local_s += 'Number of such pcts: %d\n' % (count)
#
#        return local_s
#
    ##################################################################
    ## get the pebs only in 68a or 152
    def getpebexceptions(self):
        """ This is the docstring.
        """
        local_s = ''

        local_s += 'PEBs found only in 68A and not in 152\n'
        count = 0
        for pebnumber, peb in sorted(globalpebs.items()):
            if (peb.getfoundin68a()) and (not peb.getfoundin152()):
                local_s += '%s\n' % (pebnumber)
                count += 1
        local_s += 'Number of such pebs: %d\n' % (count)

        local_s += '\n'
        local_s += 'PEBs closing in 152 but not present in 68A\n'
        count = 0
        for pebnumber, peb in sorted(globalpebs.items()):
            if (not peb.getfoundin68a()) and (peb.getusedforclosing()):
                local_s += '%s\n' % (peb)
                count += 1
        local_s += 'Number of such pebs: %d\n' % (count)

        return local_s

    ##################################################################
    ## get the ivos only in 152 or 155
    def getivoexceptions(self):
        """ This is the docstring.
        """
        local_s = ''

        local_s += 'Ivos found only in 152 and not in 155\n'
        count = 0
        for ivonumber, ivo in sorted(globalivos.items()):
            if (ivo.getfoundin152()) and (not ivo.getfoundin155()):
                local_s += '%s: %s\n' % (ivonumber, ivo)
                count += 1
        local_s += 'Number of such ivos: %d\n' % (count)

        local_s += '\n'
        local_s += 'Ivos found only in 155 and not in 152\n'
        count = 0
        for ivonumber, ivo in sorted(globalivos.items()):
            if (not ivo.getfoundin152()) and (ivo.getfoundin155()):
                local_s += '%s: %s\n' % (ivonumber, ivo)
                count += 1
        local_s += 'Number of such ivos: %d\n' % (count)

        return local_s

    ##################################################################
    ## writeexceptions: write the exceptions file
    def writeexceptions(self, filenameprefix, county, configuration):
        """ This is the docstring.
        """
        divider = '########## ########## ########## ########## ########## ##########'
        outfile = open(filenameprefix+'EXCEPTIONS.txt', 'w')
        outfile.write('%s\n' % (divider))
        outfile.write('%s\n\n' % (divider))
        outfile.write('EXCEPTIONS report for %s\n\n' % (county))
        outfile.write('Ballot total in 152 %10d\n' % (globalgettotal152()))
        outfile.write('Ballot total in 155 %10d\n' % (globalgettotal155()))
        ##
        outfile.write('\n%s\n\n' % (divider))
        outfile.write('Listing ivos only in 152 or in 155 (includes 750+)\n\n')
        outfile.write('%s\n' % (self.getivoexceptions()))
        ##
        outfile.write('\n%s\n\n' % (divider))
        outfile.write('Listing ivos opened and closed with different PEBs (includes 750+)\n')
        outfile.write('This listing comes from the 152 file\n\n')
        outfile.write('%s\n' % (self.getopencloseexceptions()))
        ##
        outfile.write('\n%s\n\n' % (divider))
        outfile.write('Listing precincts with multiple PEBs for closing (includes 750+)\n\n')
        outfile.write('%s\n' % (self.getmultiplepebs()))
        ##
        outfile.write('\n%s\n\n' % (divider))
        outfile.write('Listing PEBs only in 68A or 152 (includes 750+)\n\n')
        outfile.write('%s\n' % (self.getpebexceptions()))
        outfile.write('\n%s\n\n' % (divider))
        ##
        electionday = configuration.getdate()
        openingtime = configuration.getopeningtime()
        closingtime = configuration.getclosingtime()
        earlytime = configuration.getearlytime()
        latevotetime = configuration.getlatetime()
        outfile.write('\n%s\n\n' % (divider))
        outfile.write('Listing ivos with anomalous opening/closing times\n')
        outfile.write('Early time means before %s %s\n' % (electionday, earlytime))
        outfile.write('Late time means after   %s %s\n\n' % (electionday, latevotetime))
        ##
        outfile.write('Listing ivos with no opening/closing times (includes 750+)\n')
        outfile.write('All ivos not in the 152 will appear here\n\n')
        outfile.write('%s\n' % (self.getivosnoopenclose()))
        ##
        outfile.write('Listing ivos with early opening times (EXCLUDES 750+)\n\n')
        outfile.write('%s\n' % (self.getivosearlyopen(electionday, earlytime)))
        ##
        outfile.write('Listing ivos with late opening times (EXCLUDES 750+)\n\n')
        outfile.write('%s\n' % (self.getivoslateopen(electionday, openingtime)))
        ##
        outfile.write('Listing ivos with early closing times (EXCLUDES 750+)\n\n')
        outfile.write('%s\n' % (self.getivosearlyclose(electionday, closingtime)))
        ##
        outfile.write('Listing ivos with late closing times (EXCLUDES 750+)\n\n')
        outfile.write('%s\n' % (self.getivoslateclose(electionday, latevotetime)))
        outfile.write('\n%s\n\n' % (divider))
        ##
        outfile.write('Listing ivos whose mem card data was not collected (includes 750+)\n')
        outfile.write('This list is of all known ivos not in the 68A\n\n')
        outfile.write('%s\n' % (self.getivosnotin68a()))
        outfile.write('\n%s\n\n' % (divider))
        ##
        outfile.write('Dates of 68A first collection of mem card data (includes 750+)\n')
        outfile.write('%s\n' % (self.getfirstcollectiontimes()))
        outfile.write('\n%s\n\n' % (divider))
        ##
        outfile.write('Listing of pcts with missing mem card data (EXCLUDES 750+)\n')
        outfile.write('%s\n' % (globalgetpctsmissingmemorycarddata()))
        outfile.write('\n%s\n\n' % (divider))
        ##
        outfile.write('Listing of pcts entirely missing from 155 (EXCLUDES 750+)\n')
        outfile.write('%s\n' % (globalgetpctsmissingfrom155()))
        outfile.write('\n%s\n\n' % (divider))
        ##

        outfile.close()
    ## END OF WRITEEXCEPTIONS
    ##################################################################
##
## END OF EXCEPTIONS
######################################################################
