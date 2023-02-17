import {Table} from "react-bootstrap";
import {BsCheckCircleFill, BsXCircleFill} from "react-icons/bs";
import {useDashboard} from "../contexts/DashboardProvider";

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
          <tr key={entry.id}>
            <td>
              {entry.status === "success" ? (
                <BsCheckCircleFill color="green" />
              ) : (
                <BsXCircleFill color="red" />
              )}
            </td>
            <td>{entry.name}</td>
            <td>{entry.submitted}</td>
            <td>{entry.message}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}
