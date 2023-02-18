import { createContext, useContext, useState } from "react";
import { burnwire_arm_time } from "../components/Commands";

const DashboardContext = createContext();

// Dashboard Context Provider
// Contains variables shared across different widgets to make access/updating easier.
export default function DashboardProvider({ children }) {
  // notify command viewer when user selects command
  const [selectedCommand, setSelectedCommand] = useState(burnwire_arm_time);

  // current list of commands to send
  const [commandStack, setCommandStack] = useState([]);

  // ***grab prev command history from api on initial render

  // notify command log of API response when user sends command
  const [commandLog, setCommandLog] = useState([
    {
      id: -3,
      name: "mission_mode_low_power",
      fields: [],
      submitted: new Date().toLocaleString(),
      status: "success",
      message: "command successfully transmitted",
    },
    {
      id: -2,
      name: "burnwire_burn_time",
      fields: [],
      submitted: new Date().toLocaleString(),
      status: "failure",
      message: "connection timed out",
    },
    {
      id: -1,
      name: "take_photo_true",
      fields: [],
      submitted: new Date().toLocaleString(),
      status: "failure",
      message: "connection timed out",
    },
  ]);

  // ensure lists have unique keys
  const [count, setCount] = useState(0);

  return (
    <DashboardContext.Provider
      value={{
        selectedCommand,
        setSelectedCommand,
        commandLog,
        setCommandLog,
        commandStack,
        setCommandStack,
        count,
        setCount,
      }}
    >
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  return useContext(DashboardContext);
}
