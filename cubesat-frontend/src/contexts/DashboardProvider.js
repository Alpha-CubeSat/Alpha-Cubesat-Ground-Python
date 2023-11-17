import { createContext, useContext, useEffect, useState } from "react";
import { useApi } from "./ApiProvider";
import { IMEI_MAP } from "../constants";
import ConfirmModal from "../components/ConfirmModal";
import { toast } from "react-toastify";

const DashboardContext = createContext();

// Dashboard Context Provider
// Contains variables shared across different widgets to make access/updating easier.
export default function DashboardProvider({ children }) {
  const api = useApi();

  // rockblock imei to send commands to (used last value from local storage if it exists)
  const [imei, setImei] = useState(
    localStorage.getItem("IMEI")
      ? localStorage.getItem("IMEI")
      : Object.keys(IMEI_MAP)[0]
  );

  // current list of commands to send
  const [commandStack, setCommandStack] = useState([]);

  // list of disabled opcodes based on current commands in command card
  const [disabledOpcodes, setDisabledOpcodes] = useState([]);

  // notify command log of API response when user sends command
  const [commandLog, setCommandLog] = useState(undefined);

  // automatically fetch previous command history when first loaded or imei updated
  useEffect(() => {
    setCommandLog(undefined);
    api
      .get("/cubesat/command_history/" + imei)
      .then((response) =>
        setCommandLog(response.status === 200 ? response.data : [])
      );
  }, [api, imei]);

  // ensure commands have unique keys
  const [count, setCount] = useState(0);

  const [reqNotifShow, setReqNotifShow] = useState(false);

  // show notification permission request modal if permission has not been previously granted
  useEffect(() => {
    if ("Notification" in window && Notification.permission !== "granted") {
      setReqNotifShow(true);
    }
  }, []);

  const reqNotificationPermission = () => {
    Notification.requestPermission().then((res) => {
      console.log("Notifications: " + res);
      // res will always be denied if user explicitly blocks notifications, in that case
      // they will have to go into browser settings to manually allow them
      if (res === "granted") {
        new Notification("Notifications have been enabled.");
      } else {
        toast.error("Notification permission denied.");
      }
    });
  };

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
      <ConfirmModal
        heading="Enable Notifications"
        body={
          'Click "Continue" to receive notifications when new reports are received.'
        }
        show={reqNotifShow}
        setShow={setReqNotifShow}
        onConfirm={reqNotificationPermission}
      />
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  return useContext(DashboardContext);
}
