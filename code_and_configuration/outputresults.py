""" This is the docstring.
"""
#import sys
from collections import defaultdict

#from globalstuff import *
from globalstuff import global30Aresults
from globalstuff import globalmakeresultskeys
from globalstuff import globalpcts
from globalstuff import globalunpackkey
from globalstuff import globalvotes

######################################################################
## CLASS FOR RESULTS REPORTS
class Results:
    """ This is the docstring.
    """
    ##################################################################
    ## BOILERPLATE
    def __init__(self):
        """ This is the docstring.
        """
        self._dict2 = defaultdict(int)
        self._dict3 = defaultdict(int)
        self._dict4 = defaultdict(int)
    ##
    ## END OF BOILERPLATE
    ##################################################################

    ##################################################################
    ## WRITERESULTS: write the results files
    def writeresults(self, filenameprefix, county):
        """ This is the docstring.
        """
        self.writeresultsA(filenameprefix, county)
        self.writeresultsB(filenameprefix, county)
        self.writeresultsC(filenameprefix, county)
        self.writeresultsD(filenameprefix, county)
    ##
    ## END OF WRITERESULTS
    ##################################################################

    ##################################################################
    ## WRITERESULTSA: write the results pct, ivo, bs, cand, con
    def writeresultsA(self, filenameprefix, county):
        """ This is the docstring.
        """
        outfile = open(filenameprefix+'ResultsAPctIvoBSCanCon.txt', 'w')
        outfile.write('Results by Pct Ivo BS for %s\n\n' % (county))
        oldbstyle = ''
        for key, count in sorted(globalvotes.items()):
            pctnumber, ivonumber, bstyle, candidate, contest = globalunpackkey(key)
            if oldbstyle != bstyle:
                oldbstyle = bstyle
                outfile.write('\n')
            outfile.write('%6d %s\n' % (count, key))

            key2, key3, key4, key5 = globalmakeresultskeys(pctnumber, ivonumber,
                                                     candidate, contest)
            self._dict2[key2] += count  # pctnum, ivonum, con, cand
#            print('STORE3 %s %s' % (key3, count))
#            print('STORE5 %s %s' % (key5, count))
            self._dict3[key3] += count  # pctnum, con, cand
            self._dict3[key5] -= count  # pctnum, con, UNDERVOTE
            self._dict4[key4] += count  # con, cand
        outfile.close()
    ##
    ## END OF WRITERESULTSA
    ##################################################################

    ##################################################################
    ## WRITERESULTSB: write the results pct, ivo, cand, con
    def writeresultsB(self, filenameprefix, county):
        """ This is the docstring.
        """
        outfile = open(filenameprefix+'ResultsBPctIvoCanCon.txt', 'w')
        outfile.write('Results by Pct Ivo for %s\n\n' % (county))
        oldivonumber = ''
        for key, count in sorted(self._dict2.items()):
            keysplit = key.split()
            ivonumber = keysplit[1]
            if oldivonumber != ivonumber:
                oldivonumber = ivonumber
                outfile.write('\n')
            outfile.write('%6d %s\n' % (count, key))
        outfile.close()
    ##
    ## END OF WRITERESULTSB
    ##################################################################

    ##################################################################
    ## WRITERESULTSC: write the results pct, cand, con
    def writeresultsC(self, filenameprefix, county):
        """ This is the docstring.
        """
        outfile = open(filenameprefix+'ResultsCPctCanCon.txt', 'w')
        outfile.write('Results by Pct for %s\n\n' % (county))
        oldpctnumber = ''
        oldcontest = ''
        for key, count in sorted(self._dict3.items()):
            keysplit = key.split()
            pctnumber = keysplit[0]
            contest = keysplit[1]
            candidate = keysplit[2]
            if oldcontest != contest:
                oldcontest = contest
                outfile.write('\n')
            if oldpctnumber != pctnumber:
                oldpctnumber = pctnumber
                outfile.write('\n')

            if count < 0:  # this means the undervote line
                the155 = globalpcts[pctnumber].getvotescast155thispct()
                outfile.write('%6d %s %8d UNDERVOTEA\n' % (count+the155, key, the155))
#                if count+155 > 0:
#                    outfile.write('%6d %s %8d UNDERVOTEB\n' % (count+the155, key, the155))
            else:  # this means not the undervote line
                outfile.write('%6d %s\n' % (count, key))
# hampton
#            print('KEYSPLITONE %s : %s : %s' % (pctnumber, contest, candidate))
            for key30a, value30a in sorted(global30Aresults.items()):
# hampton
#                print('KEYSPLITTWOA %s : %s' % (key30a, value30a))
                key30asplit = key30a.split()
                if len(key30asplit) < 3:
                    continue
# hampton
#                print('KEYSPLITTWOB %s : %s' % (key30asplit, value30a))
                key30apctnumber = key30asplit[0]
                key30acontest = key30asplit[1]
                key30acandidate = key30asplit[2]
# hampton
#                print('KEYSPLITTWOC %s : %s : %s' % \
#                       (key30apctnumber, key30acontest, key30acandidate))
                if (pctnumber == key30apctnumber) and (candidate == key30acandidate):
# hampton
#                    print('KEYSPLITTWODMATCH %s : %s : %s' % (pctnumber, candidate, value30a))
                    for item in value30a:
                        item = item.replace('\r', '')
                        item = item.replace('\n', '')
# hampton
###                        outfile.write('      %s : %s\n' % (key30a, item))
                        lastdot = item.rindex(' . ')
                        itemnumbers = item[lastdot+3:]
                        thevote = itemnumbers.split()[0]
                        thevote = thevote.replace(',', '')
                        locallabel = ''
                     #   print('NUMBER', thevote)
                        if int(thevote) != count:
                            locallabel = 'THIRTYA ZORK'
###                        outfile.write('      %s : %s %s\n' % (key30a, item, locallabel))
                   # sys.exit(0)
                    continue
        outfile.close()
    ##
    ## END OF WRITERESULTSC
    ##################################################################

    ##################################################################
    ## WRITERESULTSD: write the results cand, con
    def writeresultsD(self, filenameprefix, county):
        """ This is the docstring.
        """
        outfile = open(filenameprefix+'ResultsDCanCon.txt', 'w')
        outfile.write('Results for %s\n\n' % (county))
        oldcontest = ''
        for key, count in sorted(self._dict4.items()):
            keysplit = key.split()
            contest = keysplit[0]
            if oldcontest != contest:
                oldcontest = contest
                outfile.write('\n')
            outfile.write('%6d %s\n' % (count, key))
        outfile.close()
    ##
    ## END OF WRITERESULTSD
    ##################################################################
##
## END OF RESULTS
######################################################################
