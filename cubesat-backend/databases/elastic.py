import datetime

from elasticsearch import Elasticsearch


# Makes a connection to an Elasticsearch database based on
# configured host, port, and options
def get_connection() -> Elasticsearch:
    # config = cfg.get_config()
    # auth = config['database']['elasticsearch']['conn-config']['basic-auth']
    # es = Elasticsearch('https://localhost:9200', basic_auth=auth, ca_certs = 'http_ca.crt')
    return Elasticsearch('http://localhost:9200')

# Returns the input name
def literal_index_strategy(name):
    return name

# Appends the current year, month, and day to the supplied index name 
# to break up an index into a daily index pattern.
def daily_index_strategy(name):
    today = datetime.date.today()
    time = str(today.year) + '.' + str(today.month) + '.' + str(today.day)
    return name + '-' + time

# Indexes the supplied document into elasticsearch, using the
# naming strategy to create indices using the given index name.
def index(index_base_name: str, naming_strategy, content: dict):
    es = get_connection()
    es.index(index = literal_index_strategy(index_base_name), body = content)
    # pass
    
