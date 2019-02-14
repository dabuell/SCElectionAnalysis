""" This is the docstring.
"""
######################################################################
## GETPCTNUMBERANDNAME: test to see if we should skip this line
def getpctnumberandname(line):
    """ This is the docstring.
    """
    ## pick up the pct from the header line on each page
    ## code for south carolina
    ## The precinct seems no longer (12 June 2018) to be in the 'RUN DATE' line
#    if 'RUN DATE' in line:
#        linesplit = line.split()
#        indexprecinct = linesplit.index('PRECINCT')
##        print('PRECINCT %s' % (indexprecinct))
#        indexelection = linesplit.index('ELECTION')
#        pctnumber = linesplit[indexprecinct+1]
#        pctname = '_'.join(linesplit[indexprecinct+3:indexelection])

    ## This seems to be the code for the new Unity output 12 June 2018
    linesplit = line.split()
    pctnumber = linesplit[1] 
    pctname = ' '.join(linesplit[2:])

    return pctnumber, pctname
## END OF GETPCTNUMBERANDNAME
######################################################################

######################################################################
## SKIPTHISLINE: test to see if we should skip this line
def skipthisline(line):
    """ This is the docstring.
    """
    retval = False

    if len(line.strip()) == 0:
        retval = True
    elif 'VOTR.' in line:
        retval = True
    return retval
## END OF SKIPTHISLINE
######################################################################
