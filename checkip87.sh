#!/bin/bash
#
 
ip a | grep '10.209.52.87'
 
if [ $? -eq 0 ]
then
  echo "this is active node"
  /home/vt_admin/getmetrics/start_dnsmon.sh
  /home/vt_admin/getmetrics/start_getmetrics.sh
else
  echo "this is standby node"
  /home/vt_admin/getmetrics/stop_dnsmon.sh
  /home/vt_admin/getmetrics/stop_getmetrics.sh
fi
docker ps -a

