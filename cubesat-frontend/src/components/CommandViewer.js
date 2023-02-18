import { Button, Col, Container, Row } from "react-bootstrap";
import { createRef, useRef, useState } from "react";
import InputField from "./InputField";
import Form from "react-bootstrap/Form";
import { useDashboard } from "../contexts/DashboardProvider";
import { burnwire_arm_true, rockblock_downlink_period } from "./Commands";

// Command Viewer
// Shows the title and description for a selected command.
// Allows user to enter in command arguments (if they exist) and create commands.
export default function CommandViewer() {
  // declare shared variables
  const {
    selectedCommand: command,
    setSelectedCommand,
    commandStack,
    setCommandStack,
    count,
    setCount,
  } = useDashboard();

  // check if a command is selected
  const commandSelected = Object.keys(command).length !== 0;

  // store form errors and input field references
  const [formErrors, setFormErrors] = useState({});
  const fieldRefs = useRef([]);

  // fill input references list with empty references
  const numFields = command.fields ? command.fields.length : 0;
  if (fieldRefs.current.length !== numFields) {
    fieldRefs.current = Array(numFields)
      .fill()
      .map((_, i) => fieldRefs.current[i] || createRef());
  }

  const onSubmit = (ev) => {
    ev.preventDefault();

    // validate form inputs and return if fields are invalid
    let errors = {};
    let fieldsBody = {};
    for (let field of fieldRefs.current) {
      if (!field.current.value) {
        errors[field.current.id] = "Field must not be empty.";
      } else {
        fieldsBody[field.current.id] = field.current.value;
      }
    }
    setFormErrors(errors);
    if (Object.keys(errors).length > 0) return;

    // append to command stack
    let new_command = {
      id: count,
      name: command.name,
      title: command.title,
      fields: fieldsBody,
    };
    setCommandStack([...commandStack, new_command]);
    setCount(count + 1);

    // for testing
    if (command !== rockblock_downlink_period)
      setSelectedCommand(rockblock_downlink_period);
    else setSelectedCommand(burnwire_arm_true);
  };

  return (
    <>
      <h3>{commandSelected ? command.title : "No Command Selected"}</h3>
      <hr />
      <Container fluid className="p-0">
        <Row>
          <Col sm="8">
            <h5>Description</h5>
            <p>{commandSelected ? command.description : "Select a command."}</p>
          </Col>
          {/* Command Input Fields + Submission */}
          <Col sm="4">
            <Form onSubmit={onSubmit}>
              {numFields > 0 && <b>Fields</b>}
              {numFields > 0 &&
                command.fields.map((field, i) => (
                  <InputField
                    className="mb-2"
                    key={field.title}
                    name={"field" + i}
                    label={field.title}
                    type="number"
                    error={formErrors["field" + i]}
                    fieldRef={fieldRefs.current[i]}
                  />
                ))}
              <Button
                variant="secondary"
                type="submit"
                disabled={!commandSelected}
              >
                Append Command
              </Button>
            </Form>
          </Col>
        </Row>
      </Container>
    </>
  );
}
