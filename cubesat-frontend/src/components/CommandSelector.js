import { useRef, useState } from "react";
import Dropdown from "react-bootstrap/Dropdown";
import { Container, Row, Col, Button, Form } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import namespaces, { Types } from "./SFR_Overrides";
import InputField from "./InputField";

export const OpCodes = Object.freeze({
  SFR_Override: "SFR_Override",
  Deploy: "Deploy",
  Arm: "Arm",
  Fire: "Fire",
});

export default function CommandSelector() {
  const { commandStack, setCommandStack, count, setCount } = useDashboard();

  //Selected argument values
  const [selectedOpCode, setOpCode] = useState("None");
  const [selectedNamespace, setNamespace] = useState("None");
  const [selectedField, setField] = useState("None");

  //Handles conditional rendering
  const [namespaceList, setNamespaceList] = useState([]);
  const [fieldList, setFieldList] = useState([]);
  const [fieldInput, setFieldInput] = useState();
  const [inputError, setInputError] = useState();
  const fieldInputRef = useRef();

  //for command title and command description
  const [title, setTitle] = useState("No command selected");
  const [desc, setDesc] = useState("Select a command");

  //Resets command arguments and selects OpCode
  const handleOpCodeSelect = (opcode) => () => {
    setOpCode(opcode);

    setNamespaceList(
      opcode === OpCodes.SFR_Override ? Object.keys(namespaces) : []
    );
    setFieldList([]);
    setNamespace("None");
    setField("None");

    setTitle(opcode !== OpCodes.SFR_Override ? opcode : "No command selected");
    setDesc("Select a command");
  };

  /* Handles the dropdown for the first argument by setting the selected argument
   * equal to firstArg, and checking whether an input field is required.
   */
  const handleNamespaceSelect = (namespace) => () => {
    setNamespace(namespace);
    setFieldList(Object.keys(namespaces[namespace]));
    setField("None");
    setTitle("No command selected");
    setDesc("Select a command");
  };

  const handleFieldSelect = (field) => () => {
    setField(field);
    setTitle("sfr::" + selectedNamespace + "::" + field);
    // setDesc();

    let fieldType = namespaces[selectedNamespace][field].type;
    console.log(fieldType);

    if (fieldType === Types.Int) {
      setFieldInput(
        <InputField
          name="New Value"
          label={field.title}
          type="number"
          error={inputError}
          fieldRef={fieldInputRef}
        />
      );
    }
  };

  //Handles submit button press.
  function handleSubmit(event) {
    event.preventDefault();
    let new_command = {
      id: count,
      opcode: selectedOpCode,
      ...(selectedOpCode === OpCodes.SFR_Override && {
        namespace: selectedNamespace,
        field: selectedField,
        value: fieldInputRef.current.value,
      }),
    };
    setCommandStack([...commandStack, new_command]);
    setCount(count + 1);

    // reset dropdowns
  }

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

      {/* Opcode dropdown selection*/}
      <Row>
        <Col>
          <span style={{ fontWeight: "bold" }}>Opcode</span>
          <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
              {selectedOpCode}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {Object.keys(OpCodes).map((option, index) => (
                <Dropdown.Item key={index} onClick={handleOpCodeSelect(option)}>
                  {option}
                </Dropdown.Item>
              ))}
            </Dropdown.Menu>
          </Dropdown>
        </Col>

        {/* Namespace dropdown selection*/}
        <Col>
          <span style={{ fontWeight: "bold" }}>Namespace</span>
          <Dropdown disabled>
            <Dropdown.Toggle
              variant="success"
              id="dropdown-basic"
              disabled={namespaceList.length === 0}
            >
              {selectedNamespace}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {namespaceList.map((option, index) => (
                <Dropdown.Item
                  key={index}
                  onClick={handleNamespaceSelect(option)}
                >
                  {option}
                </Dropdown.Item>
              ))}
            </Dropdown.Menu>
          </Dropdown>
        </Col>

        {/* SFR field dropdown selection*/}
        <Col>
          <span style={{ fontWeight: "bold" }}>Field</span>
          <Dropdown>
            <Dropdown.Toggle
              variant="success"
              id="dropdown-basic"
              disabled={fieldList.length === 0}
            >
              {selectedField}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {fieldList.map((option, index) => (
                <Dropdown.Item key={index} onClick={handleFieldSelect(option)}>
                  {option}
                </Dropdown.Item>
              ))}
            </Dropdown.Menu>
          </Dropdown>
        </Col>
      </Row>

      {/* Renders input field --
        renders submit button if first arg and opcode have been selected*/}
      <Row className="mt-3">
        <Col className="col-sm-8">
          <Form onSubmit={handleSubmit}>
            {fieldInput !== undefined
              ? fieldInput
              : // listInput.map((option, index) => (
                //   <Form.Group controlId={index}>
                //     <span style={{ fontWeight: "bold" }}>{option}</span>
                //     <Form.Control
                //       style={{ fontSize: "20px", height: "50px" }}
                //       type="text"
                //       placeholder="Enter argument"
                //       value={fieldArg[index]}
                //       onChange={(e) => handleInputChange(e, index)}
                //     />
                //   </Form.Group>
                // ))
                null}

            <Button
              variant="primary"
              type="submit"
              disabled={selectedOpCode === "None"}
            >
              + Command
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}
