#!/usr/bin/python

import sys
import json
import requests
import os.path

uriprepend = 'https://api.github.com/repos/'

BB = '/home/causten/openbmc-barreleye/meta-phosphor/common/recipes-phosphor/'
FNAMES = [
	'obmc-phosphor-event/obmc-phosphor-event.bb',
	'skeleton/skeleton.bb',
	'host-ipmid/host-ipmid.bb',
	'host-ipmid/host-ipmid-oem.bb',
	'host-ipmid/host-ipmi-bt.bb',
	'host-ipmid/btbridged.bb',
	'host-ipmid/host-ipmid-tool.bb',
	'host-ipmid/host-ipmi-hw-example.bb',
	'host-ipmid/host-ipmid-fru.bb',
	]



def isgithub(uri) :
	return uri.find('github.com')


##################################################################################
# Works like the curl command
# curl -k https://api.github.com/repos/openbmc/phosphor-host-ipmid/branches/master
##################################################################################
def githubversion(url):

	return 'bebdb23ea092df6cde23e6da2a8940bd84de4810'
	#githuburi = url.replace('git://github.com/', uriprepend) + '/branches/master'
	#r = requests.get(githuburi)
	#j = r.json()
	#v = j['commit']['sha']
	#return v


##################################################################################
#
# Returns 2 item list.  srcrev and srcurl
#
# Note: ${AUTOREV} is a valid return
##################################################################################
def extractrevandurl(filename):

	with open(filename, 'r') as f:
	    data = f.readlines()
	
	    for line in data:
	        if line.find('SRCREV') >= 0:
	        	srcrev = line.split('=')[1].strip()
	        	srcrev = srcrev.replace('"','')
	
	        if line.find('SRC_URI') >= 0:
	        	srcurl =  line.split('=')[1].strip()
	        	srcurl = srcurl.replace('"','')

	return [srcrev, srcurl]


def isuptodate(localrev, githubrev):

	if (localrev == '${AUTOREV}') or (githubrev == localrev):
		return True
	else:
		return False



def main():

	for f in FNAMES:

		fn = BB+f
		if os.path.isfile(fn) == False :
			print "ERROR: Not a file " + f
			continue

		srcrev , srcurl = extractrevandurl(fn)

		if srcurl == '' :
			print 'ERROR: no plugin for ' + sys.argv[1]
			continue
		
		if isgithub(srcurl) >= 0: 
			masterversion = githubversion(srcurl)
		
			if isuptodate(srcrev, masterversion):
				print 'Up to date : ' + f
			else:
				print 'OUT OF DATE: ' + f
		




if __name__ == "__main__":
    main()









