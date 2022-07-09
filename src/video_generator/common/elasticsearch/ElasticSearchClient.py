from dataclasses import asdict
import hashlib
import os
import pdb
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
            self.es_client.index(index=index_name, id=id(d), body=asdict(d))
        
        self.es_client.indices.refresh(index_name)