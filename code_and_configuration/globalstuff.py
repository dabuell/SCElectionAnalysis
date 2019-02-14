""" This is the docstring.
"""
#import sys
from collections import defaultdict

######################################################################
## GLOBAL DICTIONARY DEFINITIONS
global30Aresults = defaultdict(list)
globalcontestcandidate = set()
globalivos = defaultdict(str)
globalpcts = defaultdict(str)
globalpebs = defaultdict(str)
globaltextforcode = defaultdict(str)
globalvotes = defaultdict(int)

ALLPCTS = 'ALLPCTS'

DUMMYIVO = 'IVOxxxx'
DUMMYPEB = 'PEBxxx'
DUMMYVOTECOUNT = -9999
DUMMYDATE = 'dummydate'
DUMMYTIME = 'dummytime'
DUMMYOPENTIME = 'dummyopentime'
DUMMYCLOSETIME = 'dummyclosetime'

######################################################################
## GLOBALCONVERTTIMETOEPOCH: convert time to time since epoch
## The epoch is 00:00:00 on the day of the election.
def globalconverttimetoepoch(date, time):
    """ This is the docstring.
    """
    datesplit = date.split('_')
    timesplit = time.split(':')

    if datesplit[0] == '1994':
        year = 1994
        month = 1
        day = 1
    else:
        year = int(datesplit[0])
        month = int(datesplit[1])
        day = int(datesplit[2])

    yearoffset = year - 1970
    monthoffset = 0
    if month > 1:
        monthoffset += 31
    if month > 2:
        monthoffset += 29
    if month > 3:
        monthoffset += 31
    if month > 4:
        monthoffset += 30
    if month > 5:
        monthoffset += 31
    if month > 6:
        monthoffset += 30
    if month > 7:
        monthoffset += 31
    if month > 8:
        monthoffset += 31
    if month > 9:
        monthoffset += 30
    if month > 10:
        monthoffset += 31
    if month > 11:
        monthoffset += 30

    dateoffset = (yearoffset*365 + monthoffset + day) * 86400

    if year == 1994:
        dayoffset = 0
    else:
        dayoffset = (int(timesplit[0]) * 3600) + (int(timesplit[1]) * 60) + \
                    (int(timesplit[2]))
    epochtime = dateoffset + dayoffset

#    print 'EPOCH', year, month, day, hour, minute, second, epochtime

    return epochtime
##
## END OF GLOBALCONVERTTIMETOEPOCH
######################################################################

######################################################################
## GLOBALCREATETIMEBLOCKS: create counts by time block
def globalcreatetimeblocks(timeblockdata):
    """ This is the docstring.
    """
    timeblockcounts = defaultdict(int)
    for hour in range(0, 26):
        for quarter in range(0, 60, 15):
            timeblock = '%02d:%02d' % (hour, quarter)
            timeblockcounts[timeblock] = 0

    for seconds in timeblockdata:
        timeblock = globalsecondstotimeblock(seconds)
        timeblockcounts[timeblock] += 1

    return timeblockcounts
##
## END OF GLOBALCREATETIMEBLOCKS
######################################################################

######################################################################
## GLOBALDISPLAYTIMEBLOCKS: display counts by time block
def globaldisplaytimeblocks(timeblockcounts, maxcount, label):
    """ This is the docstring.
    """
    local_s = ''
    runningtotal = 0
    for block, count in sorted(timeblockcounts.items()):
        runningtotal += count
        if runningtotal > 0:
            local_s += '%s %s %6d : %6d\n' % (label, block, count, runningtotal)
        if runningtotal >= maxcount:
            break

    return local_s
##
## END OF GLOBALDISPLAYTIMEBLOCKS
######################################################################

#######################################################################
### DUMP68A: dump the 68A data for examination
#def globaldump68A():
#    """ This is the docstring.
#    """
#    print('%s' % (globaltostringivos()))
#    print('%s' % (globaltostringpebs()))
#    print('%s' % (globaltostringpcts()))
###
### END OF DUMP68A
#######################################################################

#######################################################################
### DUMP152: dump the 152 data for examination
#def globaldump152(county):
#    """ This is the docstring.
#    """
#    print('%s' % (globaltostringivos()))
#    print('%s' % (globaltostringpebs()))
#    print('%s' % (globaltostringeventsbyivo()))
#    print('%s' % (globaltostringtextforcode()))
###
### END OF DUMP152
#######################################################################

#######################################################################
### DUMP155: dump the 155 data for examination
#def globaldump155():
#    """ This is the docstring.
#    """
#    print('%s' % (globaltostringivos()))
#    print('%s' % (globaltostringpebs()))
#    print('%s' % (globaltostringpcts()))
###
### END OF DUMP155
######################################################################

######################################################################
## GLOBALGETPCTSMISSINGFROM155: get the pcts missing from the 155
def globalgetpctsmissingfrom155():
    """ This is the docstring.
    """
    local_s = ''

    count = 0
    for pctnumber, pct in sorted(globalpcts.items()):
        if pctnumber >= '0750':
            continue
        if DUMMYVOTECOUNT == pct.getvotescast155():
            local_s += 'PCT MISSING %s %s xxxxx vote(s)\n' % \
                        (pctnumber, pct.getpctname())
            count += 1
    local_s += 'Number of such pcts: %d\n' % (count)

    return local_s
## END OF GLOBALGETPCTSMISSINGFROM155
######################################################################

######################################################################
## GLOBALGETPCTSMISSINGMEMORYCARDDATA: get the pcts missing memory card data
def globalgetpctsmissingmemorycarddata():
    """ This is the docstring.
    """
    local_s = ''

    count = 0
    for pctnumber, pct in sorted(globalpcts.items()):
        if pctnumber >= '0750':
            continue
        votes30ivo = pct.getvotescast30ivo()
        votes155thispct = pct.getvotescast155thispct()
        if DUMMYVOTECOUNT == votes155thispct:
            votes155thispct = 0
        if votes30ivo != votes155thispct:
            local_s += 'DATA MISSING: %s %-30s: 155 file is missing %6d vote(    s)\n' % \
                        (pctnumber, pct.getpctname(), \
                         votes30ivo-votes155thispct)
            count += 1
    local_s += 'Number of such pcts: %d\n' % (count)

    return local_s
## END OF GLOBALGETPCTSMISSINGMEMORYCARDDATA
######################################################################

######################################################################
## GLOBALGETTOTAL152: get the county totals for the 152 votes
def globalgettotal152():
    """ This is the docstring.
    """
    total152 = 0
    for ivonumber, ivo in globalivos.items():
        total152 += ivo.getvotescast152()
    return total152
## END OF GLOBALGETTOTAL152
######################################################################

######################################################################
## GLOBALGETTOTAL155: get the county totals for the 155 votes
def globalgettotal155():
    """ This is the docstring.
    """
    total155 = 0
    for ivonumber, ivo in globalivos.items():
        total155 += ivo.getvotescast155()
    return total155
## END OF GLOBALGETTOTAL155
######################################################################

######################################################################
## GLOBALMAKEKEYFORVOTES: make a key for each vote from all the info
def globalmakekeyforvotes(pctnumber, ivonumber, ballotstyle, \
                          sequence, candidate, contest):
    """ This is the docstring.
    """
    key = '%4s %7s %3s %3s %-35s %s' % (pctnumber, ivonumber, \
                                       ballotstyle, sequence, \
                                       candidate, contest)
    return key
##
## END OF GLOBALMAKEKEYFORVOTES
######################################################################

######################################################################
## GLOBALMAKERESULTSKEYS: make the keys for each vote for all the
## coarser level counting
def globalmakeresultskeys(pctnumber, ivonumber, candidate, contest):
    """ This is the docstring.
    """
    key2 = '%4s %7s %-35s %-35s' % (pctnumber, ivonumber, contest, candidate)
    key3 = '%4s %-35s %-35s' % (pctnumber, contest, candidate)
    key4 = '%-35s %-35s' % (contest, candidate)
    key5 = '%4s %-35s %-35s' % (pctnumber, contest, 'UNDERVOTE')
    return key2, key3, key4, key5
##
## END OF GLOBALMAKERESULTSKEYS
######################################################################

######################################################################
## GLOBALRESETGLOBALS: reset all the globals
##    this is to be done before starting work on a new county
def globalresetglobals():
    """ This is the docstring.
    """
    globalivos.clear()
    globalpcts.clear()
    globalpebs.clear()
    globaltextforcode.clear()
    globalvotes.clear()
## END OF GLOBALRESETGLOBALS
######################################################################

######################################################################
## GLOBALSECONDSTOTIMEBLOCK: convert seconds to 'hh:mm' as string
## MAGIC NUMBERS: 93600 means 2am the day after election day
def globalsecondstotimeblock(seconds):
    """ This is the docstring.
    """
#    print('SECONDS %s' % (seconds))
    if seconds < 0:
        seconds = 0
    if seconds > 93600:
        seconds = 93599

    hour = seconds // 3600 # python 3.0 demands double slash
    remaining = seconds % 3600
    quarter = remaining // 900 # python 3.0 demands double slash

    blocks = ['00', '15', '30', '45']
    timeblock = '%02d:%2s' % (hour, blocks[quarter])

    return timeblock
## END OF GLOBALSECONDSTOTIMEBLOCK
######################################################################

######################################################################
## GLOBALTOSTRINGCANDIDATECONTEST: output all the candidate/contests
def globaltostringcontestcandidate():
    """ This is the docstring.
    """

    local_s = ''
    local_s += 'CANDIDATES AND CONTESTS\n'
    for concand in sorted(globalcontestcandidate):
        local_s += '%-s\n' % (concand)
    local_s += 'END OF CANDIDATES AND CONTESTS\n'
    return local_s
## END OF GLOBALTOSTRINGCANDIDATECONTEST
######################################################################

######################################################################
## GLOBALTOSTRINGEVENTSBYIVO: output all the events by ivos
def globaltostringeventsbyivo():
    """ This is the docstring.
    """
    local_s = ''
    sequence = 0
    ivocount = len(globalivos)
    local_s += 'EVENTS FOR THE %d IVOS\n' % (ivocount)
    for ivonumber, ivo in sorted(globalivos.items()):
        sequence += 1
        local_s += '%4d %s: %s\n' % (sequence, ivonumber, ivo.tostringevents())
    local_s += 'END OF EVENTS BY IVO INFORMATION\n'
    return local_s
## END OF GLOBALTOSTRINGEVENTSBYIVO
######################################################################

######################################################################
## GLOBALTOSTRINGIVOS: output all the ivos as a string
def globaltostringivos():
    """ This is the docstring.
    """
    sss = ''
#    sequence = 0
    ivocount = len(globalivos)
    sss += 'IVO INFORMATION FOR %d IVOS\n' % (ivocount)
    firsttime = True
    for ivonumber, ivo in sorted(globalivos.items()):
        if firsttime:
            sss += ivo.headerstring()
            firsttime = False
#        sequence += 1
#        sss += '%s' % (ivo.tostring("ZZZOOO"))
        sss += '%s\n' % (ivo) # new version
    sss += 'END OF IVO INFORMATION FOR %d IVOS\n' % (ivocount)
    return sss
## END OF GLOBALTOSTRINGIVOS
######################################################################

######################################################################
## GLOBALTOSTRINGPCTS: output all the pcts as a string
def globaltostringpcts():
    """ This is only used to dump pcts while testing code.
    """
    local_s = ''
    sequence = 0
    pctcount = len(globalpcts)
    local_s += 'PCT INFORMATION FOR %d PCTS\n' % (pctcount)
    for pctnumber, pct in sorted(globalpcts.items()):
        sequence += 1
        local_s += '%4d %s: %s\n' % (sequence, pctnumber, pct)
    local_s += 'END OF PCT INFORMATION\n'

    return local_s

## END OF GLOBALTOSTRINGPCTS
######################################################################

######################################################################
## GLOBALTOSTRINGPEBS: output all the pebs as a string
def globaltostringpebs():
    """ This is the docstring.
    """
    sss = ''
    sequence = 0
    pebcount = len(globalpebs)
    sss += 'PEB INFORMATION FOR %d PEBS\n' % (pebcount)
    for pebnumber, peb in sorted(globalpebs.items()):
        sequence += 1
        sss += '%4d %s: %s\n' % (sequence, pebnumber, peb)
    sss += 'END OF PEB INFORMATION FOR %d PEBS\n' % (pebcount)

    return sss

## END OF GLOBALTOSTRINGPEBS
######################################################################

######################################################################
## GLOBALTOSTRINGTEXTFORCODE: output all the codes and their text as a string
def globaltostringtextforcode():
    """ This is the docstring.
    """
    local_s = ''
    sequence = 0
    textcount = len(globaltextforcode)
    local_s += 'TEXTFORCODE INFORMATION FOR %5d CODES\n' % (textcount)
    for code, text in sorted(globaltextforcode.items()):
        sequence += 1
        local_s += '%4d %s: %s\n' % (sequence, code, text)
    local_s += 'END OF TEXTFORCODE INFORMATION\n'
    return local_s
## END OF GLOBALTOSTRINGTEXTFORCODE
######################################################################

######################################################################
## GLOBALTOSTRINGVOTECOUNT: output the vote count as a string
## the purpose for this is to output 'xxxx' instead of dummy
def globaltostringvotecount(value, width):
    """ This is the docstring.
    """
    local_s = ''
    formatstring = '%%%dd' % (width)
#    print 'WWWWWWUUUUUUUU', formatstring
    if DUMMYVOTECOUNT == value:
        local_s = 'xxxxxxxxxxxxxxxxxxxx'[0:width]
    else:
        local_s = formatstring % (value)

#    print 'WWWWWWUUUUUUUU', local_s

    return local_s
## END OF GLOBALTOSTRINGVOTECOUNT
######################################################################

######################################################################
## GLOBALTOSTRINGVOTES: output all the votes
def globaltostringvotes():
    """ This is the docstring.
    """
    local_s = ''
    sequence = 0
    votecount = len(globalvotes)
    local_s += 'VOTE INFORMATION FOR %7d VOTES\n' % (votecount)
    for vote, count in sorted(globalvotes.items()):
        sequence += 1
        local_s += '%4d %7d: %s\n' % (sequence, count, vote)
    local_s += 'END OF VOTE INFORMATION\n'
    return local_s
## END OF GLOBALTOSTRINGVOTES
######################################################################

######################################################################
## GLOBALUNPACKKEY: unpack a key for each vote from all the info
def globalunpackkey(key):
    """ This is the docstring.
    """
    keysplit = key.split()
#    print keysplit
    pctnumber = keysplit[0]
    ivonumber = keysplit[1]
    ballotstyle = keysplit[2]
#    sequence = keysplit[3]
    candidate = keysplit[4]
    contest = keysplit[5]

#    s = "'%s' '%s' '%s' '%s' '%s'" % (pctnumber, ivonumber, ballotstyle, candidate, contest)
#    print key
#    print s
#    print '\n'
    return pctnumber, ivonumber, ballotstyle, candidate, contest
##
## END OF GLOBALUNPACKKEY
######################################################################

######################################################################
## GLOBALUPDATECANDIDATECONTESTFROM30A: update the vote totals from 30A
def globalupdate30Aresults(county, pctnumber, concand, line):
    """ This is the docstring.
    """
    # we don't need county now, but might need later

    # this code won't work because zero vote lines have a diff number of items
##    linesplit = line.split()
##    lensplit = len(linesplit)
##    print 'UPDATE', linesplit
##    totalvotes = 0
##    opticalvotes = 0
##    ivovotes = 0
##    flashvotes = 0
##
##    if county == 'beaufort':
##        # total(-4), percent(-3), paper(-2), ivo(-1)
##        totalvotes = linesplit[lensplit-4]
##        opticalvotes = linesplit[lensplit-2]
##        ivovotes = linesplit[lensplit-1]
##        print 'IN UPDATE', totalvotes, ivovotes, opticalvotes, flashvotes
##        value = [int(totalvotes), int(ivovotes), int(opticalvotes), int(flashvotes)]
##        key = '%5s %s' % (pctnumber, candidate)
##        globalcandidatecontest30A[key] = value

##    print 'END UPDATE', pctnumber, candidate, value

#    print('UPDATE %s %s %s' % (pctnumber, concand, line))
    localkey = '%5s %s' % (pctnumber, concand)
    locallist = global30Aresults[localkey]
    locallist.append(line)
    global30Aresults[localkey] = locallist
#    print 'END UPDATE'

    return
##
## END OF GLOBALUPDATECANDIDATECONTESTFROM30A
######################################################################
