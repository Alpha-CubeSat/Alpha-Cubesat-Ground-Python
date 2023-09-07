from enum import Enum

from util.binary_parser import BinaryTypes


# Constants related to cubesat telemetry

class Opcodes(int, Enum):
    """Packet Opcodes for cubesat (see Alpha documentation for specification)"""

    normal_report = 99
    imu_report = 24
    camera_report = 42
    empty_packet = 0
    error = -1

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
    ('command_log', BinaryTypes.uint16_list)
]

# IMU report constants
MS_PER_CYCLE = 250
CYCLES_PER_FRAGMENT = 22

# Public key provided for JWT verification by rockblock web services documentation
ROCKBLOCK_PK = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlaWAVJfNWC4XfnRx96p9cztBcdQV6l8aKmzAlZdpEcQR6MSPzlgvihaUHNJgKm8t5ShR3jcDXIOI7er30cIN4/9aVFMe0LWZClUGgCSLc3rrMD4FzgOJ4ibD8scVyER/sirRzf5/dswJedEiMte1ElMQy2M6IWBACry9u12kIqG0HrhaQOzc6Tr8pHUWTKft3xwGpxCkV+K1N+9HCKFccbwb8okRP6FFAMm5sBbw4yAu39IVvcSL43Tucaa79FzOmfGs5mMvQfvO1ua7cOLKfAwkhxEjirC0/RYX7Wio5yL6jmykAHJqFG2HT0uyjjrQWMtoGgwv9cIcI7xbsDX6owIDAQAB\n-----END PUBLIC KEY-----"
