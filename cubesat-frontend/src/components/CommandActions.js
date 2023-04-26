import { useDashboard } from "../contexts/DashboardProvider";
import { Button } from "react-bootstrap";
import ConfirmModal from "./ConfirmModal";
import { useState } from "react";
import { useApi } from "../contexts/ApiProvider";

// Command Actions (component of CommandBuilder)
// Allows user to send commands and clear current commands.
// Send and clear actions protected by confirmation modal to prevent accidental clicks.
export default function CommandActions() {
  const { commandStack, setCommandStack, commandLog, setCommandLog, setDisabledOpcodes } =
    useDashboard();
  const api = useApi();

  // confirmation dialog states
  const [sendShow, setSendShow] = useState(false);
  const [clearShow, setClearShow] = useState(false);

  const commandsStacked = commandStack.length !== 0;

  const clearCommands = () => {
    setCommandStack([]);
    setDisabledOpcodes([])
  }

  const sendCommands = async () => {
    // build api request to send commands
    let request_body = [];
    // remove id field from properties
    for (let { id: omitted, ...rest } of commandStack) {
      request_body.push(rest);
    }

    // TODO: show spinner while commands are being sent
    const response = await api.post("/cubesat/command", request_body);
    console.log(response.data);

    // update command log
    setCommandLog([response.data, ...commandLog]);

    // clear commands
    setCommandStack([]);

    // allow any opcode selection
    setDisabledOpcodes([]);
  };

  return (
    <>
      {/* Clear commands button + confirmation dialog */}
      <Button
        variant="danger"
        disabled={!commandsStacked}
        onClick={() => setClearShow(true)}
        className="mb-2"
      >
        Clear Commands
      </Button>
      <ConfirmModal
        heading="Clear Commands"
        body={
          "Are you sure you want to clear " +
          commandStack.length +
          " command(s)?"
        }
        show={clearShow}
        setShow={setClearShow}
        onConfirm={clearCommands}
      />

      {/* Send commands button + confirmation dialog */}
      <Button
        variant="success"
        disabled={!commandsStacked}
        onClick={() => setSendShow(true)}
      >
        Send Commands
      </Button>
      <ConfirmModal
        heading="Send Commands"
        body={
          "Are you sure you want to send " +
          commandStack.length +
          " command(s)?"
        }
        show={sendShow}
        setShow={setSendShow}
        onConfirm={sendCommands}
      />
    </>
  );
}
