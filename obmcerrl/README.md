Log parsers for interacting with an OpenBMC server

Usage Examples

	errl.py -i 9.3.x.x -u root -c /tmp

	The errl.py tool will connect over REST to a BMC and collect all the event logs
	You then get the option to display the details.  By adding the -c <dir> you get 
	to cache the data so the next time you run the command it will skip the https 
	traffic and use a local copy.  The cache option will collect from the REST source
	correctly if the file didn't exist yet.  I you want to erase the cached data simply
	delete all the files that start with the ip address in the directory pointed to 
	by the -c option.  If you do not add the password in the cli the script will
	prompt you


	errlparser.py -i ~/errl.20

	This takes a binary file what is an error log stored in binay file.  The log 
	must follow the epapr (http://openpowerfoundation.org/?resource_lib=linux-on-power-architecture-platform-reference) and prints out interesting information.  The functions in
	this file are used by errl.py

