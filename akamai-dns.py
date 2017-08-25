#!/usr/local/bin/env python2.7
###This program used to update fastDns recordset in akamai luna controller#####
### Devloped by Ankit Kashyap ########

import requests, sys
import argparse
from akamai.edgegrid import EdgeGridAuth,EdgeRc
from urlparse import urljoin
import json

#################

####################################################
###### Variable #######
section_name="dns"
domain = "payugur.com"
###################### Authentication & Authorization ###############
edgerc = EdgeRc('.edgerc')
baseurl = 'https://%s' %edgerc.get(section_name, 'host')
#####################################################################
#################
s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, section_name)
result = s.get(urljoin(baseurl, '/config-dns/v1/zones/%s' %domain))
#####################################################################
####################################
def aws_to_nm():
    res = json.loads(result.text)
    print "Actual Response\n\n"
    print res
    serial = res['zone']['soa']['serial']
    serial = int(serial) + 1
    res['zone']['soa']['serial'] = serial

    Item1 = {u'active': True, u'ttl': 60, u'target': u'secure-loadtesting-1616539340.ap-south-1.elb.amazonaws.com.', u'name': u'securetest'}
    Item = {u'active': True, u'target': u'180.179.169.103', u'name': u'securetest', u'ttl': 60}
    List = res['zone']['a']
    if Item in List:
       ItemNumber=List.index(Item)
       print('Bye')
       exit()
       print('hello!')
    else:
       List.append(Item)
       res['zone']['cname'].remove(Item1)
       ItemNumber=List.index(Item)
       res['zone']['a'].append(Item)
    print "\n\nNew Request\n\n"
    print res
    headers = {'Content-Type': 'application/json'}
    newresult = s.post('https://akab-j7qftn2nkgreeeed-3b7l3odsfbxh4fps.luna.akamaiapis.net/config-dns/v1/zones/%s' % domain, data =json.dumps(res), headers=headers)
    print "\n\n New Response after Modification\n\n"
    print newresult.text
def nm_to_aws():
    res = json.loads(result.text)
    print "Actual Response\n\n"
    print res
    serial = res['zone']['soa']['serial']
    serial = int(serial) + 1
    res['zone']['soa']['serial'] = serial
    Item1 = {u'active': True, u'target': u'180.179.169.103', u'name': u'securetest', u'ttl': 60}
    Item = {u'active': True, u'ttl': 60, u'target': u'secure-loadtesting-1616539340.ap-south-1.elb.amazonaws.com.', u'name': u'securetest'}
    List = res['zone']['cname']
    if Item in List:
       ItemNumber=List.index(Item)
       print('Bye')
       exit()
       print('hello!')
    else:
       List.append(Item)
       res['zone']['a'].remove(Item1)
       ItemNumber=List.index(Item)
       print "\n\nNew Request\n\n"
       print res
       headers = {'Content-Type': 'application/json'}
       newresult = s.post('https://akab-j7qftn2nkgreeeed-3b7l3odsfbxh4fps.luna.akamaiapis.net/config-dns/v1/zones/%s' %domain, data =json.dumps(res), headers=headers)
       print "\n\n New Response after Modification\n\n"
       print newresult.text
def get_info():
    res = json.loads(result.text)
    print "Actual Response\n\n"
    print res

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
parser_foo = subparsers.add_parser('get_info')
parser_foo.set_defaults(func=get_info)
parser_foo = subparsers.add_parser('aws_to_nm')
parser_foo.set_defaults(func=aws_to_nm)
parser_foo = subparsers.add_parser('nm_to_aws')
parser_foo.set_defaults(func=nm_to_aws)
args = parser.parse_args()
args.func()
