# Constants related to Cubesat commanding
from enum import Enum

ROCKBLOCK_ENDPOINT = 'https://core.rock7.com/rockblock/MT'
ARG_LENGTH = 8
FLAG_LENGTH = 2

class SFR_T(str, Enum):
    BOOL = 'BOOL',
    FLOAT = 'FLOAT',
    SECOND = 'SECOND',
    MINUTE = 'MINUTE',
    HOUR = 'HOUR',
    MULTI = 'MULTI'

BURNWIRE_OPCODES = {
    'Deploy': '3333',
    'Arm': '4444',
    'Fire': '5555'
}

SFR_OVERRIDE_OPCODES_MAP = {
    'stabilization': {
        'max_time': {
            'hex': '1100',
            'type': SFR_T.MINUTE,
        }
    },
    'boot': {
        'max_time': {
            'hex': '1200',
            'type': SFR_T.HOUR,
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
        },
        'num_hard_faults': {
            'hex': '1602',
        },
        'max_time': {
            'hex': '1603',
            'type': SFR_T.HOUR,
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
        'mission_mode_hist_length': {
            'hex': '1802',
        },
        'cycle_no': {
            'hex': '1803',
        },
        'cycle_dur': {
            'hex': '1804',
        },
        'mission_time': {
            'hex': '1805',
        },
        'boot_time': {
            'hex': '1806',
        },
    },
    'burnwire': {
        'attempts': {
            'hex': '1900',
        },
        'mode': {
            'hex': '1901',
            'min': 0,
            'max': 2,
        },
        'attempts_limit': {
            'hex': '1902',
        },
        'mandatory_attempts_limit': {
            'hex': '1903',
        },
        'start_time': {
            'hex': '1904',
        },
        'burn_time': {
            'hex': '1905',
            'type': 'SECONDS',
        },
        'armed_time': {
            'hex': '1906',
            'type': SFR_T.HOUR,
        },
        'delay_time': {
            'hex': '1907',
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
        },
        'serial_requested': {
            'hex': '2008',
        },
        'mode': {
            'hex': '2009',
            'min': 0,
            'max': 2,
        },
        'failed_times': {
            'hex': '2010',
        },
        'failed_limit': {
            'hex': '2011',
        },
        'init_mode': {
            'hex': '2012',
            'min': 0,
            'max': 3,
        },
        'step_time': {
            'hex': '2013',
        },
        'init_start_time': {
            'hex': '2014',
        },
        'init_timeout': {
            'hex': '2015',
        },
        'resolution_set_delay': {
            'hex': '2016',
        },
        'resolution_get_delay': {
            'hex': '2017',
        },
        'images_written': {
            'hex': '2018',
        },
        'fragments_written': {
            'hex': '2019',
        },
        'set_res': {
            'hex': '2020',
        },
        'fragment_number_requested': {
            'hex': '2021',
        },
    },
    'rockblock': {
        'ready_status': {
            'hex': '2100',
            'type': SFR_T.BOOL,
        },
        'waiting_message': {
            'hex': '2101',
            'type': SFR_T.BOOL,
        },
        'waiting_command': {
            'hex': '2102',
            'type': SFR_T.BOOL,
        },
        'flush_status': {
            'hex': '2103',
            'type': SFR_T.BOOL,
        },
        'sleep_mode': {
            'hex': '2104',
            'type': SFR_T.BOOL,
        },
        'max_commands_count': {
            'hex': '2105',
        },
        'imu_max_fragments': {
            'hex': '2106',
        },
        'downlink_report_type': {
            'hex': '2107',
            'min': 0,
            'max': 2,
        },
        'mode': {
            'hex': '2108',
            'min': 0,
            'max': 22,
        },
        'last_downlink': {
            'hex': '2109',
        },
        'downlink_period': {
            'hex': '2110',
            'type': SFR_T.SECOND,
        },
        'conseq_reads': {
            'hex': '2111',
        },
        'start_time_check_signal': {
            'hex': '2112',
        },
        'max_check_signal_time': {
            'hex': '2113',
            'type': SFR_T.MINUTE,
        },
        'on_time': {
            'hex': '2114',
            'type': SFR_T.MINUTE,
        }
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
        },
        'init_mode': {
            'hex': '2207',
            'min': 0,
            'max': 3,
        },
        'failed_times': {
            'hex': '2208',
        },
        'failed_limit': {
            'hex': '2209',
        },
        'imu_boot_collection_start_time': {
            'hex': '2210',
        },
        'door_open__collection_start_time': {
            'hex': '2211',
        },
        'max_fragments': {
            'hex': '2212',
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
            'type': SFR_T.MINUTE,
        },
        'Id_index': {
            'hex': '2505',
            'min': 0,
            'max': 1,
        },
        'Kd_index': {
            'hex': '2506',
            'min': 0,
            'max': 1,
        },
        'Kp_index': {
            'hex': '2507',
            'min': 0,
            'max': 1,
        },
        'c_index': {
            'hex': '2508',
            'min': 0,
            'max': 1,
        },
    },
    'battery': {
        'acceptable_battery': {
            'hex': '2600',
            'type': SFR_T.FLOAT,
        },
        'min_battery': {
            'hex': '2601',
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
        'error_mode': {
            'hex': '2801',
            'type': SFR_T.BOOL,
        },
        'light_switch': {
            'hex': '2802',
            'type': SFR_T.BOOL,
        },
        'sfr_save_completed': {
            'hex': '2803',
            'type': SFR_T.BOOL,
        },
        'boot_counter': {
            'hex': '2804',
        },
        'dynamic_data_addr': {
            'hex': '2805',
        },
        'sfr_data_addr': {
            'hex': '2806',
        },
        'time_alive': {
            'hex': '2807',
        },
        'dynamic_data_age': {
            'hex': '2808',
        },
        'sfr_data_age': {
            'hex': '2809',
        },
        'eeprom_reset': {
            'hex': '2810',
            'type': SFR_T.MULTI
        }
    },
}
