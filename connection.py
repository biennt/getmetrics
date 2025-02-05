from elasticsearch import Elasticsearch
import urllib3

# Suppress warnings if SSL certificates are self-signed or otherwise not trusted
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define the connection details
es = Elasticsearch(
        [ "https://10.221.8.71:9200", "https://10.221.8.75:9200", "https://10.221.8.79:9200" ],
    basic_auth=("elastic", "Vietteldns"),
    #api_key=("lckZzpABKi7uA5SjBOP8", "kfD3JUEJStyCg7yYjOCqwg"),
    verify_certs=False  # Set to True if you have valid SSL certificates
)

# Test the connection
try:
    es.info()
except Exception as e:
    print("Error connecting to Elasticsearch")
    print(e)

