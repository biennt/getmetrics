#!/bin/sh
echo "starting getmetrics-cache"
docker start getmetrics-cache
echo "starting getmetrics-resolver"
docker start getmetrics-resolver

