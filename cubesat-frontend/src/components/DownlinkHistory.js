import { Spinner, Table } from "react-bootstrap";
import { useCallback, useEffect, useState } from "react";
import { useApi } from "../contexts/ApiProvider";

// Downlink History Log
// Shows a log of all downlinks received from the Rockblock portal and processed by the ground station
export default function DownlinkHistory() {
  const api = useApi();
  const [history, setHistory] = useState();

  const report_types = {
    99: "Normal",
    24: "IMU",
    42: "Camera",
    "-1": "Error",
  };

  const checkHistory = useCallback(async () => {
    const response = await api.get("/cubesat/downlink_history");
    setHistory(response.status === 200 ? response.data : []);
  }, [api]);

  // Fetch downlink history and update periodically
  useEffect(() => {
    // Poll every 10000 milliseconds (10 seconds)
    const interval = setInterval(async () => {
      console.log("updating history");
      setHistory(undefined);
      await checkHistory();
    }, 10000);

    // Cleanup: clear the interval when the component is unmounted or the effect reruns
    return () => {
      clearInterval(interval);
    };
  }, [checkHistory]);

  return (
    <>
      {history === undefined ? (
        <Spinner animation="border" />
      ) : (
        <Table hover>
          <thead>
            <tr className="table-secondary">
              <th>Type</th>
              <th>Transmit Time</th>
              <th>Error Message</th>
            </tr>
          </thead>

          <tbody>
            {history.map((entry, i) => (
              <tr key={i}>
                <td>{report_types[entry["telemetry_report_type"]]}</td>
                <td>{new Date(entry["transmit_time"]).toLocaleString()}</td>
                <td>
                  {
                    entry["error"]?.split("\n")[
                      entry["error"].split("\n").length - 2
                    ]
                  }
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </>
  );
}
