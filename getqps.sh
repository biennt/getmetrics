#!/bin/bash
# Bien <bien.nguyen@f5.com>

cd /home/ubuntu/getqps
port="8443"
cred='admin:abcxyz'
rm -f esfile.ndjson
today=`date '+%Y-%m-%d'`
index_name="qps-$today"
b64cred=`echo -n $cred | base64`
authheader="Authorization: Basic $b64cred"

if ! [ -f cachelist ]; then
  echo "cachelist file does not exist."
  exit 1
fi

function get_vs() {
  baseurl=$1
  url="$baseurl/mgmt/tm/gtm/listener"
  curl -s -k -H "$authheader" "$url" | jq > output.txt
  listofvs=`cat output.txt | grep "\"selfLink\"" | grep "Common" | cut -d ":" -f 3 | cut -c 12-200 | cut -d '?' -f 1`
}

function get_metrics() {
  vsbaseurl=$1
  ipaddr=$2
  vsname=`echo $vsbaseurl | cut -d '~' -f 3`
  vsstaturl="$vsbaseurl/stats"
  lastfile=`echo $vsbaseurl | md5sum | cut -c 1-32`
  if ! [ -f $lastfile ]; then
    lastreq=0
  else
    lastreq=`cat $lastfile`
  fi
  curreq=`curl -s -k -H "$authheader" "$vsstaturl" | jq | grep -A 1 totRequests | grep value | cut -d ':' -f 2`
  if [ $curreq -gt $lastreq ]; then
    q=`expr $curreq - $lastreq`
    qps=`expr $q / 60`
  else
    qps=0
  fi
  echo -n $curreq > $lastfile
  echo "{ \"index\": { \"_index\": \"$index_name\" }}" >> esfile.ndjson
  ts=`date -u +"%Y-%m-%dT%H:%M:%SZ"`
  echo "{ \"timestamp\": \"$ts\", \"ip\": \"$ipaddr\", \"hostname\": \"$hostname\", \"layer\": \"$layer\", \"dc\": \"$dc\", \"region\": \"$region\", \"vsname\": \"$vsname\", \"qps\": \"$qps\" }"  >> esfile.ndjson
  totalqps=`expr $totalqps + $qps`
}

listofcache=`cat cachelist`
for device in $listofcache; do
  ipaddr=`echo $device | cut -d ',' -f 1`
  layer=`echo $device | cut -d ',' -f 2`
  hostname=`echo $device | cut -d ',' -f 3`
  dc=`echo $device | cut -d ',' -f 4`
  region=`echo $device | cut -d ',' -f 5`
  baseurl="https://$ipaddr:$port"
  listofvs=""
  totalqps=0
  get_vs $baseurl
  for vs in $listofvs; do
    vsbaseurl="$baseurl$vs"
    get_metrics $vsbaseurl $ipaddr
  done
  echo "{ \"index\": { \"_index\": \"$index_name\" }}" >> esfile.ndjson
  ts=`date -u +"%Y-%m-%dT%H:%M:%SZ"`
  echo "{ \"timestamp\": \"$ts\", \"ip\": \"$ipaddr\", \"hostname\": \"$hostname\", \"layer\": \"$layer\", \"dc\": \"$dc\", \"region\": \"$region\", \"vsname\": \"all\", \"qps\": \"$totalqps\" }" >> esfile.ndjson
done

#### update to ES #### 
cat esfile.ndjson
curl -H 'Content-Type: application/x-ndjson' -XPOST -k -u 'elastic:abc123' 'https://localhost:9200/_bulk' --data-binary @esfile.ndjson
