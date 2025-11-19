import os

from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # API documentation
    APIFAIRY_TITLE = 'Alpha CubeSat Ground Station API'
    APIFAIRY_VERSION = '1.0'
    APIFAIRY_UI = 'elements'

rockblock_db_index = 'rockblock_data'
cubesat_db_index = 'cubesat_normal_report'
cycle_db_index = 'imu_cycle_report'
deploy_db_index = 'imu_fragment_info'
capture_db_index = 'capture_fragment_info'
chipsat_db_index = 'chipsats'

capture_root_dir = os.path.join(basedir, 'cubesat_ods_captures')
cmd_log_root_dir = os.path.join(basedir, 'command_logs')
users_db = os.path.join(basedir, 'users.db')

gs_admin_password = os.environ.get('GS_ADMIN_PASS')
rockblock_config = {
    'username': os.environ.get('ROCKBLOCK_USER'),
    'password': os.environ.get('ROCKBLOCK_PASS')
}
elastic_config = {
    'url': os.environ.get('ELASTIC_URL', 'https://localhost:9200'),
    'username': os.environ.get('ELASTIC_USER'),
    'password': os.environ.get('ELASTIC_PASS'),
    'certs': os.environ.get('ELASTIC_CERTS')
}