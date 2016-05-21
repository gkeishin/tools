#!/usr/bin/python
#################################################################################
# * "THE BEER-WARE LICENSE" (Revision 42):
# * <austenc@us.ibm.com> wrote this file.  As long as you retain this notice you
# * can do whatever you want with this stuff. If we meet some day, and you think
# * this stuff is worth it, you can buy me a beer in return.   Chris Austen
#################################################################################
import sys
import getpass
import getopt
import errlparser
import obmcrequests

loguri = '/org/openbmc/records/events/'

#############################################
# Copied the hexdump function from....
# https://gist.github.com/7h3rAm/5603718
#############################################
def hexdump(src, length=16, sep='.'):
	FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
	lines = []
	for c in xrange(0, len(src), length):
		chars = src[c:c+length]

		hex = ' '.join(["%02x" % x for x in chars])
		if len(hex) > 24:
			hex = "%s %s" % (hex[:24], hex[24:])
		printable = ''.join(["%s" % ((x <= 127 and FILTER[x]) or sep) for x in chars])
		lines.append("%08x:  %-*s  |%s|\n" % (c, length*3, hex, printable))
	print ''.join(lines)


class eventLogDB:
	def __init__(self, connection):
		self.db = {}
		connection.get(loguri)
		events = connection.data()
		for i in events:
			connection.get(i)
			self.addRec(i, connection.data())

	def addRec(self, rec, data):
		self.db[rec] = data

	def delRec(self, num):
		uri = loguri + num
		if uri in self.db: del self.db[uri]

		
	def recExists(self, num):
		uri = loguri + num

		if uri in self.db.keys():
			return True
		else :
			return False

	def keys(self):
		return self.db.keys()


def displayRecordDetails(eldb, num):
	uri = loguri + num

	print '================================================'
	print 'Event Log     ', uri
	print 'Message:      ', eldb.db[uri]['message']
	print 'Time:         ', eldb.db[uri]['time']
	print 'Severity:     ', eldb.db[uri]['severity']
	print 'Reported By:  ', eldb.db[uri]['reported_by']
	print 'Associations: '

	try:
		for i in eldb.db[uri]['associations']:
			print '              ', i[2]
	except:
		pass

	print
	if errlparser.validLog(eldb.db[uri]['debug_data'][16:]) == True:
		errlparser.parserLog(eldb.db[uri]['debug_data'][16:])

	print
	print 'IPMI SEL Data:'
	hexdump(eldb.db[uri]['debug_data'][0:16])

	print 'Debug Data:'
	hexdump(eldb.db[uri]['debug_data'][16:])

	return


def displayDetailMenu(eldb, num):

	option = ''
	while option != 'q': 
		displayRecordDetails(eldb, num)
		
		print '-----------------------------------'
		s =  'Options: d (delete), q (back) >> '
		option = raw_input(s)
		

		if option == 'd':
			print 'wanted to delete'
			eldb.delRec(num)
			option = 'q'


def displayRecordsMenu(eldb):
	
	print
	print '============================================================================'
	print '{0:4}  {1:22}  {2:22}  {3}'.format('Log#', 'Severity','Date','Message')

	for i in eldb.db:
		num = i.replace('/org/openbmc/records/events/','')
		print '{0:4}  {1:22}  {2:22}  {3}'.format(num, eldb.db[i]['severity'],eldb.db[i]['time'],eldb.db[i]['message'])

	print '--------------------------------------------------------'
	s =   'Options: # (details),  a (All details), q (quit)  >> '
	response = raw_input(s)

	return response


def runtool(ip, uname, pswd, cache):

	e  = obmcrequests.obmcConnection(ip, uname, pswd, cache)
	el = eventLogDB(e)
	
	option = ''
	
	while option != 'q':
	
		option = displayRecordsMenu(el)

		if option == 'a':
			for i in el.keys():
				s = i.replace(loguri, '')
				displayRecordDetails(el, s)

		if el.recExists(option):
			displayDetailMenu(el, option)


def usage():
	name = 'errl.py'
	print 'Usage: Version 0.2'  
	print name, '[-i] [-u] <-p> <-c dir>'
	print '\t-i | --ip=        : IP / Hostname of the target BMC'
	print '\t-u | --user=      : user name for REST interaction'
	print '\t-p | --password=  : password for REST interaction'
	print '\t-c | --cachedir=  : Cache REST interaction directory'


def main(argv):

	cache  = ''
	pswd 	= ''
	ip 		= ''
	uname 	= ''

	try:
		opts, args = getopt.getopt(argv,"hc:d:u:p:i:",["ip=","user=","password=","cachedir"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit()
		elif opt in ("-i", "--ip"):
			ip = arg
		elif opt in ("-u", "--user"):
			uname = arg
		elif opt in ("-p", "--password"):
			pswd = arg
		elif opt in ("-c", "--cachedir"):
			cache = arg

	if ip == '' or uname == '':
		usage()
		print 'ERROR: ip and user parmeters are required'
		sys.exit(2)

	if pswd == '':
		pswd = getpass.getpass('Password:')

	runtool(ip, uname, pswd, cache)

if __name__ == "__main__":
   main(sys.argv[1:])
