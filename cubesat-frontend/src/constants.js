// Command Opcodes
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
  Fragment_Request: "Request an image or IMU fragment.",
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
    return `${command.namespace}::${command.field} = ${
      command.opcode === OpCodes.SFR_Override ? data.value : data
    }`;
  } else if (command.opcode === OpCodes.Fragment_Request) {
    return `${data.type}: Fragment ${
      data.fragmentNum +
      (data.type === "Image" ? ", Serial " + data.serialNum : "")
    }`;
  } else if (command.opcode === OpCodes.EEPROM_Reset) {
    return `Boot count: ${data.bootCount}, Light: ${data.lightSwitch}, 
    SFR addr: ${data.sfrAddress}, Data addr: ${data.dataAddress}, 
    SFR age: ${data.sfrWriteAge}, Data age: ${data.dataWriteAge}`;
  }
}
