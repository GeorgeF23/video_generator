from dataclasses import asdict
import hashlib
import logging
import os
import pdb
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError


class ElasticSearchClient:
    """ Singleton class used as an interface between the application and elasticsearch
    """
    instance = None
    
    def __init__(self):
        self.elastic_host = os.environ.get('ELASTIC_HOST')
        self.es_client = Elasticsearch(self.elastic_host)

    @staticmethod
    def get_instance():
        """ Returns an instance of this class
        """
        if ElasticSearchClient.instance is None:
            ElasticSearchClient.instance = ElasticSearchClient()
        
        return ElasticSearchClient.instance

    def upload(self, data, id, index_name):
        """ Uploads a single document to elasticsearch

            * data -> object that will be uploaded
            * id -> function that returns the id of the object. Signature: id(data: object) -> the id
            * index_name -> destination index
        """
        if type(data) is not list:
            data = [data]
        
        for d in data:
            self.es_client.index(index=index_name, id=id(d), body=asdict(d))
        
        self.es_client.indices.refresh(index_name)

    def get_by_id(self, id, index_name):
        """ Fetches an object by it's id

            * id -> id of object to fetch
            * index_name -> index

            Returns: found object or None
        """
        try:
            document = self.es_client.get(index_name, id)
            return document['_source']
        except NotFoundError:
            logging.error(f'Document with id: {id} does not exist in index {index_name}')
            return None
        except Exception as e:
            logging.error(f'Unknown error while searching in ES: {e}')
        