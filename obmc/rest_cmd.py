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

def rest_call(host, option, uri, uname, password, parm=None):
    e  = obmcrequests.obmcConnection(host, uname, password)
    if option =="GET":
        print "Executing: %s  %s"% (option, uri)
        e.get(uri)
        print "\n",uri
        msg = e.data()
        json_pretty_format(msg)
    if option =="PUT":
        print "Executing: %s  %s %s"% (option, uri, parm)
        e.put(uri,parm)
    if option =="poweron":
        host_poweron(e)
    if option =="poweroff":
        host_poweroff(e)
    if option =="reboot":
        reboot_bmc(e)
    if option =="host":
        host_state(e)
    if option =="chassis":
        chassis_power(e)
    if option =="bmc":
        bmc_state(e)
    if option =="state":
        bmc_state(e)
        chassis_power(e)
        host_state(e)

def host_poweron(e):
    print "Powering On"
    host = '/xyz/openbmc_project/state/host0/'
    uri = host + 'attr/RequestedHostTransition'
    parm = 'xyz.openbmc_project.State.Host.Transition.On'
    e.put(uri,parm)

def host_poweroff(e):
    print "Powering Off"
    host = '/xyz/openbmc_project/state/host0/'
    uri = host + 'attr/RequestedHostTransition'
    parm = 'xyz.openbmc_project.State.Host.Transition.Off'
    e.put(uri,parm)

def reboot_bmc(e):
    print "Rebooting BMC"
    host = '/xyz/openbmc_project/state/bmc0/'
    uri = host + 'attr/RequestedBMCTransition'
    parm = 'xyz.openbmc_project.State.BMC.Transition.Reboot'
    e.put(uri,parm)

def host_state(e):
    host = '/xyz/openbmc_project/state/host0/'
    uri = host + 'attr/CurrentHostState'
    e.get(uri)
    msg = e.data()
    print '\nHost state:',msg.rsplit('.', 1)[1]

def chassis_power(e):
    chassis = '/xyz/openbmc_project/state/chassis0/'
    uri = chassis + 'attr/CurrentPowerState'
    e.get(uri)
    msg = e.data()
    print '\nChassis Power state:',msg.rsplit('.', 1)[1]

def bmc_state(e):
    chassis = '/xyz/openbmc_project/state/bmc0/'
    uri = chassis + 'attr/CurrentBMCState'
    e.get(uri)
    msg = e.data()
    print '\nBMC state:',msg.rsplit('.', 1)[1]

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
    print name, '-i <Host> -o <GET/PUT> -u <URL path> -p <parmeters>'
    print '\t-i | --host=   : Host IP'
    print '\t-o | --option= : GET/POST simple REST request'
    print '\t-u | --URL=    : URI path of the REST object'
    print '\t-p | --parm=   : parameter'
    print '\n\t --------------------------------------------------------------'
    print '\t *** Example ***:'
    print '\t *** Short cut command for state/on/off/reboot ***:'
    print '\t --------------------------------------------------------------'
    print '\t Get System state(BMC/Chassis/Host):'
    print '\t rest_cmd  -i xx.xx.xx.xx -o state'
    print '\t Poweron System:'
    print '\t rest_cmd  -i xx.xx.xx.xx -o poweron'
    print '\t Poweroff System:'
    print '\t rest_cmd  -i xx.xx.xx.xx -o poweroff'
    print '\t Reboot BMC:'
    print '\t rest_cmd  -i xx.xx.xx.xx -o reboot'
    print '\t --------------------------------------------------------------'
    print '\t Get Host State:'
    print '\t rest_cmd  -i xx.xx.xx.xx -o host'
    print '\t Get Chassis power State:'
    print '\t rest_cmd  -i xx.xx.xx.xx -o chassis'
    print '\t Get BMC State:'
    print '\t rest_cmd  -i xx.xx.xx.xx -o bmc'
    print '\t --------------------------------------------------------------'
    print '\t BMC GET:'
    print '\t rest_cmd  -i xx.xx.xx.xx -o GET -u /xyz/openbmc_project/'
    print '\t BMC enumerate:'
    print '\t rest_cmd  -i xx.xx.xx.xx -o GET -u /xyz/openbmc_project/enumerate'
    print '\t --------------------------------------------------------------'
    print '\t *** You can use it with URL for other interfaces ****:'
    print '\t --------------------------------------------------------------'
    print '\t Host Power On:'
    print '\t rest_cmd  -i xx.xx.xx.xx -o PUT -u /xyz/openbmc_project/state/host0/attr/RequestedHostTransition -p xyz.openbmc_project.State.Host.Transition.On'
    print '\t ----------------------------------------------------------------'
    sys.exit()


def main(argv):

    uname = 'root'
    password = '0penBmc'
    host = ''
    option = ''
    uri = ''
    parm = ''
    try:
                opts, args = getopt.getopt(argv, "h:i:o:u:p:", ["host=", "option=", "URI=", "parm=",])
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
        elif opt in ("-p", "--parm"):
            parm = arg

    if host == '':
        usage()

    if option == 'state':
        rest_call(host, option, uri, uname, password, parm)
        sys.exit()

    if option == 'poweron':
        rest_call(host, option, uri, uname, password, parm)
        sys.exit()

    if option == 'poweroff':
        rest_call(host, option, uri, uname, password, parm)
        sys.exit()

    if option == 'reboot':
        rest_call(host, option, uri, uname, password, parm)
        sys.exit()

    if option == 'host':
        rest_call(host, option, uri, uname, password, parm)
        sys.exit()

    if option == 'chassis':
        rest_call(host, option, uri, uname, password, parm)
        sys.exit()

    if option == 'bmc':
        rest_call(host, option, uri, uname, password, parm)
        sys.exit()

    if option == '':
        usage()

    if uri == '':
        usage()

    rest_call(host, option, uri, uname, password, parm)

if __name__ == "__main__":
    main(sys.argv[1:])
