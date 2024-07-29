from elasticsearch import Elasticsearch
import urllib3

# Suppress warnings if SSL certificates are self-signed or otherwise not trusted
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define the connection details
es = Elasticsearch(
    ["https://10.209.52.71:9200", "https://10.209.52.75:9200", "https://10.209.52.79:9200"],
    basic_auth=("elastic", "change_me"),
    #api_key=("change_me", "change_me"),
    verify_certs=False 
)

# Test the connection
try:
    es.info()
except Exception as e:
    print("Error connecting to Elasticsearch")
    print(e)

