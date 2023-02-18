import { Table } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import LogRow from "./LogRow";

// Command History Log
// Shows a log of all previously sent commands to the CubeSat with each command's status, name,
// submission time, and API response message.
export default function CommandLog() {
  const { commandLog } = useDashboard();

  return (
    <Table hover>
      <thead>
        <tr className="table-secondary">
          <th>Status</th>
          <th>Command</th>
          <th>Submitted</th>
          <th>Message</th>
        </tr>
      </thead>
      <tbody>
        {commandLog.map((entry) => (
          <LogRow key={entry.id} entry={entry} />
        ))}
      </tbody>
    </Table>
  );
}
