import { useDashboard } from "../contexts/DashboardProvider";
import { Button } from "react-bootstrap";
import ConfirmModal from "./ConfirmModal";
import { useState } from "react";

// Command Actions (component of CommandBuilder)
// Allows user to send commands and clear current commands.
// Send and clear actions protected by confirmation modal to prevent accidental clicks.
export default function CommandActions() {
  const { commandStack, setCommandStack, commandLog, setCommandLog } =
    useDashboard();

  // confirmation dialog states
  const [sendShow, setSendShow] = useState(false);
  const [clearShow, setClearShow] = useState(false);

  const commandsStacked = commandStack.length !== 0;

  const clearCommands = () => setCommandStack([]);

  const sendCommands = (async) => {
    let api_response = [];
    for (let command of commandStack) {
      let error = Math.random() > 0.75;
      api_response.push({
        id: command.id,
        name: command.name,
        fields: command.fields,
        submitted: new Date().toLocaleString(),
        status: !error ? "success" : "failure",
        message: !error
          ? "command successfully transmitted"
          : "connection timed out",
      });
    }
    setCommandLog([...api_response.reverse(), ...commandLog]);

    // clear commands
    setCommandStack([]);
  };

  return (
    <>
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
