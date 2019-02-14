""" This is the docstring.
"""
import sys
from collections import defaultdict

#from globalstuff import *
from globalstuff import globalivos
from globalstuff import globalpcts
from globalstuff import globalpebs
from globalstuff import globaltextforcode
from globalstuff import globalunpackkey
from globalstuff import globalvotes

######################################################################
## CLASS FOR OUTPUT FUNCTIONS
class OutputFunctions:
    """ This is the docstring.
    """

    ##################################################################
    ## writeballotstyles: write the ballotstyles file
    def writeballotstyles(self, filenameprefix, county):
        """ This is the docstring.
        """
        outfile = open(filenameprefix+'BallotStyles.txt', 'w')

        ballotset = set()
        outfile.write('Ballot Styles for %s\n\n' % (county))
        for key, count in sorted(globalvotes.items()):
            pctnumber, ivonumber, bstyle, candidate, contest = \
                                              globalunpackkey(key)
            if 'W/I' in candidate: continue
            setstring = '%3s %s %s %s %s' % \
                         (bstyle, pctnumber, ivonumber, contest, candidate)
            ballotset.add(setstring)

        oldbstyle = ''
        oldpctnumber = ''
        oldivonumber = ''
        for setstring in sorted(ballotset):
            setstringsplit = setstring.split()
            bstyle = setstringsplit[0]
            pctnumber = setstringsplit[1]
            ivonumber = setstringsplit[2]
            contest = setstringsplit[3]
            candidate = setstringsplit[4]

            if bstyle != oldbstyle:
                outfile.write('\n')
            oldbstyle = bstyle

            if pctnumber != oldpctnumber:
                outfile.write('\n')
            oldpctnumber = pctnumber

            if ivonumber != oldivonumber:
                outfile.write('\n')
            oldivonumber = ivonumber

            outfile.write('%3s %s %s %s %s\n' %
                          (bstyle, pctnumber, ivonumber, contest, candidate))

        outfile.close()

    ## END OF WRITEBALLOTSTYLES
    ##################################################################

    ##################################################################
    ## writeeventcounts: write the eventcounts file
    def writeeventcounts(self, filenameprefix, county):
        """ This is the docstring.
        """
        totaleventcount = 0
        if filenameprefix == 'stdout':
            outfile = sys.stdout
        else:
            outfile = open(filenameprefix+'EventCounts.txt', 'w')
        outfile.write('Event logs for %s\n\n' % (county))

        for ivonumber, ivo in sorted(globalivos.items()):
            eventfreq = defaultdict(int)
            totaleventcount += len(ivo.getevents())
            for event in ivo.getevents():
                eventfreq[event.getcode152()] += 1

            for code, freq in sorted(eventfreq.items()):
                outfile.write('%s %3d %s %s\n' % (ivonumber, freq, code, \
                                                  globaltextforcode[code]))
            outfile.write('\n')

        outfile.write('Total number of iVos dumped: %d\n' % (len(globalivos)))
        outfile.write('Total number of events dumped: %d\n' % (totaleventcount))
    ## END OF WRITEEVENTCOUNTS
    ##################################################################

    ##################################################################
    ## writeeventlogs: write the eventlogs file
    def writeeventlogs(self, filenameprefix, county):
        """ This is the docstring.
        """
        totaleventcount = 0
        if filenameprefix == 'stdout':
            outfile = sys.stdout
        else:
            outfile = open(filenameprefix+'EventLogs.txt', 'w')
        outfile.write('Event logs for %s\n\n' % (county))

        for ivonumber, ivo in sorted(globalivos.items()):
            for event in ivo.getevents():
                outfile.write('%s\n' % (event))
            outfile.write('\n')
            totaleventcount += len(ivo.getevents())

        outfile.write('Total number of iVos dumped: %d\n' % (len(globalivos)))
        outfile.write('Total number of events dumped: %d\n' % (totaleventcount))
    ## END OF WRITEEVENTLOGS
    ##################################################################

    ##################################################################
    ## writeeventtexts: write the eventtexts file
    def writeeventtexts(self, filenameprefix, county):
        """ This is the docstring.
        """
        if filenameprefix == 'stdout':
            outfile = sys.stdout
        else:
            outfile = open(filenameprefix+'EventTexts.txt', 'w')
        outfile.write('Event texts for %s\n\n' % (county))

        for code, text in sorted(globaltextforcode.items()):
            outfile.write('%s %s\n' % (code, text))

        outfile.write('Total number of event texts: %d\n' % \
                       (len(globaltextforcode)))
    ## END OF WRITEEVENTTEXTS
    ##################################################################

    ##################################################################
    ## WRITEIVODETAIL: write the ivodetail file
    def writeivodetail(self, filenameprefix, county):
        """ This is the docstring.
        """
        if filenameprefix == 'stdout':
            outfile = sys.stdout
        else:
            outfile = open(filenameprefix+'IvoDetail.txt', 'w')
        outfile.write('iVotronic data for %d iVos in %s\n\n' % (len(globalivos), county))

        firsttime = True
        for ivonumber, ivo in sorted(globalivos.items()):
            if firsttime:
                outfile.write('%s' % (ivo.headerstring()))
                firsttime = False
            outfile.write('%s\n' % (ivo))

        outfile.write('Total number of iVotronics: %d\n\n' % (len(globalivos)))
    ## END OF WRITEIVODETAIL
    ##################################################################

    ##################################################################
    ## WRITEIVOSANDPCTS: write the ivodetail file
    def writeivosandpcts(self, filenameprefix, county):
        """ This is the docstring.
        """
        if filenameprefix == 'stdout':
            outfile = sys.stdout
        else:
            outfile = open(filenameprefix+'IvosAndPcts.txt', 'w')
        outfile.write('Pct Ivo Count for %s\n\n' % (county))

        outfile.write('%4s %7s %8s %8s : %s\n' % \
                     ('PCT', 'IVO', '152', '155', 'RUNNINGTOTAL'))
        for pctnumber, pct in sorted(globalpcts.items()):
            pcttotal155 = 0
            votes30ivo = 0
            for ivonumber in sorted(pct.getivos()):
                ivo = globalivos[ivonumber]
                votes30ivo = pct.getvotescast30ivo()
#                votes30ivo = ivo.getvotescast30ivo()
                votes152 = ivo.getvotescast152()
                votes155 = ivo.getvotescast155()
                votes155thispct = ivo.getvotescast155bypct(pctnumber)
                outfile.write('%4s %s' % (pctnumber, ivonumber))
                outfile.write(' %8d' % (votes152))
                outfile.write(' %8d' % (votes155))
                outfile.write(' %8d' % (votes155thispct))
                pcttotal155 += votes155thispct
                outfile.write(' : %8d' % (pcttotal155))
                if votes152 != votes155:
                    outfile.write(' %8d 152-155DIFF\n' % (pcttotal155))
                else:
                    outfile.write('\n')
            outfile.write('%4s %20s' % (pctnumber, pct.getpctname()))
            outfile.write('%8d : %8d' % (pcttotal155, votes30ivo))
            outfile.write(' ( %8d )' % (pcttotal155 - votes30ivo))
            if (pcttotal155 < votes30ivo) and (pctnumber < '750'):
                outfile.write(' ZORK more in 30A than 155\n')
            elif (pcttotal155 > votes30ivo) and (pctnumber < '750'):
                outfile.write(' ZORK fewer in 30A than 155\n')
            else:
                outfile.write('\n')

            outfile.write('\n')

        outfile.write('Total number of pcts: %d\n\n' % (len(globalpcts)))
    ## END OF WRITEIVOSANDPCTS
    ##################################################################

    ##################################################################
    ## writememorycards: write the memorycards file
    def writememorycards(self, filenameprefix, county):
        """ This is the docstring.
        """
        if filenameprefix == 'stdout':
            outfile = sys.stdout
        else:
            outfile = open(filenameprefix+'MemoryCards.txt', 'w')
        outfile.write('Memory card collection times for %s\n\n' % (county))

        outputlist = []
        for ivonumber, ivo in sorted(globalivos.items()):
            local_s = '%s %s' % (ivo.getmemorycollectiontime(), ivonumber)
            outputlist.append(local_s)

        for local_s in sorted(outputlist):
            outfile.write('%s\n' % (local_s))

    ## END OF WRITEMEMORYCARDS
    ##################################################################

    ##################################################################
    ## writepctdetail: write the pctdetail file
    def writepctdetail(self, filenameprefix, county):
        """ This is the docstring.
        """
        if filenameprefix == 'stdout':
            outfile = sys.stdout
        else:
            outfile = open(filenameprefix+'PctDetail.txt', 'w')
        outfile.write('Pct data for %s\n\n' % (county))

        outfile.write('Vote counts are "registered (total optical ivo flash) 155 155thispct,"\n\n')

        for pctnumber, pct in sorted(globalpcts.items()):
            outfile.write('%s\n' % (pct))

        outfile.write('Total number of Pcts: %d\n' % (len(globalpcts)))
    ## END OF WRITEPCTDETAIL
    ##################################################################

    ##################################################################
    ## writepebdetail: write the pebdetail file
    def writepebdetail(self, filenameprefix, county):
        """ This is the docstring.
        """
        if filenameprefix == 'stdout':
            outfile = sys.stdout
        else:
            outfile = open(filenameprefix+'PEBDetail.txt', 'w')
        outfile.write('PEB data for %d PEBs for %s\n\n' % \
                       (len(globalpebs), county))

        firsttime = True
        for pebnumber, peb in sorted(globalpebs.items()):
            if firsttime:
                outfile.write('%s' % (peb.headerstring()))
                firsttime = False
            outfile.write('%s\n' % (peb))
        outfile.write('End of PEB data for %d PEBs for %s\n\n' % \
                       (len(globalpebs), county))

        outfile.write('\n')
        outfile.write('PEBs not used in closing in 152 and not in 68A\n')
        for pebnumber, peb in sorted(globalpebs.items()):
            if (not peb.getusedforclosing()) and (not peb.getfoundin68a()):
                outfile.write('%s' % (peb.getpebnumber()))
                outfile.write(' %s' % (peb.getpebtype()))
                outfile.write(' Closing in 152, In 68A: ')
                if peb.getusedforclosing():
                    outfile.write(' YES')
                else:
                    outfile.write(' NO ')
                if peb.getfoundin68a():
                    outfile.write(' YES')
                else:
                    outfile.write(' NO ')
                outfile.write('\n')
        outfile.write('\n')

        outfile.write('PEBs used in closing in 152 but not in 68A\n')
        for pebnumber, peb in sorted(globalpebs.items()):
            if (peb.getusedforclosing()) and (not peb.getfoundin68a()):
                outfile.write('%s' % (peb.getpebnumber()))
                outfile.write(' %s' % (peb.getpebtype()))
                outfile.write(' Closing in 152, NOT In 68A: ')
                if peb.getusedforclosing():
                    outfile.write(' YES')
                else:
                    outfile.write(' NO ')
                if peb.getfoundin68a():
                    outfile.write(' YES')
                else:
                    outfile.write(' NO ')
                outfile.write('\n')
        outfile.write('\n')

        outfile.write('PEBs not used in closing in 152 but present in 68A\n')
        for pebnumber, peb in sorted(globalpebs.items()):
            if (not peb.getusedforclosing()) and (peb.getfoundin68a()):
                outfile.write('%s' % (peb.getpebnumber()))
                outfile.write(' %s' % (peb.getpebtype()))
                outfile.write(' NOT Closing in 152, BUT In 68A: ')
                if peb.getusedforclosing():
                    outfile.write(' YES')
                else:
                    outfile.write(' NO ')
                if peb.getfoundin68a():
                    outfile.write(' YES')
                else:
                    outfile.write(' NO ')
                outfile.write('\n')
        outfile.write('\n')

        outfile.write('PEBs used in closing in 152 and present in 68A\n')
        for pebnumber, peb in sorted(globalpebs.items()):
            if (peb.getusedforclosing()) and (peb.getfoundin68a()):
                outfile.write('%s' % (peb.getpebnumber()))
                outfile.write(' %s' % (peb.getpebtype()))
                outfile.write(' Closing in 152, In 68A: ')
                if peb.getusedforclosing():
                    outfile.write(' YES')
                else:
                    outfile.write(' NO ')
                if peb.getfoundin68a():
                    outfile.write(' YES')
                else:
                    outfile.write(' NO ')
                outfile.write(' %s' % (peb.getvotecollectiontime()))
                outfile.write('\n')

        outfile.write('\n')

        outfile.write('Total number of PEBs: %d\n' % (len(globalpebs)))
    ## END OF WRITEPEBDETAIL
    ##################################################################
##
## END OF OUTPUT FUNCTIONS
######################################################################
