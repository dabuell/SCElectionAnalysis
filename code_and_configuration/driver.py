""" This is the docstring for this file.
"""
import sys
#from collections import defaultdict

from dabfunctions import checkargs

from configuration import Configuration
#from globalstuff import globaldump68A
#from globalstuff import globaldump152
#from globalstuff import globaldump155
from globalstuff import globalivos
from globalstuff import globalpcts
from globalstuff import globalresetglobals

from f152 import F152
from f155 import F155
from f30a import F30A
from f68a import F68A

from outputfunctions import OutputFunctions
from outputexceptions import Exceptions
from outputresults import Results

from outputfirstlastworking import FirstLastWorking

######################################################################
## create the prefix for the input files
def createinfilenameprefix(datapath, county):
    """
    Create the prefix for file names for input data.
    """
#    print('CREATE PATH   %s' % (datapath))
#    print('CREATE COUNTY %s' % (county))
    prefix = '../../votingdata/' + datapath + '/' + county + '/'
#    prefix += '/2016 Audit Workspace (All elections)/Republican PPP/'
#    prefix = '../../VotingData/DATA2016PrimaryDem/' + county
#    prefix += '/2016 Audit Workspace (All elections)/Democratic PPP/'
#    prefix += county.upper() + '/'
#    prefix = '../../VotingData/DATA2012GeneralElection/' + county + '/'
#    prefix = '../../VotingData/Data2016GeneralElection/' + county + '/'
    return prefix

######################################################################
## create the prefix for the output files
def createoutfilenameprefix(county, date):
    """
    Create the prefix for file names for output.
    """
    dateadjusted = date.replace('_', '')
    prefix = county + '_' + dateadjusted + '_'
    return prefix

######################################################################
## main program as a function
def main():
    """
    Main program used only to hide local variables.
    """
    ## check arguments and open the output file
    checkargs(2, "usage: a.out configfilename")
    ##
    theconfig = Configuration(sys.argv[1])
    print(theconfig)

    counties = theconfig.getcounties()
    outputfunctions = OutputFunctions()

    print('DRIVER: this date %s' % (theconfig.getdate()))
    print('DRIVER: this year %s' % (theconfig.getyearfromdate()))
    print('DRIVER: this counties %s' % (counties))

    ## loop on the counties and do the computation
    for county in counties:
        globalresetglobals()
        infilenameprefix = createinfilenameprefix(theconfig.getdatapath(), \
                                                  county)
        print('DRIVER: in prefix: %s' % (infilenameprefix))
        outfilenameprefix = createoutfilenameprefix(county, theconfig.getdate())
        print('DRIVER: out prefix:%s' % (outfilenameprefix))

        print('DRIVER: read 152')
        f152 = F152(infilenameprefix, theconfig)
        print('DRIVER: done read 152')

        #  Update the ivos based on the events.
        #  This code used to be further down but has been moved here on the
        #  assumption that it doesn't need 155 or 68A information.
        for ivonumber, ivo in sorted(globalivos.items()):
#            print('DRIVER: ivo#,ivo: %s %s' % (ivonumber, ivo))
            ivo.updateivofromevents(theconfig.getdate(), theconfig)

        #  We can now write the actual log files.
#        outputfunctions.writeeventlogs('152dump_', county)
#        outputfunctions.writeeventtexts('152dump_', county)
#        outputfunctions.writeeventcounts('152dump_', county)

        # And we can dump what data we have from only the 152.
        # The global dump of the 152 is the three outputs above and
        #     these two below.
#        outputfunctions.writeivodetail('152dump_', county)
#        outputfunctions.writepebdetail('152dump_', county)
     #   sys.exit()

        print('DRIVER: read 155')
        f155 = F155()
        f155.readdata(infilenameprefix, theconfig.getdate())
        # And we can dump what data we have from the 152 and 155.
        # The global dump of the 155 is these three outputs below.
#        globaldump155()
#        outputfunctions.writeivodetail('155dump_', county)
#        outputfunctions.writepebdetail('155dump_', county)
#        outputfunctions.writepctdetail('155dump_', county)
        print('DRIVER: done read 155')

        print('DRIVER: read 68A')
        f68a = F68A()
        f68a.readdata(infilenameprefix, theconfig.getdate())
        # We now dump what data we have from the 152, 155, and 68A.
        # The global dump of the 68A is the three outputs above and
        #     these two below.
#        globaldump68A()
#        outputfunctions.writeivodetail('68Adump_', county)
#        outputfunctions.writepebdetail('68Adump_', county)
#        outputfunctions.writepctdetail('68Adump_', county)
        print('DRIVER: done read 68A')

        print('DRIVER: read 30A')
        f30a = F30A(infilenameprefix, theconfig.getdate(), county)
        print('DRIVER: done read 30A')

#        for ivonumber, ivo in sorted(globalivos.items()):
##            print('DRIVER: ivo#,ivo: %s %s' % (ivonumber, ivo))
#            ivo.updateivofromevents(theconfig.getdate(), theconfig)

        ## now update for each pct the pebs used for closing for each ivo
        for pctnumber, pct in sorted(globalpcts.items()):
            for ivonumber in pct.getivos():
                ivo = globalivos[ivonumber]
                pct.addtoopeningpebs(ivo.getpebnumberopening())
                pct.addtoclosingpebs(ivo.getpebnumberclosing())
                pct.addtovotescast155(ivo.getvotescast155(), \
                                      ivo.getvotescast155bypct(pctnumber))
        #sys.exit()

        print('DRIVER: %s' % (f152))
        print('DRIVER: %s' % (f155))
        print('DRIVER: %s' % (f68a))
        print('DRIVER: %s' % (f30a))

        outputfunctions = OutputFunctions()
        outputfunctions.writeivodetail(outfilenameprefix, county)
        outputfunctions.writepebdetail(outfilenameprefix, county)
        outputfunctions.writepctdetail(outfilenameprefix, county)
        outputfunctions.writememorycards(outfilenameprefix, county)
        outputfunctions.writeeventlogs(outfilenameprefix, county)
        outputfunctions.writeeventtexts(outfilenameprefix, county)
        outputfunctions.writeeventcounts(outfilenameprefix, county)

        print('DRIVER: WRITE FIRST FILES DONE')

        results = Results()
        results.writeresults(outfilenameprefix, county)

        print('DRIVER: WRITE RESULTS FILES DONE')

        exceptions = Exceptions()
        exceptions.writeexceptions(outfilenameprefix, county, theconfig)

        print('DRIVER: WRITE EXCEPTIONS FILES DONE')

        firstlastworking = FirstLastWorking()
        firstlastworking.writefirstlastworking(outfilenameprefix, county, theconfig)

        print('DRIVER: WRITE FIRSTLASTWORKING FILES DONE')

        outputfunctions.writeivosandpcts(outfilenameprefix, county)
        outputfunctions.writeballotstyles(outfilenameprefix, county)

        print('DRIVER: DONE!!!')

######################################################################
## main program for this computation
main()
