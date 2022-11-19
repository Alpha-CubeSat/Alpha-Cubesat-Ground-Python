from enum import Enum

class opcodes(Enum):
    normal_report = 99
    deployment_report = 24
    ttl = 42

def read_cubesat_data(rockblock_report):
    pass

def save_cubesat_data(data):
    pass

def process_deploy_data(data):
    pass
    
def process_ttl_data(data):
    pass