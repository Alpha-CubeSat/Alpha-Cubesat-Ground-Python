# Constants related to Cubesat commanding
from enum import Enum

ROCKBLOCK_ENDPOINT = 'https://core.rock7.com/rockblock/MT'
ARG_LENGTH = 8
FLAG_LENGTH = 2

class SFR_T(str, Enum):
    BOOL = 'BOOL',
    FLOAT = 'FLOAT',
    INT = 'INT',
    TIME = 'TIME',
    MULTI = 'MULTI'

BURNWIRE_OPCODES = {
    'Deploy': '3333',
    'Arm': '4444',
    'Fire': '5555'
}

EEPROM_RESET_OPCODE = '7777'

SFR_OVERRIDE_OPCODES_MAP = {
    'stabilization': {
        'max_time': {
            'hex': '1100',
            'type': SFR_T.TIME,
        }
    },
    'boot': {
        'max_time': {
            'hex': '1200',
            'type': SFR_T.TIME,
        },
    },
    'detumble': {
        'min_stable_gyro_z': {
            'hex': '1500',
            'type': SFR_T.FLOAT,
        },
        'max_stable_gyro_x': {
            'hex': '1501',
            'type': SFR_T.FLOAT,
        },
        'max_stable_gyro_y': {
            'hex': '1502',
            'type': SFR_T.FLOAT,
        },
        'min_unstable_gyro_x': {
            'hex': '1503',
            'type': SFR_T.FLOAT,
        },
        'min_unstable_gyro_y': {
            'hex': '1504',
            'type': SFR_T.FLOAT,
        },
    },
    'aliveSignal': {
        'downlinked': {
            'hex': '1600',
            'type': SFR_T.BOOL,
        },
        'max_downlink_hard_faults': {
            'hex': '1601',
            'type': SFR_T.INT
        },
        'num_hard_faults': {
            'hex': '1602',
            'type': SFR_T.INT
        },
        'max_time': {
            'hex': '1603',
            'type': SFR_T.TIME,
        },
    },
    'photoresistor': {
        'covered': {
            'hex': '1700',
            'type': SFR_T.BOOL,
        },
    },
    'mission': {
        'deployed': {
            'hex': '1800',
            'type': SFR_T.BOOL,
        },
        'possible_uncovered': {
            'hex': '1801',
            'type': SFR_T.BOOL,
        },
        'boot_time': {
            'hex': '1802',
            'type': SFR_T.INT
        },
        'mission_mode_hist_length': {
            'hex': '1803',
            'type': SFR_T.INT
        },
        'cycle_no': {
            'hex': '1804',
            'type': SFR_T.INT
        },
        'cycle_dur': {
            'hex': '1805',
            'type': SFR_T.INT
        },
    },
    'burnwire': {
        'attempts': {
            'hex': '1900',
            'type': SFR_T.INT
        },
        'mode': {
            'hex': '1901',
            'min': 0,
            'max': 2,
            'type': SFR_T.INT
        },
        'attempts_limit': {
            'hex': '1902',
            'type': SFR_T.INT
        },
        'mandatory_attempts_limit': {
            'hex': '1903',
            'type': SFR_T.INT
        },
        'start_time': {
            'hex': '1904',
            'type': SFR_T.INT
        },
        'burn_time': {
            'hex': '1905',
            'min': 0,
            'max': 5000,
            'type': SFR_T.TIME,
        },
        'armed_time': {
            'hex': '1906',
            'min': 0,
            'max': 12*360000,
            'type': SFR_T.TIME,
        },
        'delay_time': {
            'hex': '1907',
            'type': SFR_T.INT
        },
    },
    'camera': {
        'photo_taken_sd_failed': {
            'hex': '2000',
            'type': SFR_T.BOOL,
        },
        'take_photo': {
            'hex': '2001',
            'type': SFR_T.BOOL,
        },
        'turn_on': {
            'hex': '2002',
            'type': SFR_T.BOOL,
        },
        'turn_off': {
            'hex': '2003',
            'type': SFR_T.BOOL,
        },
        'powered': {
            'hex': '2004',
            'type': SFR_T.BOOL,
        },
        'report_ready': {
            'hex': '2005',
            'type': SFR_T.BOOL,
        },
        'fragment_requested': {
            'hex': '2006',
            'type': SFR_T.BOOL,
        },
        'start_progress': {
            'hex': '2007',
            'type': SFR_T.INT
        },
        'serial_requested': {
            'hex': '2008',
            'type': SFR_T.INT
        },
        'mode': {
            'hex': '2009',
            'min': 0,
            'max': 2,
            'type': SFR_T.INT
        },
        'failed_times': {
            'hex': '2010',
            'type': SFR_T.INT
        },
        'failed_limit': {
            'hex': '2011',
            'type': SFR_T.INT
        },
        'init_mode': {
            'hex': '2012',
            'min': 0,
            'max': 3,
            'type': SFR_T.INT
        },
        'init_start_time': {
            'hex': '2013',
            'type': SFR_T.INT
        },
        'init_timeout': {
            'hex': '2014',
            'type': SFR_T.INT
        },
        'images_written': {
            'hex': '2015',
            'type': SFR_T.INT
        },
        'fragments_written': {
            'hex': '2016',
            'type': SFR_T.INT
        },
        'set_res': {
            'hex': '2017',
            'type': SFR_T.INT
        },
        'fragment_number_requested': {
            'hex': '2018',
            'type': SFR_T.INT
        },
    },
    'rockblock': {
        'ready_status': {
            'hex': '2100',
            'type': SFR_T.BOOL,
        },
        'waiting_command': {
            'hex': '2101',
            'type': SFR_T.BOOL,
        },
        'flush_status': {
            'hex': '2102',
            'type': SFR_T.BOOL,
        },
        'sleep_mode': {
            'hex': '2103',
            'type': SFR_T.BOOL,
        },
        'max_commands_count': {
            'hex': '2104',
            'type': SFR_T.INT
        },
        'downlink_report_type': {
            'hex': '2105',
            'min': 0,
            'max': 2,
            'type': SFR_T.INT
        },
        'mode': {
            'hex': '2106',
            'min': 0,
            'max': 22,
            'type': SFR_T.INT
        },
        'last_downlink': {
            'hex': '2107',
            'type': SFR_T.INT
        },
        'downlink_period': {
            'hex': '2108',
            'min': 1,
            'max': 86400000*2,
            'type': SFR_T.TIME,
        },
        'lp_downlink_period': {
            'hex': '2109',
            'min': 1,
            'max': 86400000*2,
            'type': SFR_T.TIME,
        },
        'transmit_downlink_period': {
            'hex': '2110',
            'min': 1,
            'max': 86400000*2,
            'type': SFR_T.TIME,
        },
        'on_time': {
            'hex': '2111',
            'min': 0,
            'max': 5400000,
            'type': SFR_T.TIME,
        },
        'start_time_check_signal': {
            'hex': '2112',
            'type': SFR_T.INT
        },
    },
    'imu': {
        'sample_gyro': {
            'hex': '2200',
            'type': SFR_T.BOOL,
        },
        'turn_on': {
            'hex': '2201',
            'type': SFR_T.BOOL,
        },
        'turn_off': {
            'hex': '2202',
            'type': SFR_T.BOOL,
        },
        'powered': {
            'hex': '2203',
            'type': SFR_T.BOOL,
        },
        'report_written': {
            'hex': '2204',
            'type': SFR_T.BOOL,
        },
        'report_ready': {
            'hex': '2205',
            'type': SFR_T.BOOL,
        },
        'mode': {
            'hex': '2206',
            'min': 0,
            'max': 2,
            'type': SFR_T.INT
        },
        'init_mode': {
            'hex': '2207',
            'min': 0,
            'max': 3,
            'type': SFR_T.INT
        },
        'failed_times': {
            'hex': '2208',
            'type': SFR_T.INT
        },
        'failed_limit': {
            'hex': '2209',
            'type': SFR_T.INT
        },
        'imu_boot_collection_start_time': {
            'hex': '2210',
            'type': SFR_T.INT
        },
        'door_open__collection_start_time': {
            'hex': '2211',
            'type': SFR_T.INT
        },
        'max_fragments': {
            'hex': '2212',
            'type': SFR_T.INT
        },
    },
    'temperature': {
        'in_sun': {
            'hex': '2300',
            'type': SFR_T.BOOL,
        },
    },
    'current': {
        'in_sun': {
            'hex': '2400',
            'type': SFR_T.BOOL,
        },
    },
    'acs': {
        'off': {
            'hex': '2500',
            'type': SFR_T.BOOL,
        },
        'mode': {
            'hex': '2501',
            'min': 0,
            'max': 2,
            'type': SFR_T.INT
        },
        'simple_mag': {
            'hex': '2502',
            'type': SFR_T.BOOL,
        },
        'simple_current': {
            'hex': '2503',
            'type': SFR_T.BOOL,
        },
        'on_time': {
            'hex': '2504',
            'min': 0,
            'max': 5400000,
            'type': SFR_T.TIME,
        },
        'Id_index': {
            'hex': '2505',
            'min': 0,
            'max': 1,
            'type': SFR_T.INT
        },
        'Kd_index': {
            'hex': '2506',
            'min': 0,
            'max': 1,
            'type': SFR_T.INT
        },
        'Kp_index': {
            'hex': '2507',
            'min': 0,
            'max': 1,
            'type': SFR_T.INT
        },
        'c_index': {
            'hex': '2508',
            'min': 0,
            'max': 1,
            'type': SFR_T.INT
        },
    },
    'battery': {
        'acceptable_battery': {
            'hex': '2600',
            'type': SFR_T.FLOAT,
        },
        'min_battery': {
            'hex': '2601',
            'type': SFR_T.FLOAT
        },
    },
    'button': {
        'pressed': {
            'hex': '2700',
            'type': SFR_T.BOOL,
        },
    },
    'eeprom': {
        'boot_mode': {
            'hex': '2800',
            'type': SFR_T.BOOL,
        },
        'boot_restarted': {
            'hex': '2801',
            'type': SFR_T.BOOL,
        },
        'error_mode': {
            'hex': '2802',
            'type': SFR_T.BOOL,
        },
        'light_switch': {
            'hex': '2803',
            'type': SFR_T.BOOL,
        },
        'sfr_save_completed': {
            'hex': '2804',
            'type': SFR_T.BOOL,
        },
        'boot_counter': {
            'hex': '2805',
            'type': SFR_T.INT
        },
        'dynamic_data_addr': {
            'hex': '2806',
            'min': 10,
            'max': 89,
            'type': SFR_T.INT
        },
        'sfr_data_addr': {
            'hex': '2807',
            'min': 90,
            'max': 4085,
            'type': SFR_T.INT
        },
        'time_alive': {
            'hex': '2808',
            'type': SFR_T.INT
        },
        'dynamic_data_age': {
            'hex': '2809',
            'type': SFR_T.INT
        },
        'sfr_data_age': {
            'hex': '2810',
            'type': SFR_T.INT
        },
        # not really sfr but here for convenience
        'eeprom_reset': {
            'hex': '2811',
            'type': SFR_T.MULTI
        }
    },
}

COMMAND_OPCODE_MAP = {}
COMMAND_OPCODE_MAP[EEPROM_RESET_OPCODE] = 'EEROM Reset'
for (k, v) in BURNWIRE_OPCODES.items():
    COMMAND_OPCODE_MAP[v] = k

for namespace in SFR_OVERRIDE_OPCODES_MAP:
    for field in SFR_OVERRIDE_OPCODES_MAP[namespace]:
        hex_val = SFR_OVERRIDE_OPCODES_MAP[namespace][field]['hex']
        COMMAND_OPCODE_MAP[hex_val] = namespace + '::' + field
