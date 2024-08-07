#!/bin/bash
#
 
ip a | grep '10.10.10.87'
 
if [ $? -eq 0 ]
then
  echo "this is active node"
  /home/admin/getmetrics/start_dnsmon.sh
  /home/admin/getmetrics/start_getmetrics.sh
else
  echo "this is standby node"
  /home/admin/getmetrics/stop_dnsmon.sh
  /home/admin/getmetrics/stop_getmetrics.sh
fi
docker ps -a

