opcode_map = {
  "13107": "deploy",
  "17476": "arm",
  "21845": "fire",
  "4352": "stabilization : max_time",
  "4608": "boot : max_time",
  "4864": "simple : max_time",
  "5120": "point : max_time",
  "5376": "detumble : start_time",
  "5377": "detumble : max_time",
  "5380": "detumble : min_stable_gyro_z",
  "5381": "detumble : max_stable_gyro_x",
  "5382": "detumble : max_stable_gyro_y",
  "5383": "detumble : min_unstable_gyro_x",
  "5384": "detumble : min_unstable_gyro_y",
  "5632": "aliveSignal : max_downlink_hard_faults",
  "5633": "aliveSignal : downlinked",
  "5634": "aliveSignal : max_time",
  "5635": "aliveSignal : num_hard_faults",
  "5888": "photoresistor : covered",
  "6144": "mission : acs_transmit_cycle_time",
  "6145": "mission : time_deployed",
  "6146": "mission : deployed",
  "6147": "mission : already_deployed",
  "6148": "mission : possible_uncovered",
  "6400": "burnwire : attempts",
  "6401": "burnwire : start_time",
  "6402": "burnwire : burn_time",
  "6403": "burnwire : armed_time",
  "6404": "burnwire : mode",
  "6405": "burnwire : attempts_limit",
  "6406": "burnwire : mandatory_attempts_limit",
  "6407": "burnwire : delay_time",
  "8192": "camera : photo_taken_sd_failed",
  "8193": "camera : take_photo",
  "8194": "camera : turn_on",
  "8195": "camera : turn_off",
  "8196": "camera : powered",
  "8197": "camera : start_progress",
  "8198": "camera : step_time",
  "8199": "camera : init_start_time",
  "8200": "camera : init_timeout",
  "8201": "camera : begin_delay",
  "8208": "camera : resolution_set_delay",
  "8209": "camera : resolution_get_delay",
  "8210": "camera : init_mode",
  "8211": "camera : mode",
  "8212": "camera : images_written",
  "8213": "camera : fragments_written",
  "8214": "camera : set_res",
  "8215": "camera : failed_times",
  "8216": "camera : failed_limit",
  "8217": "camera : fragment_number_requested",
  "8224": "camera : serial_requested",
  "8448": "rockblock : ready_status",
  "8449": "rockblock : last_downlink",
  "8450": "rockblock : downlink_period",
  "8451": "rockblock : waiting_message",
  "8452": "rockblock : max_commands_count",
  "8453": "rockblock : imu_max_fragments",
  "8454": "rockblock : imudownlink_start_time",
  "8455": "rockblock : imudownlink_remain_time",
  "8456": "rockblock : imu_first_start",
  "8457": "rockblock : imu_downlink_on",
  "8464": "rockblock : flush_status",
  "8465": "rockblock : waiting_command",
  "8466": "rockblock : conseq_reads",
  "8467": "rockblock : timeout",
  "8468": "rockblock : start_time",
  "8469": "rockblock : start_time_check_signal",
  "8470": "rockblock : max_check_signal_time",
  "8471": "rockblock : sleep_mode",
  "8472": "rockblock : downlink_report_type",
  "8473": "rockblock : mode",
  "8704": "imu : mode",
  "8705": "imu : init_mode",
  "8706": "imu : max_fragments",
  "8707": "imu : sample_gyro",
  "8708": "imu : turn_on",
  "8709": "imu : turn_off",
  "8710": "imu : powered",
  "8711": "imu : failed_times",
  "8712": "imu : failed_limit",
  "8713": "imu : imu_boot_collection_start_time",
  "8714": "imu : door_open__collection_start_time",
  "8960": "temperature : in_sun",
  "9216": "current : in_sun",
  "9472": "acs : max_no_communication",
  "9473": "acs : on_time",
  "9474": "acs : off",
  "9475": "acs : mag",
  "9476": "acs : detumble_timeout",
  "9728": "battery : acceptable_battery",
  "9729": "battery : min_battery",
  "9984": "button : pressed",
  "10240": "eeprom : boot_counter",
  "10241": "eeprom : wait_time_write_step_time",
  "10242": "eeprom : alloted_time",
  "10243": "eeprom : alloted_time_passed",
  "10244": "eeprom : sfr_write_step_time",
  "10245": "eeprom : sfr_address_age",
  "10246": "eeprom : storage_full",
  "command_log": []
}