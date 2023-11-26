import { Spinner, Table } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import { useCallback, useEffect } from "react";
import LogRow from "./LogRow";
import { useApi } from "../contexts/ApiProvider";

// Command History Log
// Shows a log of all previously sent commands to the CubeSat with each command's status, name,
// submission time, and API response message.
export default function CommandHistory() {
  const { commandLog, setCommandLog } = useDashboard();
  const { imei } = useDashboard();

  const api = useApi();

  const checkProcessed = useCallback(async () => {
    console.log("fetching processed opcodes");
    await api.get("/cubesat/processed_commands/" + imei).then((response) => {
      const dataList = response["data"];
      const newCommandLog = JSON.parse(JSON.stringify(commandLog));
      let accum = 0;
      for (let i = newCommandLog.length - 1; i >= 0; i--) {
        for (let command of newCommandLog[i].commands) {
          if (dataList[accum] === 1) {
            command["processed"] = "true";
          }
          accum++;
        }
      }
      setCommandLog(newCommandLog);
    });
  }, [api, commandLog, setCommandLog, imei]);

  // Checks whether a command has appeared in the command log of the downlinked normal report
  useEffect(() => {
    // Poll every 5000 milliseconds (5 seconds)
    const interval = setInterval(() => {
      checkProcessed();
    }, 5000);

    // Cleanup: clear the interval when the component is unmounted or the effect re - runs
    return () => {
      clearInterval(interval);
    };
  }, [checkProcessed]);

  return (
    <>
      {commandLog === undefined ? (
        <Spinner animation="border" />
      ) : (
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
      )}
    </>
  );
}
