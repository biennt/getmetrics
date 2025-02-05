#!/bin/sh
echo "stopping dnsmon"
docker stop dnsmon
echo "removing dnsmon"
docker rm dnsmon

echo "starting dnsmon"
docker run -d --name dnsmon \
 -v /u01/getmetrics/listenerlist.json:/usr/src/app/listenerlist.json \
 -v /u01/getmetrics/domainlist.json:/usr/src/app/domainlist.json \
 -v /u01/getmetrics/connection.py:/usr/src/app/connection.py \
 -v /u01/getmetrics/dnsmon-build/dnsmon.py:/usr/src/app/dnsmon.py \
 --log-driver=local --log-opt max-size=10m --log-opt max-file=3 \
 --restart unless-stopped dnsmon

