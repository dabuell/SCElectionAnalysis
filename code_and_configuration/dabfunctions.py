""" This is the docstring.
"""
##def checkargs(number, message):

######################################################################
##
import sys

######################################################################
## CHECK ARGUMENTS
def checkargs(number, message):
    """ This is the docstring.
    """
    if len(sys.argv) != number:
        print(message)
        sys.exit(1)

