// Command Opcodes and descriptions
export const OpCodes = Object.freeze({
  Deploy: "Deploy",
  Arm: "Arm",
  Fire: "Fire",
  SFR_Override: "SFR_Override",
  Fault: "Fault",
  Fragment_Request: "Fragment_Request",
  EEPROM_Reset: "EEPROM_Reset",
});

export const opcodeDesc = {
  Deploy: "Move the CubeSat into the Deployment phase.",
  Arm: "Move the CubeSat into the Armed phase.",
  Fire: "Move the CubeSat into the In Sun phase.",
  SFR_Override: "Override the selected SFR field with the provided value.",
  Fault: "Force, suppress, or restore the selected fault.",
  Fragment_Request: "Request an ODS capture fragment.",
  EEPROM_Reset: "Reset the EEPROM metadata with the provided values.",
};

// SFR field types
export const SFR_Type = Object.freeze({
  Int: "INT",
  Float: "FLOAT",
  Time: "TIME",
  Bool: "BOOL",
});

// Rockblock IMEIs
export const IMEI_MAP = {
  300534061570670: "OG FlatSat",
  300234064326340: "New FlatSat",
};

// Telemetry report types
export const report_types = {
  99: "Normal",
  24: "IMU",
  42: "ODS",
  "-1": "Error",
};

// Base URL for viewing normal reports in Kibana
export const kibanaNRBase = `${process.env.REACT_APP_KIBANA_URL}/app/discover#/doc/${process.env.REACT_APP_KIBANA_NR_DOC_ID}/cubesat_normal_report?id=`;

export const isDeploymentOpcode = (opcode) =>
  opcode === OpCodes.Deploy ||
  opcode === OpCodes.Arm ||
  opcode === OpCodes.Fire;

export function stringifyCommand(command) {
  let data = command.value;
  if (
    command.opcode === OpCodes.SFR_Override ||
    command.opcode === OpCodes.Fault
  ) {
    return `${command.namespace}::${command.field} = ${command.opcode === OpCodes.SFR_Override ? data.value : data
      }`;
  } else if (command.opcode === OpCodes.Fragment_Request) {
    return `${data.type}: Fragment ${data.fragmentNum +
      (data.type === "Capture" ? ", Serial " + data.serialNum : "")
      }`;
  } else if (command.opcode === OpCodes.EEPROM_Reset) {
    return `Boot count: ${data.bootCount}, Light: ${data.lightSwitch}, 
    SFR addr: ${data.sfrAddress}, Data addr: ${data.dataAddress}, 
    SFR age: ${data.sfrWriteAge}, Data age: ${data.dataWriteAge}`;
  }
}