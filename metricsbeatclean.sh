#!/bin/bash
#curl -k -u elastic:Vietteldns -XGET https://10.221.8.71:9200/_cat/indices > index_list.txt
cat index_list.txt  | grep dnsprofile| tr -s ' ' | cut -d ' ' -f 3

