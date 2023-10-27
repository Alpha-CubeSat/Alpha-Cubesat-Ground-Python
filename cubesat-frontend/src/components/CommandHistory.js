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

  function isNested(subArr, parentArr) {
    return parentArr.some(
      (innerArr) =>
        subArr.length === innerArr.length &&
        subArr.every((elem, idx) => elem === innerArr[idx])
    );
  }

  // function logsEqual(array1, array2) {
  //   if (array1.length !== array2.length) {
  //     return false
  //   }
  //   for (let i = 0; i < array1.length; i++) {
  //     if (array1[i] !== array2[i]) {
  //       return false;
  //     }
  //   }
  //   return true;
  // }

  const checkCommandHistory = useCallback(async () => {
    // automatically fetch previous command history (without processed)
    console.log("fetching command history");
    await api
      .get("/cubesat/command_history/" + imei)
      .then((response) =>
        setCommandLog(response.status === 200 ? response.data : [])
      );
  }, [api, imei, setCommandLog]);

  const checkProcessed = useCallback(async () => {
    console.log("fetching processed opcodes");
    await api.get("/cubesat/processed_commands/" + imei).then((response) => {
      const dataList = response["data"][0][-1];
      const sfrList = [];
      const opcodeList = [];
      for (let item of dataList) {
        if (item.includes("::")) {
          sfrList.push([
            item.substring(0, item.indexOf(":")),
            item.substring(item.indexOf(":") + 2),
          ]);
        } else {
          opcodeList.push(item);
        }
      }
      for (let i = commandLog.length - 1; i >= 0; i--) {
        for (let command of commandLog[i].commands) {
          if (opcodeList.includes(command["opcode"])) {
            command["processed"] = "true";
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
          }
          setCommandLog(commandLog);
        }
      }
    });
  }, [api, commandLog, setCommandLog, imei]);

  // Checks whether a command has appeared in the command log of the downlinked normal report
  useEffect(() => {
    // Poll every 5000 milliseconds (5 seconds)
    const interval = setInterval(() => {
      checkCommandHistory();
      //checkProcessed();
    }, 5000);

    // Cleanup: clear the interval when the component is unmounted or the effect re - runs
    return () => {
      clearInterval(interval);
    };
  }, [checkProcessed, checkCommandHistory]);

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
