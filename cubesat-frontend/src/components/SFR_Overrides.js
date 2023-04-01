// Flight Software SFR Fields
// see https://github.com/Alpha-CubeSat/oop-flight-code/blob/main/src/sfr.cpp for more info

export const Types = Object.freeze({
  Minute: "Minute",
  Hour: "Hour",
  Int: "Int",
  Float: "Float",
  Bool: "Bool",
});

const stabilization = {
  // OP Codes 1100
  max_time: { type: Types.Minute },
};

const boot = {
  // OP Codes 1200
  max_time: { type: Types.Hour },
};

const simple = {
  // OP Codes 1300
  max_time: { type: Types.Minute },
};

const point = {
  // OP Codes 1400
  max_time: { type: Types.Minute },
};

const detumble = {
  // OP Codes 1500
  start_time: { type: Types.Int },
  max_time: { type: Types.Hour },

  min_stable_gyro_z: "uint8_t",
  max_stable_gyro_x: "uint8_t",
  max_stable_gyro_y: "uint8_t",

  min_unstable_gyro_x: "uint8_t",
  min_unstable_gyro_y: "uint8_t",
};

const aliveSignal = {
  // OP Codes 1600
  max_downlink_hard_faults: { type: Types.Int },
  downlinked: { type: Types.Bool },
  max_time: { type: Types.Hour },
  num_hard_faults: { type: Types.Int },
};

const photoresistor = {
  // OP Codes 1700
  covered: { type: Types.Bool },
};

const mission = {
  // OP Codes 1800
  acs_transmit_cycle_time: { type: Types.Minute },

  time_deployed: { type: Types.Int },
  deployed: { type: Types.Bool },
  already_deployed: { type: Types.Bool },
  possible_uncovered: { type: Types.Bool },
};

const burnwire = {
  // OP Codes 1900
  attempts: { type: Types.Int },
  start_time: { type: Types.Int },
  burn_time: { type: Types.Int },
  armed_time: { type: Types.Int },
  mode: "uint16_t",
  attempts_limit: { type: Types.Int },
  mandatory_attempts_limit: { type: Types.Int },
  delay_time: { type: Types.Int },
};

const camera = {
  // OP Codes 2000
  photo_taken_sd_failed: { type: Types.Bool },
  take_photo: { type: Types.Bool },
  turn_on: { type: Types.Bool },
  turn_off: { type: Types.Bool },
  powered: { type: Types.Bool },

  // Initialization
  start_progress: { type: Types.Int },
  step_time: { type: Types.Int },
  init_start_time: { type: Types.Int },
  init_timeout: { type: Types.Int },
  begin_delay: { type: Types.Int },
  resolution_set_delay: { type: Types.Int },
  resolution_get_delay: { type: Types.Int },

  init_mode: "uint16_t",
  mode: "uint16_t",

  images_written: { type: Types.Int },
  fragments_written: { type: Types.Int },

  set_res: "uint32_t",

  failed_times: { type: Types.Int },
  failed_limit: { type: Types.Int },

  fragment_number_requested: { type: Types.Int },
  serial_requested: { type: Types.Int },
};

const rockblock = {
  // OP Codes 2100
  ready_status: { type: Types.Bool },

  last_downlink: { type: Types.Int },
  downlink_period: { type: Types.Int },

  waiting_message: { type: Types.Bool },

  max_commands_count: { type: Types.Int },

  imu_max_fragments: { type: Types.Int },
  imu_downlink_start_time: { type: Types.Int },
  imu_downlink_remain_time: { type: Types.Int },
  imu_first_start: { type: Types.Bool },
  imu_downlink_on: { type: Types.Bool },

  flush_status: { type: Types.Bool },
  waiting_command: { type: Types.Bool },
  conseq_reads: { type: Types.Int },
  timeout: { type: Types.Minute },
  start_time: { type: Types.Int },
  start_time_check_signal: { type: Types.Int },
  max_check_signal_time: { type: Types.Minute },
  sleep_mode: { type: Types.Bool },

  downlink_report_type: "uint16_t",
  mode: "uint16_t",
};

const imu = {
  // OP Codes 2200
  mode: "uint16_t",

  init_mode: "uint16_t",

  max_fragments: { type: Types.Int },

  sample_gyro: { type: Types.Bool },

  turn_on: { type: Types.Bool },
  turn_off: { type: Types.Bool },
  powered: { type: Types.Bool },

  failed_times: { type: Types.Int },
  failed_limit: { type: Types.Int },
};

const temperature = {
  // OP Codes 2300
  in_sun: { type: Types.Bool },
};

const current = {
  // OP Codes 2400
  in_sun: { type: Types.Bool },
};

const acs = {
  // OP Codes 2500
  max_no_communication: { type: Types.Int },

  on_time: { type: Types.Minute },
  off: { type: Types.Bool },

  mag: "uint16_t",
};

const battery = {
  // OP Codes 2600
  acceptable_battery: "uint32_t",
  min_battery: "uint32_t",
};

const button = {
  // OP Codes 2700
  pressed: { type: Types.Bool },
};

const eeprom = {
  // OP Codes 2800
  boot_counter: { type: Types.Int },
  wait_time_write_step_time: { type: Types.Int },
  allotted_time: { type: Types.Int },
  allotted_time_passed: { type: Types.Bool },
  sfr_write_step_time: { type: Types.Int },
  sfr_address_age: { type: Types.Int },
  storage_full: { type: Types.Bool },
};

const namespaces = {
  stabilization: stabilization,
  boot: boot,
  simple: simple,
  point: point,
  detumble: detumble,
  aliveSignal: aliveSignal,
  photoresistor: photoresistor,
  mission: mission,
  burnwire: burnwire,
  camera: camera,
  rockblock: rockblock,
  imu: imu,
  temperature: temperature,
  current: current,
  acs: acs,
  battery: battery,
  button: button,
  eeprom: eeprom,
};
export default namespaces;
