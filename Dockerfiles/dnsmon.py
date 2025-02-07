from datetime import datetime
from connection import es
import json
import time
import dns.resolver
import sys

def dnsmon_check(device,domain):
    status = "down"
    rrset = ""
    restime = 0
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = [device["ip"]]
    dns.resolver.default_resolver.timeout = 3
    retry = 3
    while (status == "down") and (retry > 0):
      try:
        r = dns.resolver.resolve(domain["name"],domain["type"])
        rrset = r.rrset
        restime = round(r.response.time * 1000000)
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
    print("-- {} type {} on {}: result is \"{}\", status is {}, response time is {}".format(domain["name"],domain["type"],device["ip"],rrset,status,restime))
    result = {
       'status': status,
       'response_time': restime,
       'rrset': rrset
    }
    return result

######################################################

interval = 1
f = open('listenerlist.json')
d = open('domainlist.json')
devicelist = json.load(f)
domainlist = json.load(d)
es_index_name = "dnsmon"
while True:
    for device in devicelist['devices']:
        print("Checking {} ..".format(device['ip']))
        for domain in domainlist['domains']:
          time.sleep(interval)
          result = dnsmon_check(device,domain)
          time_now = datetime.now()
          doc = {
            'timestamp': time_now.strftime('%Y-%m-%dT%H:%M:%S+07:00')
          }
          doc['hostname'] = device['hostname']
          doc['ip'] = device['ip']
          doc['prober'] = device['prober']
          doc['query'] = domain["name"] + ' ' + domain["type"]
          doc['status'] = result['status']
          doc['response_time'] = result['response_time']
          doc['rrset'] = str(result['rrset'])
          res = es.index(index=es_index_name + "-{}".format(time_now.strftime('%Y.%m.%d')), document=doc)
          print("{} updating to elastic server: {}".format(doc['timestamp'], res['result']))
        print("----------------------------------------")
f.close()
d.close()
