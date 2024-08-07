#!/bin/sh
echo "starting dnsmon"
docker stop dnsmon
docker rm dnsmon
docker run -d --name dnsmon \
 -v /home/admin/getmetrics/listenerlist.json:/usr/src/app/listenerlist.json \
 -v /home/admin/getmetrics/domainlist.json:/usr/src/app/domainlist.json \
 -v /home/admin/getmetrics/connection.py:/usr/src/app/connection.py \
 --restart unless-stopped dnsmon

