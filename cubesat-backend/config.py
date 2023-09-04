import os

from dotenv import load_dotenv

from util.binary.binary_parser import BinaryTypes

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
rockblock_config = {
    'imei': os.environ.get('ROCKBLOCK_IMEI'),
    'username': os.environ.get('ROCKBLOCK_USER'),
    'password': os.environ.get('ROCKBLOCK_PASS')
}
elastic_config = {
    'username': os.environ.get('ELASTIC_USER'),
    'password': os.environ.get('ELASTIC_PASS'),
    'certs': os.environ.get('ELASTIC_CERTS')
}

# Public key provided for JWT verification by rockblock web services documentation
rockblock_web_pk = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlaWAVJfNWC4XfnRx96p9cztBcdQV6l8aKmzAlZdpEcQR6MSPzlgvihaUHNJgKm8t5ShR3jcDXIOI7er30cIN4/9aVFMe0LWZClUGgCSLc3rrMD4FzgOJ4ibD8scVyER/sirRzf5/dswJedEiMte1ElMQy2M6IWBACry9u12kIqG0HrhaQOzc6Tr8pHUWTKft3xwGpxCkV+K1N+9HCKFccbwb8okRP6FFAMm5sBbw4yAu39IVvcSL43Tucaa79FzOmfGs5mMvQfvO1ua7cOLKfAwkhxEjirC0/RYX7Wio5yL6jmykAHJqFG2HT0uyjjrQWMtoGgwv9cIcI7xbsDX6owIDAQAB\n-----END PUBLIC KEY-----"

normal_report_structure = [
    ('is_photoresistor_covered', BinaryTypes.uint8),
    ('is_door_button_pressed', BinaryTypes.uint8),
    ('mission_mode', BinaryTypes.uint8),
    ('burnwire_burn_time', BinaryTypes.uint8),
    ('burnwire_armed_timeout_limit', BinaryTypes.uint8),
    ('burnwire_mode', BinaryTypes.uint8),
    ('burnwire_attempts', BinaryTypes.uint8),
    ('downlink_period', BinaryTypes.uint8),
    ('waiting_messages', BinaryTypes.uint8),
    ('is_command_waiting', BinaryTypes.uint8),
    ('x_mag', BinaryTypes.uint8),
    ('y_mag', BinaryTypes.uint8),
    ('z_mag', BinaryTypes.uint8),
    ('x_gyro', BinaryTypes.uint8),
    ('y_gyro', BinaryTypes.uint8),
    ('z_gyro', BinaryTypes.uint8),
    ('photoresistor', BinaryTypes.uint8),
    ('temp', BinaryTypes.uint8),
    ('solar_current', BinaryTypes.uint8),
    ('in_sun', BinaryTypes.uint8),
    ('battery_voltage', BinaryTypes.uint8),
    ('fault_1', BinaryTypes.uint8),
    ('fault_2', BinaryTypes.uint8),
    ('fault_3', BinaryTypes.uint8),
    ('camera_on', BinaryTypes.uint8),
    ('eeprom_boot_counter', BinaryTypes.uint8),
    ('imu_is_valid', BinaryTypes.uint8),
    ('battery_is_valid', BinaryTypes.uint8),
    ('command_log', BinaryTypes.uint16)
    ]

