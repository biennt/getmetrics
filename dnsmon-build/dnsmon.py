from datetime import datetime
from connection import es
import json
import time
import dns.resolver
import sys

def dnsmon_check(device,domain):
    status = "down"
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = [device["ip"]]
    dns.resolver.default_resolver.timeout = 3
    retry = 3
    while (status == "down") and (retry > 0):
      try:
        r = dns.resolver.resolve(domain["name"],domain["type"])
        status = "up"
      except dns.exception.Timeout:
        status = "Timeout"
      except dns.exception.UnexpectedEnd:
        status = "UnexpectedEnd"
      except dns.resolver.NoAnswer:
        status = "NoAnswer"
      except dns.resolver.NoNameservers:
        status = "NoNameServers/ServFail"
      except dns.resolver.NXDOMAIN:
        status = "NXDomain"
      retry = retry - 1
    print("checking {} type {} on {}, result is {}".format(domain["name"],domain["type"],device["ip"],status))
    if status == "up":
      return True
    else:
      return False

######################################################

interval = 1
f = open('listenerlist.json')
d = open('domainlist.json')
devicelist = json.load(f)
domainlist = json.load(d)
es_index_name = "dnsmon"

while True:
    for device in devicelist['devices']:
        upcheck = 0
        time_now = datetime.now()
        doc = {
          'timestamp': time_now.strftime('%Y-%m-%dT%H:%M:%S+07:00')
        }
        doc['hostname'] = device['hostname']
        doc['ip'] = device['ip']
        doc['layer'] = device['layer']

        for domain in domainlist['domains']:
            doc[domain['name']] = "down"
            if dnsmon_check(device,domain):
                doc[domain['name']] = "up"
                upcheck = upcheck + 1
        print("-- {} -- {}".format(device['ip'],upcheck))
        doc['upcheck'] = upcheck
        res = es.index(index=es_index_name + "-{}".format(time_now.strftime('%Y.%m.%d')), body=doc)
        print("dnsmon-result: {}".format(res['result']))
    time.sleep(interval)

f.close()
d.close()
