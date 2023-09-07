import os
from enum import Enum

from dotenv import load_dotenv

from util.binary_parser import BinaryTypes

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

class Opcodes(int, Enum):
    """Packet Opcodes for cubesat (see Alpha documentation for specification)"""

    normal_report = 99
    imu_report = 24
    camera_report = 42
    empty_packet = 0
    error = -1

# CONSTANTS
MS_PER_CYCLE = 250
CYCLES_PER_FRAGMENT = 22

ROCKBLOCK_ENDPOINT = 'https://core.rock7.com/rockblock/MT'
ARG_LENGTH = 8
FLAG_LENGTH = 2
BURNWIRE_OPCODES =  {
    'Deploy': '3333',
    'Arm': '4444',
    'Fire': '5555'
}
SFR_OVERRIDE_OPCODES_MAP = {
    'stabilization': {
        'max_time': '1100',
    },
    'boot': {
        'max_time': '1200',
    },
    'simple': {
        'max_time': '1300',
    },
    'point': {
        'max-time': '1400',
    },
    'detumble': {
        'start_time': '1500',
        'max_time': '1501',
        'min_stable_gyro_z': '1502',
        'max_stable_gyro_x': '1503',
        'max_stable_gyro_y': '1504',
        'min_unstable_gyro_x': '1505',
        'min_unstable_gyro_y': '1506',
    },
    'aliveSignal' : {
        'max_downlink_hard_faults': '1600',
        'downlinked': '1601',
        'max_time': '1602',
        'num_hard_faults': '1603',
    },
    'photoresistor': {
        'covered': '1700',
    },
    'mission': {
        'acs_transmit_cycle_time': '1800',
        'time_deployed': '1801',
        'deployed': '1802',
        'already_deployed': '1803',
        'possible_uncovered': '1804',
    },
    'burnwire': {
        'attempts': '1900',
        'start_time': '1901',
        'burn_time': '1902',
        'armed_time': '1903',
        'mode': '1904',
        'attempts_limit': '1905',
        'mandatory_attempts_limit': '1906',
        'delay_time': '1907',
    },
    'camera': {
        'photo_taken_sd_failed': '2000',
        'take_photo': '2001',
        'turn_on': '2002',
        'turn_off': '2003',
        'powered': '2004',
        'start_progress': '2005',
        'step_time': '2006',
        'init_start_time': '2007',
        'init_timeout': '2008',
        'begin_delay': '2009',
        'resolution_set_delay': '2010',
        'resolution_get_delay': '2011',
        'init_mode': '2012',
        'mode': '2013',
        'images_written': '2014',
        'fragments_written': '2015',
        'set_res': '2016',
        'failed_times': '2017',
        'failed_limit': '2018',
        'fragment_number_requested': '2019',
        'serial_requested': '2020',
    },
    'rockblock': {
        'ready_status': '2100',
        'last_downlink': '2101',
        'downlink_period': '2102',
        'waiting_message': '2103',
        'max_commands_count': '2104',
        'imu_max_fragments': '2105',
        'imu_downlink_start_time': '2106',
        'imu_downlink_remain_time': '2107',
        'imu_first_start': '2108',
        'imu_downlink_on': '2109',
        'flush_status': '2110',
        'waiting_command': '2111',
        'conseq_reads': '2112',
        'timeout': '2113',
        'start_time': '2114',
        'start_time_check_signal': '2115',
        'max_check_signal_time': '2116',
        'sleep_mode': '2117',
        'downlink_report_type': '2118',
        'mode': '2119',
    },
    'imu': {
        'mode': '2200',
        'init_mode': '2201',
        'max_fragments': '2202',
        'sample_gyro': '2203',
        'turn_on': '2204',
        'turn_off': '2205',
        'powered': '2206',
        'failed_times': '2207',
        'failed_limit': '2208',
    },
    'temperature': {
        'in_sun': '2300',
    },
    'current': {
        'in_sun': '2400',
    },
    'acs': {
        'max_no_communication': '2500',
        'on_time': '2501',
        'off': '2502',
        'mag': '2503',
    },
    'battery': {
        'acceptable_battery': '2600',
        'min_battery': '2601',
    },
    'button': {
        'pressed': '2700',
    },
    'eeprom': {
        'boot_counter': '2800',
        'wait_time_write_step_time': '2801',
        'allotted_time': '2802',
        'allotted_time_passed': '2803',
        'sfr_write_step_time': '2804',
        'sfr_address_age': '2805',
        'storage_full': '2806',
    },
}
