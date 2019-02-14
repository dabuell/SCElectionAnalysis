""" This is the docstring.
"""
######################################################################
## SKIPTHISLINE: test to see if we should skip this line
def skipthisline(line):
    """ This is the docstring.
    """
    retval = False
    if len(line) < 52: # require up through the code in the line
        retval = True
    elif 'ELECTION ID' in line:
        retval = True
    elif 'RUN DATE' in line:
        retval = True
    elif 'OFFICIAL' in line:
        retval = True
    elif 'Votronic' in line:
        retval = True
    elif 'official' in line: ## horry
        retval = True
    elif 'Official' in line: ## charleston, cherokee
        retval = True
    elif 'General Election' in line: ## charleston
        retval = True
    elif 'Novembe' in line: ## charleston
        retval = True
    elif 'REPORT' in line: ## york
        retval = True
    elif 'Marlboro' in line: ## marlboro
        retval = True
    elif 'PPP Rep' in line: ## marlboro
        retval = True
    elif 'February' in line: ## marlboro
        retval = True

#    print('RETURN ', retval)
    return retval
## END OF SKIPTHISLINE
######################################################################
