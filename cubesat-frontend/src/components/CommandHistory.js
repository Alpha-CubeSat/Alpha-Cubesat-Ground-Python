import { Spinner, Table } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import { useEffect } from "react";
import LogRow from "./LogRow";
import { useApi } from "../contexts/ApiProvider";

// Command History Log
// Shows a log of all previously sent commands to the CubeSat with each command's status, name,
// submission time, and API response message.
export default function CommandHistory() {
  const { commandLog, setCommandLog } = useDashboard();
  const { imei } = useDashboard();

  const api = useApi();

  useEffect(() => {
    const interval = setInterval(() => {
      api.get("/cubesat/command_history/" + imei)
        .then((response) =>
          setCommandLog(response.status === 200 ? response.data : [])
        );
    }, 5000);
    return () => {
      clearInterval(interval);
    };
  }, [api, imei, setCommandLog]);


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
