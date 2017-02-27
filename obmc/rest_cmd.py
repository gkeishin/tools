#!/usr/bin/python
import sys
import os
import getopt
import requests
import json
import logging
import warnings
import httplib
import obmcrequests

warnings.filterwarnings("ignore")

def rest_call(host, option, uri, uname, password):
    e  = obmcrequests.obmcConnection(host, uname, password)
    if option =="GET":
        print "Executing: %s  %s"% (option, uri)
        e.get(uri)
        print "\n",uri
        msg = e.data()
        json_pretty_format(msg)

########################################################################
#   @brief    Print the JSON data pretty format to Console
#   @param    response: @type json: JSON response data
#   @return   None
########################################################################
def json_pretty_format(response):
    print json.dumps(response, indent=4)

def usage():
    name = 'cmd'
    print 'Usage: '
    print name, '-i <Host> -o <GET/POST> -u <URL path>'
    print '\t-i | --host=   : Host IP'
    print '\t-o | --option= : GET/POST simple REST request'
    print '\t-u | --URL=    : URI path of the REST object'
    sys.exit()


def main(argv):

    host = ''
    option = ''
    uri = ''
    try:
        opts, args = getopt.getopt(argv, "h:i:o:u:", ["host=", "option=", "URI="])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-i", "--host"):
            host = arg
        elif opt in ("-o", "--option"):
            option = arg
        elif opt in ("-u", "--uri"):
            uri = arg

    if host == '':
        usage()

    if option == '':
        usage()

    if uri == '':
        usage()

    uname = 'root'
    password = '0penBmc'
    rest_call(host, option, uri, uname, password)

if __name__ == "__main__":
    main(sys.argv[1:])
