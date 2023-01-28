import os

from dotenv import load_dotenv

from util.binary.binary_parser import BinaryTypes

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # API documentation
    APIFAIRY_TITLE = 'Alpha CubeSat Ground Station API'
    APIFAIRY_VERSION = '1.0'
    APIFAIRY_UI = os.environ.get('DOCS_UI', 'elements')

rockblock_db_index = 'rockblock_data'
cubesat_db_index = 'cubesat_normal_report'
cycle_db_index = 'imu_cycle_report'
deploy_db_index = 'cubesat_deploy_report'
image_db_index = 'image_fragment_info'

image_root_dir = os.path.join(basedir, 'cubesat_images')
users_db = os.path.join(basedir, 'users.db')

normal_report_structure = [
    ('is_photoresistor_covered', BinaryTypes.uint8),
    ('is_door_button_pressed', BinaryTypes.uint8),
    ('mission_mode', BinaryTypes.uint8),
    ('fire_burnwire', BinaryTypes.uint8),
    ('arm_burnwire', BinaryTypes.uint8),
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
    ('temp', BinaryTypes.uint8),
    ('temp_mode', BinaryTypes.uint8),
    ('solar_current', BinaryTypes.uint8),
    ('in_sun', BinaryTypes.uint8),
    ('acs_mode', BinaryTypes.uint8),
    ('battery_voltage', BinaryTypes.uint8),
    ('fault_mode', BinaryTypes.uint8),
    ('check_x_mag', BinaryTypes.uint8),
    ('check_y_mag', BinaryTypes.uint8),
    ('check_z_mag', BinaryTypes.uint8),
    ('check_x_gyro', BinaryTypes.uint8),
    ('check_y_gyro', BinaryTypes.uint8),
    ('check_z_gyro', BinaryTypes.uint8),
    ('check_temp', BinaryTypes.uint8),
    ('check_solar_current', BinaryTypes.uint8),
    ('check_battery', BinaryTypes.uint8),
    ('take_photo', BinaryTypes.uint8),
    ('camera_on', BinaryTypes.uint8)
]