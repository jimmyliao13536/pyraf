#! /usr/local/bin/python -i
"""
Start up pyraf (Python IRAF front end)

Brief help:

	To load a package:
		iraf.load("images")
		iraf.run("images")
	The .run version does not list the tasks after loading.
	You can also do iraf.load("images",doprint=0) or just
	iraf.load("images",0) to skip printing.

	To get short-hand task or package object:
		imstat = iraf.getTask("imstat")
		imhead = iraf.getTask("imheader")
		sts = iraf.getPkg("stsdas")
	Note minimum match is used for task names.  Packages are accessible
	using either getTask() or getPkg(), while tasks are available only
	through getTask().

	If the -p option is used, packages are defined as objects with
	the package name.  E.g. after startup you can load stsdas by
	saying
		stsdas()
	Note there is no minimum match in this case, you must type the
	entire package name.  Tasks are available as attributes of the
	package, e.g.
		restore()
		restore.lucy.lpar()
	When accessed this way, minimum match is used for the task names.
	Both tasks directly in the package and tasks in subpackages that
	have already been loaded are accessible (so images.imhead() works
	even though imheader is in the imutil package.)

	Similarly, if you set the -t option then both tasks and packages are
	defined as variables, so this will work:
		stsdas()
		restore()
		lucy.lpar()

	To set task parameters there are various syntaxes:
		imhead.long = "yes"
		imstat.image = "dev$pix"
		imstat.set("images","dev$pix")
		imhead.setParList("dev$pix",longhe="yes")
	As usual, minimum match is used for parameter names (so we can
	use just 'long' rather than 'longheader').

	To run tasks:
		imstat()
		imstat.run()
		iraf.run("imstat")
		imhead("dev$pix",long="yes")

$Id$

R. White, 1999 March 4
"""

import os, sys, iraf

def usage():
	print "Usage: %s [options]" % sys.argv[0]
	print """ where options are one or more of:
	-n  Keep user namespace clean, don't define tasks or packages
	    as variables (default)
	-p  Packages are defined as variables
	-t  Both tasks and packages are defined as variables
	-v  Set verbosity level (may be repeated to increase verbosity)
	-h  Print this message"""
	sys.exit()

# special initialization when this is the main program

if __name__ == "__main__":

	# read the user's startup file (if there is one)

	if os.environ.has_key('PYTHONSTARTUP') and \
			os.path.isfile(os.environ['PYTHONSTARTUP']):
		execfile(os.environ['PYTHONSTARTUP'])

	# use command-line options to define behavior for iraf namespaces
	# -n  Don't add anything to namespace (default)
	# -p  Add packages to namespace
	# -t  Add tasks (and packages) to namespace
	# -v  Increment verbosity (note can use multiple times to make
	#     more verbose, e.g. -v -v)

	import getopt, irafnames
	try:
		optlist,args = getopt.getopt(sys.argv[1:], "ptnvh")
	except getopt.error, e:
		print str(e)
		usage()
	verbose = 0
	if optlist:
		for opt, value in optlist:
			if opt == "-p":
				irafnames.setPkgStrategy()
			elif opt == "-t":
				irafnames.setTaskStrategy()
			elif opt == "-n":
				irafnames.setDefaultStrategy()
			elif opt == "-v":
				verbose = verbose + 1
			elif opt == "-h":
				usage()
	iraf.setVerbose(verbose)
	del getopt, irafnames, verbose

# load initial iraf symbols and packages

iraf.init()

yes = 1
no = 0
flpr = "This is not the IRAF cl!  Forget those old bad habits!"
retall = "This is not IDL..."

# set search path to include directory containing this script
# and current directory

dirname = os.path.dirname(sys.argv[0])
if not dirname: dirname = os.getcwd()
if dirname not in sys.path:
	sys.path.insert(0, dirname)
	sys.path.insert(0, '.')
del dirname

if __name__ == "__main__":
	#
	# start up monty keeping definitions in local name space
	#
	import monty
	print 'Pyraf, Python front end to IRAF (copyright AURA 1999)'
	print 'Python: ' + sys.copyright
	m = monty.monty(locals=locals())
	m.start()

