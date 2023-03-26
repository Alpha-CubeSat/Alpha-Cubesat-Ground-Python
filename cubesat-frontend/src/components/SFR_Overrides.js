export const stabilization = {
  // OP Codes 1100
  max_time: "uint32_t",
};

export const boot = {
  // OP Codes 1200
  max_time: "uint32_t",
};

export const simple = {
  // OP Codes 1300
  max_time: "uint32_t",
};

export const point = {
  // OP Codes 1400
  max_time: "uint32_t",
};

export const detumble = {
  // OP Codes 1500
  start_time: "uint32_t",
  max_time: "uint32_t",

  min_stable_gyro_z: "uint8_t",
  max_stable_gyro_x: "uint8_t",
  max_stable_gyro_y: "uint8_t",

  min_unstable_gyro_x: "uint8_t",
  min_unstable_gyro_y: "uint8_t",
};

export const aliveSignal = {
  // OP Codes 1600
  max_downlink_hard_faults: "uint16_t",
  downlinked: "bool",
  max_time: "uint32_t",
  num_hard_faults: "uint16_t",
};

export const photoresistor = {
  // OP Codes 1700
  covered: "bool",
};

export const mission = {
  // OP Codes 1800
  acs_transmit_cycle_time: "uint32_t",

  time_deployed: "uint32_t",
  deployed: "bool",
  already_deployed: "bool",
  possible_uncovered: "bool",
};

export const burnwire = {
  // OP Codes 1900
  attempts: "uint16_t",
  start_time: "uint32_t",
  burn_time: "uint32_t",
  armed_time: "uint32_t",
  mode: "uint16_t",
  attempts_limit: "uint16_t",
  mandatory_attempts_limit: "uint16_t",
  delay_time: "uint32_t",
};

export const camera = {
  // OP Codes 2000
  photo_taken_sd_failed: "bool",
  take_photo: "bool",
  turn_on: "bool",
  turn_off: "bool",
  powered: "bool",

  // Initialization
  start_progress: "uint8_t",
  step_time: "uint32_t",
  init_start_time: "uint32_t",
  init_timeout: "uint32_t",
  begin_delay: "uint32_t",
  resolution_set_delay: "uint32_t",
  resolution_get_delay: "uint32_t",

  init_mode: "uint16_t",
  mode: "uint16_t",

  images_written: "uint32_t",
  fragments_written: "uint32_t",

  set_res: "uint32_t",

  failed_times: "uint16_t",
  failed_limit: "uint16_t",

  fragment_number_requested: "uint32_t",
  serial_requested: "uint8_t",
};

export const rockblock = {
  // OP Codes 2100
  ready_status: "bool",

  last_downlink: "uint32_t",
  downlink_period: "uint32_t",

  waiting_message: "bool",

  max_commands_count: "uint8_t",

  imu_max_fragments: "uint16_t",

  imudownlink_start_time: "uint32_t",
  imudownlink_remain_time: "uint32_t",
  imu_first_start: "bool",
  imu_downlink_on: "bool",

  flush_status: "bool",
  waiting_command: "bool",
  conseq_reads: "uint32_t",
  timeout: "uint32_t",
  start_time: "uint32_t",
  start_time_check_signal: "uint32_t",
  max_check_signal_time: "uint32_t",
  sleep_mode: "bool",

  downlink_report_type: "uint16_t",
  mode: "uint16_t",
};

export const imu = {
  // OP Codes 2200
  mode: "uint16_t",

  init_mode: "uint16_t",

  max_fragments: "uint32_t",

  sample_gyro: "bool",

  turn_on: "bool",
  turn_off: "bool",
  powered: "bool",

  failed_times: "uint16_t",
  failed_limit: "uint16_t",
};

export const temperature = {
  // OP Codes 2300
  in_sun: "bool",
};

export const current = {
  // OP Codes 2400
  in_sun: "bool",
};

export const acs = {
  // OP Codes 2500
  max_no_communication: "uint32_t",

  on_time: "uint32_t",
  off: "bool",

  mag: "uint16_t",
};

export const battery = {
  // OP Codes 2600
  acceptable_battery: "uint32_t",
  min_battery: "uint32_t",
};

export const button = {
  // OP Codes 2700
  pressed: "bool",
};

export const eeprom = {
  // OP Codes 2800
  boot_counter: "uint8_t",
  wait_time_write_step_time: "uint32_t",
  allotted_time: "uint32_t",
  allotted_time_passed: "bool",
  sfr_write_step_time: "uint32_t",
  sfr_address_age: "uint32_t",
};
