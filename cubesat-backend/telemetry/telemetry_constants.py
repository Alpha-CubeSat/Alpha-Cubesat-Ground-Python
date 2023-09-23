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

bool_fields = ["button_pressed", "current_in_sun", "temp_in_sun", 
               "waiting_command", "waiting_message", "camera_powered", 
               "possible_uncovered", "photo_resistor_covered"]

eeprom_bools = ["boot_mode", "error_mode", "light_switch", "sfr_save_completed"]

fault_fields = [['mag_x_value_fault','mag_x_average_fault'], ['mag_y_value_fault','mag_y_average_fault'], 
                ['mag_z_value_fault','mag_z_average_fault'], ['gyro_x_value_fault','gyro_x_average_fault'], 
                ['gyro_y_value_fault','gyro_y_average_fault'], ['gyro_z_value_fault','gyro_z_average_fault'],
                ['temp_c_value_fault','temp_c_average_fault'], ['voltage_value_fault','voltage_average_fault'],
                ['light_val_fault', 'hardware_faults'], ['solar_current_average_fault', eeprom_bools]]

normal_report_structure = [
    ('burn_time', BinaryTypes.uint8),
    ('armed_time', BinaryTypes.uint8),
    ('downlink_period', BinaryTypes.uint8),
    ('Id_index', BinaryTypes.uint8),
    ('Kd_index', BinaryTypes.uint8),
    ('Kp_index', BinaryTypes.uint8),
    ('c_index', BinaryTypes.uint8),
    ('boot_counter', BinaryTypes.uint8),
    ('dynamic_data_addr', BinaryTypes.uint8),
    ('sfr_data_addr', BinaryTypes.uint8),
    ('time_alive', BinaryTypes.uint8),
    ('dynamic_data_age', BinaryTypes.uint8),
    ('sfr_data_age', BinaryTypes.uint8),
    (bool_fields, BinaryTypes.uint8_bools),
    ('light_val_average_standby', BinaryTypes.uint8),
    ('light_val_average_deployment', BinaryTypes.uint8),
    ('mag_x_average', BinaryTypes.uint8),
    ('mag_y_average', BinaryTypes.uint8),
    ('mag_z_average', BinaryTypes.uint8),
    ('gyro_x_average', BinaryTypes.uint8),
    ('gyro_y_average', BinaryTypes.uint8),
    ('gyro_z_average', BinaryTypes.uint8),
    ('temp_c_average', BinaryTypes.uint8),
    ('temp_c_value', BinaryTypes.uint8),
    ('solar_current_average', BinaryTypes.uint8),
    ('voltage_value', BinaryTypes.uint8),
    ('voltage_average', BinaryTypes.uint8),
    (fault_fields, BinaryTypes.uint8_split),
    ('mission_mode_log', BinaryTypes.uint5_list),
    ('command_log', BinaryTypes.uint16_list)
]

# IMU report constants
MS_PER_CYCLE = 250
CYCLES_PER_FRAGMENT = 22

# Public key provided for JWT verification by rockblock web services documentation
ROCKBLOCK_PK = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlaWAVJfNWC4XfnRx96p9cztBcdQV6l8aKmzAlZdpEcQR6MSPzlgvihaUHNJgKm8t5ShR3jcDXIOI7er30cIN4/9aVFMe0LWZClUGgCSLc3rrMD4FzgOJ4ibD8scVyER/sirRzf5/dswJedEiMte1ElMQy2M6IWBACry9u12kIqG0HrhaQOzc6Tr8pHUWTKft3xwGpxCkV+K1N+9HCKFccbwb8okRP6FFAMm5sBbw4yAu39IVvcSL43Tucaa79FzOmfGs5mMvQfvO1ua7cOLKfAwkhxEjirC0/RYX7Wio5yL6jmykAHJqFG2HT0uyjjrQWMtoGgwv9cIcI7xbsDX6owIDAQAB\n-----END PUBLIC KEY-----"
