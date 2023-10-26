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
deploy_db_index = 'cubesat_deploy_report'
image_db_index = 'image_fragment_info'

image_root_dir = os.path.join(basedir, 'cubesat_images')
users_db = os.path.join(basedir, 'users.db')

gs_admin_password = os.environ.get('GS_ADMIN_PASS', 'admin')
rockblock_config = {
    'username': os.environ.get('ROCKBLOCK_USER'),
    'password': os.environ.get('ROCKBLOCK_PASS')
}
elastic_config = {
    'username': os.environ.get('ELASTIC_USER'),
    'password': os.environ.get('ELASTIC_PASS'),
    'certs': os.environ.get('ELASTIC_CERTS')
}

rockblock_imei = os.environ.get('ROCKBLOCK_IMEI')