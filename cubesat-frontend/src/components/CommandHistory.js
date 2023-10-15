import { Table } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import { useCallback, useEffect } from "react";
import LogRow from "./LogRow";
import { useApi } from "../contexts/ApiProvider";

// Command History Log
// Shows a log of all previously sent commands to the CubeSat with each command's status, name,
// submission time, and API response message.
export default function CommandHistory() {
  const { commandLog, setCommandLog } = useDashboard();

  const api = useApi();

  function isNested(subArr, parentArr) {
    return parentArr.some(
      (innerArr) =>
        subArr.length === innerArr.length &&
        subArr.every((elem, idx) => elem === innerArr[idx])
    );
  }

  const checkProcessed = useCallback(async () => {
    console.log("fetching processed opcodes");
    await api.get("/cubesat/processed_commands").then((response) => {
      const dataList = response["data"];
      const sfrList = [];
      const opcodeList = [];
      for (let data in dataList) {
        for (let item of dataList[data]) {
          if (item.includes("::")) {
            sfrList.push([
              item.substr(0, item.indexOf(":")),
              item.substr(item.indexOf(":") + 2),
            ]);
          } else {
            opcodeList.push(item);
          }
        }
      }
      const newCommandLog = JSON.parse(JSON.stringify(commandLog));
      for (let i = newCommandLog.length - 1; i >= 0; i--) {
        let logEntry = newCommandLog[i];
        for (let command of logEntry.commands) {
          if (opcodeList.includes(command["opcode"])) {
            command["processed"] = "true";
            setCommandLog(newCommandLog);
            let index = opcodeList.indexOf(command["opcode"]);
            opcodeList.splice(index, 1);
          } else if (
            isNested([command["namespace"], command["field"]], sfrList)
          ) {
            command["processed"] = "true";
            let index = sfrList.indexOf(command["namespace"]);
            sfrList.splice(index, 1);
            let index2 = sfrList.indexOf(command["field"]);
            sfrList.splice(index2, 1);
            setCommandLog(newCommandLog);
          }
        }
      }
    });
  }, [api, commandLog, setCommandLog]);

  // Checks whether a command has appeared in the command log of the downlinked normal report
  useEffect(() => {
    // Poll every 10000 milliseconds (10 seconds)
    const interval = setInterval(() => {
      checkProcessed();
    }, 10000);

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
