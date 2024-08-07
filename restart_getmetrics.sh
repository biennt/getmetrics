#!/bin/sh
echo "starting getmetrics-cache"
docker stop getmetrics-cache
docker rm getmetrics-cache
docker run -d --name getmetrics-cache -v /home/admin/getmetrics/caches/devicelist.json:/usr/src/app/devicelist.json -v /home/admin/getmetrics/connection.py:/usr/src/app/connection.py --restart unless-stopped getmetrics

echo "starting getmetrics-resolver"
docker stop getmetrics-resolver
docker rm getmetrics-resolver
docker run -d --name getmetrics-resolver -v /home/admin/getmetrics/resolvers/devicelist.json:/usr/src/app/devicelist.json -v /home/admin/getmetrics/connection.py:/usr/src/app/connection.py --restart unless-stopped getmetrics

