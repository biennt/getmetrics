# getmetrics
collecting metrics from f5 big-ip via icontrol rest and put into elasticsearchs

# Build containers

```
cd getmetrics-build
docker build -t getmetrics .
cd ..
```

```
cd dnsmon-build
docker build -t dnsmon .
cd ..
```

# Run the containers

Prepare `devicelist.json` and `connection.py`

```
docker run -d --name getmetrics-cache \
 -v /home/vt_admin/getmetrics/caches/devicelist.json:/usr/src/app/devicelist.json \
 -v /home/vt_admin/getmetrics/connection.py:/usr/src/app/connection.py \
 --restart unless-stopped getmetrics
```

Prepare `listenerlist.json`, `domainlist.json`, and  `connection.py`

```
docker run -d --name dnsmon \
 -v /home/vt_admin/getmetrics/listenerlist.json:/usr/src/app/listenerlist.json \
 -v /home/vt_admin/getmetrics/domainlist.json:/usr/src/app/domainlist.json \
 -v /home/vt_admin/getmetrics/connection.py:/usr/src/app/connection.py \
 --restart unless-stopped dnsmon
 ```

# Create crontab entries
Install and configure keepalived, create a crontab entries to run checkip87.sh every minute

Modify `checkip87.sh` to fit your environment
