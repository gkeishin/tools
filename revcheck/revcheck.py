#!/usr/bin/python

import sys
import json
import requests
import os.path
import getpass

uriprepend = 'https://api.github.com/repos/'

BB = '/home/causten/openbmc-barreleye/meta-phosphor/common/'
FNAMES = [
	#'recipes-kernel/linux/linux-obmc_4.4.bb',
	'recipes-phosphor/obmc-phosphor-event/obmc-phosphor-event.bb',
	'recipes-phosphor/skeleton/skeleton.bb',
	'recipes-phosphor/host-ipmid/host-ipmid.bb',
	'recipes-phosphor/host-ipmid/host-ipmid-oem.bb',
	'recipes-phosphor/host-ipmid/btbridged.bb',
	'recipes-phosphor/host-ipmid/host-ipmid-tool.bb',
	'recipes-phosphor/host-ipmid/host-ipmid-fru.bb',
	'recipes-phosphor/dbus/obmc-mapper.bb',
	'recipes-phosphor/dbus/obmc-rest.bb',
	'recipes-phosphor/rest-dbus/rest-dbus.bb',
	'recipes-phosphor/settings/settings.bb',
	'recipes-phosphor/obmc-phosphor-user/obmc-phosphor-user.bb',
	'recipes-phosphor/inarp/inarp.bb',
	'recipes-phosphor/network/network.bb',
	'recipes-phosphor/obmc-phosphor-fan/obmc-phosphor-fand.bb',
	'recipes-phosphor/skeleton/pyphosphor.bb',
	'recipes-phosphor/obmc-console/obmc-console.bb',
	'recipes-phosphor/obmc-phosphor-initfs/obmc-phosphor-init.bb',
	'recipes-phosphor/host-ipmid/host-ipmi-bt.bb',
	'recipes-phosphor/host-ipmid/host-ipmi-hw-example.bb',
	'recipes-phosphor/packagegroups/packagegroup-obmc-phosphor-apps.bb',
	'recipes-phosphor/obmc-phosphor-chassis/obmc-phosphor-chassisd.bb',
	'recipes-phosphor/obmc-phosphor-flash/obmc-phosphor-flashd.bb',
	'recipes-phosphor/obmc-phosphor-policy/obmc-phosphor-policyd.bb',
	'recipes-phosphor/obmc-phosphor-example-sdbus/obmc-phosphor-example-sdbus.bb',
	'recipes-phosphor/images/obmc-phosphor-image.bb',
	'recipes-phosphor/images/obmc-phosphor-image-no-sysmgr.bb',
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

	#print 'githuburi:' + githuburi
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
##################################################################################
def extractrevandurl(filename):
	
	branch = 'master'
	linecontinue = False
	completeuri = ''
	tline = ''
	srcurl = ''
	srcrev = ''
	
	with open(filename, 'r') as f:
		data = f.readlines()
	
		for line in data:

			line = line.strip()

			# Line continuation escapes are allow
			# build the entire line before proceeding
			if line.endswith('\\'):
				tline = tline + line[:len(line)-1] + ';'
				linecontinue = True
				continue

			if linecontinue == True:
				linecontinue = False
				tline = tline + line
				line = tline
				#print "completeline : ", line
				tline = ''


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
						srcurl = srcurl.replace('.git','')
						srcurl = srcurl.strip()
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
	
	#print srcrev, srcurl, branch
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
			continue
		
		if isgithub(srcurl) >= 0: 
			masterversion = githubversion(srcurl, branch, usr, pwd)
		
			if isuptodate(srcrev, masterversion):
				print 'Up to date : ' + f
			else:
				print 'OUT OF DATE: ' + BB+ f
		




if __name__ == "__main__":
	main()








