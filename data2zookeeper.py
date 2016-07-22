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

#loop excuted
while True:
    zk.start() #create connection to zookeeper_serser

    if zk.exists(hostpath):
        for host, ip in hostsinfo.items():
            zk.set(hostpath + "/" + host, ip)
    else:
        zk.ensure_path(hostpath)
        for host, ip in hostsinfo.items():
            zk.create(hostpath + "/" + host, hostsinfo.get(host))
    zk.stop()
    time.sleep(10)
