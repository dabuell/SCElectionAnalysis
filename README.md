# SCElectionAnalysis

CAVEAT:  This is the code as rewritten for the 2018 South Carolina data
that uses the upgraded iVotronic firmware and Unity software.  Some of
the code that is commented is from the version of this code that read
the data from an earlier version of the firmware and software. 

CAVEAT:  Some of the special cases come from the fact that not all
counties seem to use exactly the same software configuration.  This
means that some county-specific tests must be applied.


The "main" program is the 'driver.py' code. This is invoked and provided
with a "configuration" file.  I tend to label data files and such with
file names starting with 'x', 'y', or 'z' so they collate to the bottom
of a list of files and I can see them.

The 'zconfigfile' file is what I used for the 2018 primary and general
election.
The driver reads only what it needs:
* The directory that fills out the path to the data.
* The date of Election Day.
* Time the polls should open.
* Time the polls should close.
* Time that should be considered "too early" on Election Day.
* Time that should be considered "too late" on Election Day.
* The county.  This can be a list or just one.  The program reads county
  names until it hits a blank line.

Note that I only read this much, so I can store the rest of the county
names further down in the file.

So the current configuration file starts out:

DATA2018GeneralElection
2018_11_06
07:00:00
19:00:00
05:30:00
19:30:00
McCormick

date of election day
poll opening time (24 hour clock)
poll closing time (24 hour clock)
time when machine opening is considered "early" (24 hour clock)
time when closing/votes are considered "late" (24 hour clock)

The git repository has results for McCormick County, which is the
smallest of the counties in South Carolina and thus is suitable
for use in testing and as an example.
Data for McCormick County can be obtained at
    https://www.scvotes.org/data/Audit2018General.html
and then scrolling down to the "Audit Files" link.

