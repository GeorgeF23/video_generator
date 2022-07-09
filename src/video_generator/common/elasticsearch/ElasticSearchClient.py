from dataclasses import asdict
import hashlib
import os
from elasticsearch import Elasticsearch

class ElasticSearchClient:
    
    instance = None
    
    def __init__(self):
        self.elastic_host = os.environ.get('ELASTIC_HOST')
        self.es_client = Elasticsearch(self.elastic_host)

    @staticmethod
    def get_instance():
        if ElasticSearchClient.instance is None:
            ElasticSearchClient.instance = ElasticSearchClient()
        
        return ElasticSearchClient.instance

    def upload(self, data, id, index_name):
        if type(data) is not list:
            data = [data]
        
        for d in data:
            d_id = id(d)

            self.es_client.index(index=index_name, id=hashlib.md5(d_id.encode()).hexdigest(), body=asdict(d))
        
        self.es_client.indices.refresh(index_name)