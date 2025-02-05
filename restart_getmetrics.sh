#!/bin/sh

echo "stopping getmetrics-cache"
docker stop getmetrics-cache

echo "removing getmetrics-cache"
docker rm getmetrics-cache

echo "starting getmetrics-cache"
docker run -d --name getmetrics-cache \
-v /u01/getmetrics/caches/devicelist.json:/usr/src/app/devicelist.json \
-v /u01/getmetrics/connection.py:/usr/src/app/connection.py \
-v /u01/getmetrics/getmetrics-build/getmetrics.py:/usr/src/app/getmetrics.py \
--log-driver=local --log-opt max-size=10m --log-opt max-file=3 \
--restart unless-stopped getmetrics

echo "stopping getmetrics-resolver"
docker stop getmetrics-resolver

echo "removing getmetrics-resolver"
docker rm getmetrics-resolver

echo "starting getmetrics-resolver"
docker run -d --name getmetrics-resolver \
-v /u01/getmetrics/resolvers/devicelist.json:/usr/src/app/devicelist.json \
-v /u01/getmetrics/connection.py:/usr/src/app/connection.py \
-v /u01/getmetrics/getmetrics-build/getmetrics.py:/usr/src/app/getmetrics.py \
--log-driver=local --log-opt max-size=10m --log-opt max-file=3 \
--restart unless-stopped getmetrics

