# __author__ = 'jtxiao'

#!/usr/bin/env python
#
# zookeeper storage hostname
#
# date 2014-8-12
#

import os
import time
from kazoo.client import KazooClient

#define hostinfo dict
hostsinfo = dict(host=os.popen('hostname').read().strip('\n'), ip=os.popen(
    'ifconfig |grep -A 1 eth |grep inet |tr -s " "|cut -d ":" -f2 |cut -d " " -f 1').read().strip('\n'))
#define kazoo path to create data
hostpath = "/hostsinfo/"+os.popen('hostname').read().strip('\n')
#hostsinfo = {host: os.popen('hostname').readline(),
#             'ip': os.popen('ifconfig |grep -A 1 eth |grep inet |tr -s " "|cut -d ":" -f2 |cut -d " " -f 1').readline()}

#connectString for zookeeper server
zk = KazooClient(hosts=hostsinfo.get('ip') + ":2181")

#excute watch
while True:
    zk.start() #create connection to zookeeper_serser

    if zk.exists(hostpath):
        data,stat = zk.get(hostpath+"/ip")
        print("Version: %s,data: %s" % (stat.version,data.decode('utf-8')))
    else:
        print("No this host information in zookeeper server.")
    zk.stop()
    time.sleep(10)
