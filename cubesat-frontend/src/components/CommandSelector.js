import { useEffect, useRef, useState } from "react";
import Dropdown from "react-bootstrap/Dropdown";
import { Button, Col, Container, Row } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import { useApi } from "../contexts/ApiProvider";
import {
  EepromReset,
  Fault,
  FragmentRequest,
  MissionModeOverride,
  SfrOverride,
} from "./CommandForms";
import { isDeploymentOpcode, opcodeDesc, OpCodes } from "../constants";

// Command Selector
// Has dropdown menus for user to build a command to be sent to the CubeSat
// Dropdowns for SFR namespace and field are searchable to improve usability
// Supports multiple types command arguments (ints, floats, booleans, time) and min/max checking
// Shows the title and description for a selected command
export default function CommandSelector() {
  const {
    commandStack,
    setCommandStack,
    count,
    setCount,
    disabledOpcodes,
    setDisabledOpcodes,
  } = useDashboard();

  const api = useApi();

  /*
  Command selector: title, description, opcode selector, "add command" button
  also manages the currently selected opcode, displays the corresponding form and passes in its command data,
  calls the form's onSubmit function when "add command" is pressed

  Command forms:
  command-specific html (like namespace/field dropdowns for sfr)
  command-specific onSubmit logic that verifies command validity when "add command" pressed
   */

  const [allCommandMetadata, setAllCommandMetadata] = useState({});

  // fetch metadata for all commands
  useEffect(() => {
    api
      .get("/cubesat/command_data")
      .then((response) =>
        setAllCommandMetadata(response.status === 200 ? response.data : {})
      );
  }, [api]);

  const [selectedOpCode, setOpCode] = useState("None");

  // Argument input form for currently selected command opcode
  const [currentForm, setCurrentForm] = useState(<div></div>);
  const formRef = useRef();

  // Command title and description
  const [title, setTitle] = useState("No command selected");
  const [desc, setDesc] = useState("Select a command");

  // Updates command form based on selected opcode
  const handleOpCodeSelect = (opcode) => () => {
    setOpCode(opcode);

    if (opcode === OpCodes.SFR_Override) {
      setCurrentForm(
        <SfrOverride
          SFR_Data={allCommandMetadata["SFR_Override"]}
          setTitle={setTitle}
          ref={formRef}
        />
      );
    } else if (opcode === OpCodes.EEPROM_Reset) {
      setCurrentForm(<EepromReset ref={formRef} />);
    } else if (isDeploymentOpcode(opcode)) {
      setCurrentForm(<div></div>);
    } else if (opcode === OpCodes.Fault) {
      setCurrentForm(
        <Fault
          Fault_Data={allCommandMetadata["Faults"]}
          setTitle={setTitle}
          ref={formRef}
        />
      );
    } else if (opcode === OpCodes.Fragment_Request) {
      setCurrentForm(<FragmentRequest ref={formRef} />);
    } else if (opcode === OpCodes.Mission_Mode_Override) {
      setCurrentForm(
        <MissionModeOverride
          MM_Data={allCommandMetadata["Mission_Mode_Override"]}
          ref={formRef}
        />)
    }

    setTitle(opcode);
    setDesc(opcodeDesc[opcode]);
  };

  // Validates input field before adding command to the command builder
  const handleSubmit = () => {
    let data;
    if (!isDeploymentOpcode(selectedOpCode)) {
      // call child onSubmit to validate input, if it is valid the command will be returned
      data = formRef.current.handleSubmit();
      if (data === undefined) return;
    }

    // add to command builder
    let new_command = {
      id: count,
      opcode: selectedOpCode,
      ...(!isDeploymentOpcode(selectedOpCode) && data),
    };
    setCommandStack([...commandStack, new_command]);
    setCount(count + 1);

    // Allows only one deployment command to be sent at a time
    if (
      new_command["opcode"] === "Deploy" ||
      new_command["opcode"] === "Arm" ||
      new_command["opcode"] === "Fire"
    ) {
      setDisabledOpcodes(["Deploy", "Arm", "Fire"]);
    }

    // reset
    setOpCode("None");
    setTitle("No command selected");
    setDesc("Select a command");
    setCurrentForm(<div></div>);
  };

  return (
    <Container>
      {/* Command Title and Description */}
      <Row>
        <h4>
          {title !== "No Command Selected" ? title : "No Command Selected"}
        </h4>
        <p>{desc}</p>
        <hr />
      </Row>

      {/* Opcode dropdown selection */}
      <Row className="d-flex flex-wrap">
        <Col className="col-md-4">
          <span style={{ fontWeight: "bold" }}>Opcode</span>
          <Dropdown className="position-absolute">
            <Dropdown.Toggle variant="success" id="dropdown-basic">
              {selectedOpCode}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {Object.keys(OpCodes).map((option, index) => (
                <Dropdown.Item
                  key={index}
                  disabled={disabledOpcodes.includes(option)}
                  onClick={handleOpCodeSelect(option)}
                >
                  {option}
                </Dropdown.Item>
              ))}
            </Dropdown.Menu>
          </Dropdown>
        </Col>
        <Col>
          {/* Command form for selected opcode */}
          <div>{currentForm}</div>
          {/* Submit disabled if no opcode selected */}
          <Button
            style={{ position: "absolute", left: "30px", bottom: "30px" }}
            variant="primary"
            // call onSubmit of currently selected form
            onClick={handleSubmit}
            disabled={selectedOpCode === "None"}
            className="mt-2"
          >
            + Command
          </Button>
        </Col>
      </Row>
    </Container>
  );
}
