#!/usr/bin/python

import sys
import json
import requests
import os.path
import getpass

uriprepend = 'https://api.github.com/repos/'

BB = '/home/causten/openbmc-barreleye/meta-phosphor/common/'
FNAMES = [
	#'recipes-kernel/linux/linux-obmc_4.3.bb',
	'recipes-phosphor/obmc-phosphor-event/obmc-phosphor-event.bb',
	'recipes-phosphor/skeleton/skeleton.bb',
	'recipes-phosphor/host-ipmid/host-ipmid.bb',
	'recipes-phosphor/host-ipmid/host-ipmid-oem.bb',
	'recipes-phosphor/host-ipmid/btbridged.bb',
	'recipes-phosphor/host-ipmid/host-ipmid-tool.bb',
	'recipes-phosphor/host-ipmid/host-ipmid-fru.bb',
	'recipes-phosphor/dbus/obmc-mapper.bb',
	'recipes-phosphor/dbus/obmc-rest.bb',
	]


def isgithub(uri) :
	return uri.find('github.com')


##################################################################################
# Works like the curl command
# curl -k https://api.github.com/repos/openbmc/phosphor-host-ipmid/branches/master
# curl -k https://api.github.com/repos/openbmc/linux/branches/dev-4.3
##################################################################################
def githubversion(url, branch, usr, pw):

	#return 'bebdb23ea092df6cde23e6da2a8940bd84de4810'
	githuburi = url.replace('git://github.com/', uriprepend) + '/branches/' + branch
	r = requests.get(githuburi, auth=(usr,pw))
	j = r.json()
	v = j['commit']['sha']
	return v


##################################################################################
#
# Returns 2 item list.  srcrev and srcurl
#
# Note: ${AUTOREV} is a valid return
# Note: TODO : handle linux tag/release
# Note TODO: Handle line continuations...
#
#	SRC_URI += " \
#        git://github.com/openbmc/phosphor-rest-server \
#        "
##################################################################################
def extractrevandurlv2(filename):
	branch = 'master'
	srcrev = ''
	srcurl = ''
	with open(filename, 'r') as f:
		data = f.readlines()

		for line in data:
			if line.find('SRCREV') >= 0:
				srcrev = line.split('=')[1].strip()
				srcrev = srcrev.replace('"','')
	
			if line.find('SRC_URI') >= 0:
				x = line.find('"')
				y = line.rfind('"')



		x = data.find('SRCREV')
		s = data[x+5:]
		x = s.find('"')
		s = s[x+1:]
		print s


	
	return [srcrev, srcurl, branch]



def extractrevandurl(filename):
	
	branch = 'master'
	
	with open(filename, 'r') as f:
		data = f.readlines()
	
		for line in data:
			if line.find('SRCREV') >= 0:
				srcrev = line.split('=')[1].strip()
				srcrev = srcrev.replace('"','')
	
			if line.find('SRC_URI') >= 0:
				x = line.find('"')
				y = line.rfind('"')

				completeuri = line[x+1:y]
				urigroups   = completeuri.split(';')

				for b in urigroups:
					if 'git://github.com' in b:
						srcurl = b
					if 'branch' in b:
						branch = b.split('=')[1]


	if '${' in branch:
		x = branch.find('{')
		y = branch.find('}')

		branchvar = branch[x+1:y]

		print "Variable found for branch : " + branchvar

		for line in data:
			if branchvar in line:
				var = line.split('=')[1]
				print "Found branch name " + var
				break
	
	return [srcrev, srcurl, branch]


def isuptodate(localrev, githubrev):

	if (localrev == '${AUTOREV}') or (githubrev == localrev):
		return True
	else:
		return False



def main():

	usr = getpass.getuser()
	pwd = getpass.getpass("enter github password for user %s: " % usr)


	for f in FNAMES:

		fn = BB+f
		if os.path.isfile(fn) == False :
			print "ERROR: Not a file " + f
			continue

		srcrev , srcurl, branch = extractrevandurl(fn)

		if srcurl == '' :
			print 'ERROR: no plugin for ' + sys.argv[1]
			continue
		
		if isgithub(srcurl) >= 0: 
			masterversion = githubversion(srcurl, branch, usr, pwd)
		
			if isuptodate(srcrev, masterversion):
				print 'Up to date : ' + f
			else:
				print 'OUT OF DATE: ' + BB+ f
		




if __name__ == "__main__":
	main()









