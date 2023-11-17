import { BsCheckCircleFill, BsXCircleFill } from "react-icons/bs";
import { Spinner, Table } from "react-bootstrap";
import { useEffect, useRef, useState } from "react";
import { useApi } from "../contexts/ApiProvider";
import { IMEI_MAP } from "../constants";
import { FiExternalLink } from "react-icons/fi";

// Downlink History Log
// Shows a log of all downlinks received from the Rockblock portal and processed by the ground station
export default function DownlinkHistory() {
  const api = useApi();
  const [history, setHistory] = useState();
  const [autoRefetchLoading, setAutoRefetchLoading] = useState(false);

  const kibanaNRBase = `${process.env.REACT_APP_KIBANA_URL}/app/discover#/doc/${process.env.REACT_APP_KIBANA_NR_DOC_ID}/cubesat_normal_report?id=`;

  const report_types = {
    99: "Normal",
    24: "IMU",
    42: "Camera",
    "-1": "Error",
  };

  // Fetch downlink history and update periodically (every 10 seconds)
  useInterval(async () => {
    console.log("updating history");
    // remember last history entry before refreshing
    const beforeHistory = history
      ? JSON.parse(JSON.stringify(history[0]))
      : undefined;

    setAutoRefetchLoading(true);
    const response = await api.get("/cubesat/downlink_history");
    const data = response.status === 200 ? response.data : [];
    setHistory(data);
    setAutoRefetchLoading(false);

    // if not first time and transmit_time of first history entry is different,
    // send new report notification
    if (
      beforeHistory &&
      beforeHistory["transmit_time"] !== data[0]["transmit_time"]
    ) {
      console.log("new report detected");
      new Notification(
        `New ${
          report_types[data[0]["telemetry_report_type"]]
        } report received from ${IMEI_MAP[data[0]["imei"]]}`
      );
    }
  }, 10000);

  return (
    <>
      {history === undefined ? (
        <Spinner animation="border" />
      ) : (
        <>
          {/* show message when auto-refreshing history */}
          {autoRefetchLoading && (
            <div className="mb-2">
              <span>Updating...</span>
              <Spinner animation="border" size="sm" className="ms-2" />
            </div>
          )}

          <Table hover>
            <thead>
              <tr className="table-secondary">
                <th>Status</th>
                <th>Type</th>
                <th>IMEI</th>
                <th>Transmit Time</th>
              </tr>
            </thead>

            <tbody>
              {history.map((entry, i) => (
                <tr key={i}>
                  {/* status indicator, show error msg on hover */}
                  <td>
                    {entry["error"] ? (
                      <BsXCircleFill
                        color="red"
                        title={
                          entry["error"]?.split("\n")[
                            entry["error"].split("\n").length - 2
                          ]
                        }
                      />
                    ) : (
                      <BsCheckCircleFill color="green" />
                    )}
                  </td>
                  {/* report type, include link to NR if it exists */}
                  <td>
                    {entry["normal_report_id"] ? (
                      <a
                        href={kibanaNRBase + entry["normal_report_id"]}
                        target="_blank"
                        rel="noreferrer"
                        title="View normal report"
                      >
                        {report_types[entry["telemetry_report_type"]]}
                        <FiExternalLink className="ms-1" />
                      </a>
                    ) : (
                      report_types[entry["telemetry_report_type"]]
                    )}
                  </td>
                  {/* IMEI and transmit_time */}
                  <td>{IMEI_MAP[entry["imei"]]}</td>
                  <td>{new Date(entry["transmit_time"]).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </>
      )}
    </>
  );
}

// Allows setInterval() to work with React useState() and useEffect() hooks
// https://overreacted.io/making-setinterval-declarative-with-react-hooks/
function useInterval(callback, delay) {
  const savedCallback = useRef();

  // Remember the latest callback.
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval.
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      let id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
}
