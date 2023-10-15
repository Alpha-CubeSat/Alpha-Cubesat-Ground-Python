import { createContext, useContext, useEffect, useState } from "react";
import { useApi } from "./ApiProvider";
import { IMEI_MAP } from "../constants";

const DashboardContext = createContext();

// Dashboard Context Provider
// Contains variables shared across different widgets to make access/updating easier.
export default function DashboardProvider({ children }) {
  const api = useApi();

  // current list of commands to send
  const [commandStack, setCommandStack] = useState([]);

  // list of disabled opcodes based on current commands in command card
  const [disabledOpcodes, setDisabledOpcodes] = useState([]);

  // notify command log of API response when user sends command
  const [commandLog, setCommandLog] = useState([]);

  // automatically fetch previous command history when ground station is first loaded
  useEffect(() => {
    api
      .get("/cubesat/command_history")
      .then((response) =>
        setCommandLog(response.status === 200 ? response.data : [])
      );
  }, [api]);

  // ensure commands have unique keys
  const [count, setCount] = useState(0);

  // cubesat imei to send commands to
  const [imei, setImei] = useState(Object.keys(IMEI_MAP)[0]);

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
        setDisabledOpcodes,
        imei,
        setImei,
      }}
    >
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  return useContext(DashboardContext);
}
