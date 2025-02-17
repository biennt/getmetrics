from datetime import datetime
from connection import es
from elasticsearch import helpers
import requests
import json
import time


def get_dnsprofile(device):
    es_index_name = "dnsprofile"

    # sua cai nay khi chay production
    url = "https://" + device['ip'] + httpsport + "/mgmt/tm/ltm/profile/dns/dnsprofile/stats"

    username = device['username']
    password = device['password']

    try:
        response = requests.get(url, auth=(username, password),verify=False,timeout=5)
        api_data = response.json()
        metrics = api_data['entries']["https://localhost/mgmt/tm/ltm/profile/dns/~Common~dnsprofile/stats"]['nestedStats']['entries']

        time_now = datetime.now()
        doc = {
            'timestamp': time_now.strftime('%Y-%m-%dT%H:%M:%S+07:00')
        }

        doc['hostname'] = device['hostname']
        doc['ip'] = device['ip']
        doc['layer'] = device['layer']

        for key in metrics:
            valueobj = metrics[key]
            if valueobj.get('value'):
                doc[key] = valueobj["value"]

        print(doc)
        try:
            res = es.index(index=es_index_name + "-{}".format(time_now.strftime('%Y.%m.%d')), body=doc)
            print("dnsprofile-result: {}".format(res['result']))
        except Exception as e:
            print("Error connecting to Elasticsearch")
            print(e)

    except requests.exceptions.Timeout:
        print("Timed out when connect to {}".format(url))


def get_cachestats(device):
    es_index_name = "cachestats"

    if device['layer'] == "cache":
        url = "https://" + device['ip'] + httpsport + "/mgmt/tm/ltm/dns/cache/transparent/transparent_cache/stats"
    else:
        url = "https://" + device['ip'] + httpsport + "/mgmt/tm/ltm/dns/cache/validating-resolver/validating_resolver_cache/stats"

    username = device['username']
    password = device['password']

    try:
        response = requests.get(url, auth=(username, password),verify=False,timeout=5)
        api_data = response.json()
        if device['layer'] == "cache":
            metrics = api_data['entries']['https://localhost/mgmt/tm/ltm/dns/cache/transparent/~Common~transparent_cache/stats']['nestedStats']['entries']
        else:
            metrics = api_data['entries']['https://localhost/mgmt/tm/ltm/dns/cache/validating-resolver/~Common~validating_resolver_cache/stats']['nestedStats']['entries']

        time_now = datetime.now()
        doc = {
            'timestamp': time_now.strftime('%Y-%m-%dT%H:%M:%S+07:00')
        }
        doc['hostname'] = device['hostname']
        doc['ip'] = device['ip']
        doc['layer'] = device['layer']

        for key in metrics:
            valueobj = metrics[key]
            if valueobj.get('value'):
                doc[key] = str(valueobj['value'])
        print(doc)
        try:
            res = es.index(index=es_index_name + "-{}".format(time_now.strftime('%Y.%m.%d')), body=doc)
            print("cachestats-result: {}".format(res['result']))
        except Exception as e:
            print("Error connecting to Elasticsearch")
            print(e)

    except requests.exceptions.Timeout:
        print("Timed out when connect to {}".format(url))


def get_cpustats(device):
    es_index_name = "cpustats"


    url = "https://" + device['ip'] + httpsport + "/mgmt/tm/sys/cpu/stats"

    username = device['username']
    password = device['password']

    try:
        response = requests.get(url, auth=(username, password),verify=False,timeout=5)
        api_data = response.json()

        cpusockets = api_data['entries']
        totalsocket = len(cpusockets)

        time_now = datetime.now()
        documents = []
        for i in range(0, totalsocket, 1):
            cpusocket = cpusockets["https://localhost/mgmt/tm/sys/cpu/" + str(i) + "/stats"]["nestedStats"]["entries"]["https://localhost/mgmt/tm/sys/cpu/"+ str(i) + "/cpuInfo/stats"]["nestedStats"]["entries"]
            totalcore = len(cpusocket)
            for j in range (0, totalcore, 1):
                cpucore = cpusocket["https://localhost/mgmt/tm/sys/cpu/"+ str(i) + "/cpuInfo/" + str(j) + "/stats"]["nestedStats"]["entries"]
                item = {}
                source = {
                            'timestamp': time_now.strftime('%Y-%m-%dT%H:%M:%S+07:00')
                }
                source['hostname'] = device['hostname']
                source['ip'] = device['ip']
                source['layer'] = device['layer']
                source['socketid'] = i
                source['coreid'] = j
                for key in cpucore:
                    valueobj = cpucore[key]
                    if valueobj.get('value'):
                        source[key] = valueobj['value']

                item["_index"] = es_index_name + "-{}".format(time_now.strftime('%Y.%m.%d'))
                item["_source"] = source
                documents.append(item)
        try:
            response = helpers.bulk(es, documents)
            print("Bulk indexing response:", response)
        except Exception as e:
            print("Error connecting to Elasticsearch")
            print(e)
    except requests.exceptions.Timeout:
        print("Timed out when connect to {}".format(url))


def get_memstats(device):
    es_index_name = "memstats"


    url = "https://" + device['ip'] + httpsport + "/mgmt/tm/sys/memory/stats"

    username = device['username']
    password = device['password']

    try:
        response = requests.get(url, auth=(username, password),verify=False,timeout=3)
        api_data = response.json()
        hostmemstats = api_data['entries']["https://localhost/mgmt/tm/sys/memory/memory-host/stats"]["nestedStats"]["entries"]["https://localhost/mgmt/tm/sys/memory/memory-host/0/stats"]["nestedStats"]["entries"]

        time_now = datetime.now()
        doc = {
            'timestamp': time_now.strftime('%Y-%m-%dT%H:%M:%S+07:00')
        }

        doc['hostname'] = device['hostname']
        doc['ip'] = device['ip']
        doc['layer'] = device['layer']
        for key in hostmemstats:
            valueobj = hostmemstats[key]
            if valueobj.get('value'):
                doc[key] = valueobj['value']
        print(doc)
        try:
            res = es.index(index=es_index_name + "-{}".format(time_now.strftime('%Y.%m.%d')), body=doc)
            print("memstats-result: {}".format(res['result']))
        except Exception as e:
            print("Error connecting to Elasticsearch")
            print(e)
    except requests.exceptions.Timeout:
        print("Timed out when connect to {}".format(url))


def get_lsnstats(device):
    es_index_name = "lsnstats"


    url = "https://" + device['ip'] + httpsport + "/mgmt/tm/ltm/virtual/stats"

    username = device['username']
    password = device['password']

    try:
        response = requests.get(url, auth=(username, password),verify=False,timeout=3)
        api_data = response.json()
        lsnall = api_data['entries']

        for item in lsnall.items():
          tmp = item[1]
          metrics = tmp["nestedStats"]["entries"]
          time_now = datetime.now()
          doc = {
              'timestamp': time_now.strftime('%Y-%m-%dT%H:%M:%S+07:00')
          }
          doc['hostname'] = device['hostname']
          doc['ip'] = device['ip']
          doc['layer'] = device['layer']
          for key in metrics:
            valueobj = metrics[key]
            if valueobj.get('value'):
              doc[key] = valueobj['value']
            if valueobj.get('description'):
              doc[key] = valueobj['description']
          print(json.dumps(doc,indent=2))

    except requests.exceptions.Timeout:
        print("Timed out when connecting to {}".format(url))
        
######################################################

httpsport = ""
#httpsport = ":8443"

interval = 5
f = open('devicelist.json')
devicelist = json.load(f)
while True:
    for device in devicelist['devices']:
        print("--------------------------------------------------------------------------------------------")
        
        print("---- collect statistics from dns profile")
        get_dnsprofile(device)

        print("---- collect statistics from cache profile")
        get_cachestats(device)

        print("---- collect statistics for cpu utilization")
        get_cpustats(device)

        print("---- collect statistics for memory utilization")
        get_memstats(device)
        
        print("--------------------------------------------------------------------------------------------")
    time.sleep(interval)
f.close()

