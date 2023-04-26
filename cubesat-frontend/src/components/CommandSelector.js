import { useRef, useState } from "react";
import Dropdown from "react-bootstrap/Dropdown";
import { Container, Row, Col, Button, Form } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import namespaces, { Types } from "./SFR_Overrides";
import InputField from "./InputField";
import { Typeahead } from "react-bootstrap-typeahead";

// Allowed opcodes
export const OpCodes = Object.freeze({
  SFR_Override: "SFR_Override",
  Deploy: "Deploy",
  Arm: "Arm",
  Fire: "Fire",
});

export const opcodeDesc = {
  SFR_Override: "Override the selected SFR field with the provided value.",
  Deploy: "Move the CubeSat into the Deployment phase.",
  Arm: "Move the CubeSat into the Armed phase.",
  Fire: "Move the CubeSat into the In Sun phase.",
};

// Command Selector
// Has dropdown menus for user to build a command to be sent to the CubeSat
// Dropdowns for SFR namespace and field are searchable to improve usability
// Supports multiple types command arguments (ints, floats, booleans, time) and min/max checking
// Shows the title and description for a selected command
export default function CommandSelector() {
  const { commandStack, setCommandStack, count, setCount, disabledOpcodes, setDisabledOpcodes } = useDashboard();

  // Selected dropdown values
  const [selectedOpCode, setOpCode] = useState("None");
  const [selectedNamespace, setNamespace] = useState("None");
  const [selectedField, setField] = useState("None");

  // Dropdown item lists for namespaces and fields
  const [namespaceList, setNamespaceList] = useState([]);
  const [fieldList, setFieldList] = useState([]);
  const namespaceRef = useRef();
  const fieldRef = useRef();

  // Input field data and form error
  const [fieldData, setFieldData] = useState({});
  const [inputError, setInputError] = useState();
  const fieldInputRef = useRef();

  // Command title and description
  const [title, setTitle] = useState("No command selected");
  const [desc, setDesc] = useState("Select a command");

  // Updates dropdown menus based on selected opcode
  const handleOpCodeSelect = (opcode) => () => {
    setOpCode(opcode);

    setNamespaceList(
      opcode === OpCodes.SFR_Override ? Object.keys(namespaces) : []
    );
    setFieldList([]);
    setNamespace("None");
    setField("None");
    setFieldData({});
    setInputError();
    setTitle(opcode !== OpCodes.SFR_Override ? opcode : "No command selected");
    setDesc(opcodeDesc[opcode]);
    namespaceRef.current.clear();
    fieldRef.current.clear();
  };

  // Updates dropdown menus based on selected SFR namespace
  const handleNamespaceSelect = (namespace) => {
    setNamespace(namespace);
    if (namespace in namespaces) {
      setFieldList(Object.keys(namespaces[namespace]));
    } else {
      setFieldList([]);
    }
    setField("None");
    setFieldData({});
    setInputError();
    setTitle("No command selected");
    fieldRef.current.clear();
  };

  // Updates input field based on selected SFR field
  const handleFieldSelect = (field) => {
    if (field in namespaces[selectedNamespace]) {
      setField(field);
      setFieldData(namespaces[selectedNamespace][field]);
      setInputError();

      setTitle("sfr::" + selectedNamespace + "::" + field);
      // setDesc();
    }
  };

  // Validates input field before adding command to the command builder
  function handleSubmit(event) {
    event.preventDefault();

    let input_value = "";
    if (selectedOpCode === OpCodes.SFR_Override) {
      input_value =
        fieldData.type !== Types.Bool
          ? fieldInputRef.current.value
          : fieldInputRef.current.checked.toString();

      // validate input: make sure field is not empty, ints and floats are valid, input within min and max values
      let error = "";
      let int_check = new RegExp("^-?\\d+$");
      let float_check = new RegExp("^-?\\d+(\\.\\d+)?$");
      if (!input_value) {
        error = "Field cannot be empty.";
      } else if (
        (fieldData.type === Types.Int ||
          fieldData.type === Types.Minute ||
          fieldData.type === Types.Hour) &&
        !int_check.test(input_value)
      ) {
        error = "Not a valid integer.";
      } else if (
        fieldData.type === Types.Float &&
        !float_check.test(input_value)
      ) {
        error = "Not a valid float.";
      } else if (fieldData.min !== undefined && input_value < fieldData.min) {
        error = "Minimum value is " + fieldData.min;
      } else if (fieldData.max !== undefined && input_value > fieldData.max) {
        error = "Maximum value is " + fieldData.max;
      }
      setInputError(error);
      if (error.length > 0) return;
    }

    // add to command builder
    let new_command = {
      id: count,
      opcode: selectedOpCode,
      ...(selectedOpCode === OpCodes.SFR_Override && {
        namespace: selectedNamespace + "",
        field: selectedField + "",
        value: input_value,
      }),
    };
    setCommandStack([...commandStack, new_command]);
    setCount(count + 1);
    
    //Allows only one command--deploy, arm, or fire to be sent at a time
    if (new_command["opcode"] === "Deploy" || new_command["opcode"] === "Arm" || new_command["opcode"] === "Fire") {
      setDisabledOpcodes(["Deploy","Arm","Fire"])
    }

    

    // reset dropdowns
    setOpCode("None");
    setNamespaceList([]);
    setFieldList([]);
    setNamespace("None");
    setField("None");
    setFieldData({});
    setInputError();
    setTitle("No command selected");
    setDesc("Select a command");
    fieldRef.current.clear();
    namespaceRef.current.clear();
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
                <Dropdown.Item key={index} disabled ={disabledOpcodes.includes(option)} onClick={handleOpCodeSelect(option)}>
                  {option}
                </Dropdown.Item>
              ))}
            </Dropdown.Menu>
          </Dropdown>
        </Col>

        {/* Namespace dropdown selection*/}
        <Col className="justify-content-mid" md={4}>
          <span style={{ fontWeight: "bold" }}>Namespace</span>
          <Form>
            <Typeahead
              id="searchable-dropdown"
              labelKey="namespace"
              options={namespaceList}
              disabled={selectedOpCode !== OpCodes.SFR_Override}
              placeholder="namespace..."
              ref={namespaceRef}
              onChange={(selected) => handleNamespaceSelect(selected)}
              onInputChange={(selected) => handleNamespaceSelect(selected)}
              renderMenuItemChildren={(option, { text }) => <>{option}</>}
            />
          </Form>
        </Col>

        {/* SFR field dropdown selection*/}
        <Col>
          <span style={{ fontWeight: "bold" }}>Field</span>
          <Typeahead
            id="second-searchable-dropdown"
            labelKey="field"
            options={fieldList}
            ref={fieldRef}
            disabled={
              selectedOpCode !== OpCodes.SFR_Override ||
              !(selectedNamespace in namespaces)
            }
            placeholder="field..."
            onChange={(select) => handleFieldSelect(select)}
            onInputChange={(select) => handleFieldSelect(select)}
            renderMenuItemChildren={(option, { text }) => <>{option}</>}
          />
          {/* SFR field input */}
          <Row className="mt-3 mb-3">
            <Col className="justify-content-end" md={14}>
              <Form onSubmit={handleSubmit} noValidate>
                {fieldData.type && (
                  <span
                    className="mb-3"
                    style={{
                      position: "absolute",
                      top: "220px",
                      fontWeight: "bold",
                    }}
                  >
                    Field Argument
                  </span>
                )}

                {fieldData.type && fieldData.type !== Types.Bool && (
                  <InputField
                    name="sfr_override"
                    type="number"
                    className="mt-4"
                    placeholder={
                      fieldData.type === Types.Minute
                        ? "Minutes"
                        : fieldData.type === Types.Hour
                        ? "Hours"
                        : "Value"
                    }
                    error={inputError}
                    fieldRef={fieldInputRef}
                  />
                )}
                {fieldData.type === Types.Bool && (
                  <>
                    <Form.Check
                      className="mt-3"
                      name="sfr_override"
                      label="true"
                      type="radio"
                      inline
                      defaultChecked
                      ref={fieldInputRef}
                    />
                    <Form.Check
                      className="mt-3"
                      name="sfr_override"
                      label="false"
                      type="radio"
                      inline
                    />
                  </>
                )}
                {/* Submit disabled if no opcode selected or SFR override selected but no namespace or field selected */}
                <Button
                  style={{ position: "absolute", left: "30px", bottom: "30px" }}
                  variant="primary"
                  type="submit"
                  disabled={
                    selectedOpCode === "None" ||
                    (selectedOpCode === OpCodes.SFR_Override &&
                      (selectedNamespace === "None" ||
                        selectedField === "None"))
                  }
                  className="mt-2"
                >
                  + Command
                </Button>
              </Form>
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
}
