#!/usr/bin/python
#################################################################################
# * "THE BEER-WARE LICENSE" (Revision 42):
# * <austenc@us.ibm.com> wrote this file.  As long as you retain this notice you
# * can do whatever you want with this stuff. If we meet some day, and you think
# * this stuff is worth it, you can buy me a beer in return.   Chris Austen
#################################################################################
import sys, getopt
import struct

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



class event_log:
	def __init__(self, bytes):
		self.b       = bytes
		self.index   = 0
		self.section = 0
		self.section_len = 0
		self.size    = len(bytes)

	
################################################################
# next_section
#	Returns True|False : if there is a valid section
#
#   Advances to the next major section in the error log.  This 
#   function should be called after the class has been initialized 
# 
################################################################
	def next_section(self):
		if (self.section_len+self.section) >= self.size:
			return False

		# Set the section offset to the start of the new section
		self.section  = self.section + self.section_len

		seclen = struct.unpack(">H", ''.join([chr(x) for x in self.b[self.section+2:self.section+4]]))[0]

		if self.section_len == 0:
			self.section     = 0			
			self.section_len = seclen
		else:
			self.section_len = seclen

		# I've seen a log that had a bunch of
		# zeros at the end of the log.  That caused
		# looping because it would have reset the 
		# pointers back to the beginning of the log
		if self.section_len == 0:
			print 'WARNING: LOG CORRUPTION DETECTED, FOUND AN INVALID SECTION'
			return False

		return True


	def print_section_header(self):
		seclen = struct.unpack(">H", ''.join([chr(x) for x in self.b[self.section+2:self.section+4]]))[0]
		secid = ''.join(chr(x) for x in self.b[self.section+0:self.section+2])
		
		# I have support for the PS section for now.  Over time more can be added
		if secid == 'PS':
			print_section_header_ps(self.b[self.section+0:self.section+seclen])



def print_section_header_ps(bytes):

		secid, seclen, secver, secsub, seccc = struct.unpack(">HHBBH", ''.join([chr(x) for x in bytes[0:8]]))

		w2, w3, w4, w5, w6, w7, w8, w9 = struct.unpack(">8L", ''.join([chr(x) for x in bytes[0x10:0x30]]))

		refcode = ''.join(chr(x) for x in bytes[0x30:0x50])
		print 'Extended Refernce Codes:  ', refcode
		print '0x{:08x}  0x{:08x}  0x{:08x}  0x{:08x}'.format(w2, w3, w4, w5)
		print '0x{:08x}  0x{:08x}  0x{:08x}  0x{:08x}'.format(w6, w7, w8, w9)


def parserLog(bytes):

	el = event_log(bytes)

	while el.next_section():
		el.print_section_header()


def loadlog(fn):
	raw = []

	f = open(fn, "rb")
	try:
		for byte in bytearray(f.read()):
			raw.append(byte)
	finally:
		f.close()	

	return raw

################################################################
# Various checks to see if a byte stream can really be parsed
################################################################
def validLog(bytes):

	if len(bytes) == 0:
		return False

	hdr = ''.join(chr(x) for x in bytes[0:2])

	if hdr != 'PH':
		return False

	return True


def usage():
	print 'test.py -i <inputfile>'
	print 'The input file for testing needs to be a binary version of an errorlog'


def main(argv):

	inputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:",["ifile="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg

	if inputfile == '':
		usage()
		sys.exit(2)

	bytes = loadlog(inputfile)

	if validLog(bytes) == True:
		parserLog(bytes)
	else:
		print inputfile , 'is not a valid event log'
		sys.exit(2)



if __name__ == "__main__":
   main(sys.argv[1:])
