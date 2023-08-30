import { Table } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import { useEffect } from "react";
import LogRow from "./LogRow";

// Command History Log
// Shows a log of all previously sent commands to the CubeSat with each command's status, name,
// submission time, and API response message.
export default function CommandLog() {
  const { commandLog, setCommandLog } = useDashboard();

  // Checks whether a command has appeared in the command log of the downlinked normal report
  // const checkProcessed = async () => {
  //   axios.get('/cubesat/commandLog', commandLog).then(response => {
  //     const newCommandLog = JSON.parse(JSON.stringify(commandLog));
  //     for (let logEntry of newCommandLog) {
  //       for (let command of logEntry.commands) {
  //         if (response.opcode === command.opcode && response.namespace === opcode.namespace
  //           && response.value === command.value) {
  //           command.processed = "true";
  //         }
  //       }
  //     }
  //     setCommandLog(newCommandLog)
  //   })
  // };

  // useEffect(() => {
  //   // Poll every 5000 milliseconds (5 second)
  //   const interval = setInterval(() => {
  //     checkProcessed();
  //   });
  // }, 5000);

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