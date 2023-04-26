import { createContext, useContext, useState } from "react";

const DashboardContext = createContext();

// Dashboard Context Provider
// Contains variables shared across different widgets to make access/updating easier.
export default function DashboardProvider({ children }) {
  // current list of commands to send
  const [commandStack, setCommandStack] = useState([]);

  // list of disabled opcodes based on current commands in command card
  const [disabledOpcodes, setDisabledOpcodes] = useState([]);

  // ***grab prev command history from api on initial render

  // notify command log of API response when user sends command
  const [commandLog, setCommandLog] = useState([
    {
      status: "success",
      timestamp: "1677363088399.2676",
      commands: [
        {
          opcode: "SFR_Override",
          namespace: "camera",
          field: "turn_on",
          value: "true",
        },
        {
          opcode: "SFR_Override",
          namespace: "burnwire",
          field: "burn_time",
          value: "10000",
        },
        {
          opcode: "Deploy",
        },
      ],
      error_code: "",
      error_message: "",
    },
  ]);

  // ensure lists have unique keys
  const [count, setCount] = useState(0);

  return (
    <DashboardContext.Provider
      value={{
        commandLog,
        setCommandLog,
        commandStack,
        setCommandStack,
        count,
        setCount,
        disabledOpcodes,
        setDisabledOpcodes
      }}
    >
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  return useContext(DashboardContext);
}
