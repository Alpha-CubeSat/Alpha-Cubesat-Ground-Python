import { Table } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import { useCallback, useEffect } from "react";
import LogRow from "./LogRow";
import { useApi } from "../contexts/ApiProvider";

// Command History Log
// Shows a log of all previously sent commands to the CubeSat with each command's status, name,
// submission time, and API response message.
export default function CommandLog() {
  const { commandLog, setCommandLog } = useDashboard();

  const api = useApi();
  const checkProcessed = useCallback(async () => {
    await api.get("/cubesat/processed_commands").then((response) => {
      const dataList = response["data"][response["data"].length - 1];
      const sfrList = [];
      for (let item of dataList) {
        if (item.includes(":")) {
          sfrList.push(
            item.substr(0, item.indexOf(" :")),
            item.substr(item.indexOf(":") + 2)
          );
        }
      }
      const newCommandLog = JSON.parse(JSON.stringify(commandLog));
      for (let logEntry of newCommandLog) {
        for (let command of logEntry.commands) {
          if (
            !("processed" in command) &&
            (dataList.includes(command["opcode"].toLowerCase()) ||
              (sfrList.includes(command["namespace"]) &&
                sfrList.includes(command["field"])))
          ) {
            command["processed"] = "true";
          }
        }
      }
      setCommandLog(newCommandLog);
    });
  }, [api, commandLog, setCommandLog]);

  // Checks whether a command has appeared in the command log of the downlinked normal report
  useEffect(() => {
    // Poll every 10000 milliseconds (10 seconds)
    const interval = setInterval(() => {
      checkProcessed();
    }, 5000);

    // Cleanup: clear the interval when the component is unmounted or the effect re - runs
    return () => {
      clearInterval(interval);
    };
  }, [checkProcessed]);

  return (
    <Table hover>
      <thead>
        <tr className="table-secondary">
          <th>Status</th>
          <th>Command(s)</th>
          <th>Processed</th>
          <th>Sent</th>
          <th>Message</th>
        </tr>
      </thead>
      <tbody>
        {commandLog.map((entry, i) => (
          <LogRow key={i} entry={entry} />
        ))}
      </tbody>
    </Table>
  );
}
