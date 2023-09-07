# Constants related to Cubesat commanding

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