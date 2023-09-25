// Flight Software SFR Fields
// see https://github.com/Alpha-CubeSat/oop-flight-code/blob/main/src/sfr.cpp for more info

export const Types = Object.freeze({
  Minute: "Minute",
  Hour: "Hour",
  Int: "Int",
  MultiInt: "MultiInt",
  Float: "Float",
  Bool: "Bool",
});

const stabilization = {
  // OP Codes 1100
  max_time: { type: Types.Minute, min: 0, max: 300 },
};

const boot = {
  // OP Codes 1200
  max_time: { type: Types.Hour, min: 0, max: 5 }, // 10UL for min?
};

const simple = {
  // OP Codes 1300
  max_time: { type: Types.Minute, min: 0, max: 300 }, // 10UL for min?
};

const point = {
  // OP Codes 1400
  max_time: { type: Types.Minute },
};

const detumble = {
  // OP Codes 1500
  start_time: { type: Types.Int },
  max_time: { type: Types.Hour },

  min_stable_gyro_z: { type: Types.Float, min: 0, max: 2 },
  max_stable_gyro_x: { type: Types.Float, min: 0, max: 1 },
  max_stable_gyro_y: { type: Types.Float, min: 0, max: 1 },

  min_unstable_gyro_x: { type: Types.Float, min: 0, max: 1 },
  min_unstable_gyro_y: { type: Types.Float, min: 0, max: 1 },
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
  mode: { type: Types.Int, min: 0, max: 2 },
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

  init_mode: { type: Types.Int, min: 0, max: 3 },
  mode: { type: Types.Int, min: 0, max: 2 },

  images_written: { type: Types.Int },
  fragments_written: { type: Types.Int },

  set_res: "uint32_t", // Adafruit_VC0706.h: VC0706_160x120 ?

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
  imu_downlink_remain_time: { type: Types.Minute },
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

  downlink_report_type: { type: Types.Int, min: 0, max: 2 },
  mode: { type: Types.Int, min: 0, max: 22 },
};

const imu = {
  // OP Codes 2200
  mode: { type: Types.Int, min: 0, max: 2 },
  init_mode: { type: Types.Int, min: 0, max: 3 },

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

  mag: { type: Types.Int, min: 0, max: 2 },
};

const battery = {
  // OP Codes 2600
  acceptable_battery: { type: Types.Float },
  min_battery: { type: Types.Float },
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
  error_mode_reset: { type: Types.MultiInt }
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
