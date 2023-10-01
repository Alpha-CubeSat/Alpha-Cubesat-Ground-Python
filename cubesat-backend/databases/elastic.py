import datetime

from elasticsearch import Elasticsearch

import config


# Makes a connection to an Elasticsearch database based on configured host, port, and options
def get_connection() -> Elasticsearch:
    cfg = config.elastic_config
    es = Elasticsearch('https://localhost:9200',
                       basic_auth=(cfg['username'], cfg['password']), ca_certs=cfg['certs'])
    return es

# Appends the current year, month, and day to the supplied index name 
# to break up an index into a daily index pattern.
def daily_index_strategy(name):
    today = datetime.date.today()
    time = str(today.year) + '.' + str(today.month) + '.' + str(today.day)
    return name + '-' + time

# Indexes the supplied document into elasticsearch, using the
# naming strategy to create indices using the given index name.
def index(index_base_name: str, content: dict):
    es = get_connection()
    es.index(index=index_base_name, body=content)

# Returns the data corresponding to the supplied index and a list of input fields
def get_es_data(idx: str, cols: list, query: dict = None) -> list:
    result = []
    if not query:
        query = {"match_all": {}}
    response = get_connection().search(
        index=idx,
        source=cols,
        query=query
    )
    for hit in response['hits']['hits']:
        result.append(hit['_source'])
    return result

