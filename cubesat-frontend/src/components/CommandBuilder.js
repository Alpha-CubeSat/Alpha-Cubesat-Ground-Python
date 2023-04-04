import { Container } from "react-bootstrap";
import CommandList from "./CommandList";
import CommandActions from "./CommandActions";

// Command Builder
// Allows the user to string multiple commands to send to the CubeSat at the same time.
// Drag and drop interface allows easy reordering + deletion of commands.
// Allows user to send commands and clear current commands.
export default function CommandBuilder() {
  return (
    <>
      <Container className="p-0 h-100 d-flex flex-column">
        <h5>New Command</h5>
        <hr />
        {/* Current list of commands to send to cubesat */}
        <Container className="p-0 flex-fill overflow-auto scrollbar-small">
          <CommandList />
        </Container>
        {/* Clear and send command buttons */}
        <Container className="p-0 justify-content-end">
          <hr />
          <CommandActions />
        </Container>
      </Container>
    </>
  );
}
