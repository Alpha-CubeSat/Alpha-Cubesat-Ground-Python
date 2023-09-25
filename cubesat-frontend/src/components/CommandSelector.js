import { useEffect, useRef, useState } from "react";
import Dropdown from "react-bootstrap/Dropdown";
import { Button, Col, Container, Form, Row } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import InputField from "./InputField";
import { Typeahead } from "react-bootstrap-typeahead";
import { useApi } from "../contexts/ApiProvider";

// SFR field types
// defaults to Int unless type attribute is set
const SFR_Type = Object.freeze({
  Second: "SECOND",
  Minute: "MINUTE",
  Hour: "HOUR",
  Multi: "MULTI",
  Float: "FLOAT",
  Bool: "BOOL",
  Int: "INT",
});

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
  const {
    commandStack,
    setCommandStack,
    count,
    setCount,
    disabledOpcodes,
    setDisabledOpcodes,
  } = useDashboard();

  const api = useApi();

  // SFR namspaces
  const [namespaces, setNamespaces] = useState({});

  // fetch metadata for all SFR override opcodes
  useEffect(() => {
    api
      .get("/cubesat/sfr_opcodes")
      .then((response) =>
        setNamespaces(response.status === 200 ? response.data : {})
      );
  }, [api]);
  // console.log(namespaces);

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
  const [eepromFields, setEepromFields] = useState({
    bootCount: "",
    sfrAddress: "",
    dataAddress: "",
    sfrWriteAge: "",
    dataWriteAge: "",
    lightSwitch: false,
  });

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

  const handleEepromChange = (event) => {
    const { name, value } = event.target;
    setEepromFields((prevFields) => ({
      ...prevFields,
      [name]: value,
    }));
  };

  // Validates input field before adding command to the command builder
  function handleSubmit(event) {
    event.preventDefault();

    let input_value = "";
    if (selectedOpCode === OpCodes.SFR_Override) {
      if (fieldData.type === SFR_Type.Multi) {
        input_value =
          String(eepromFields["bootCount"]) +
          String(eepromFields["lightSwitch"]) +
          String(eepromFields["sfrAddress"]) +
          String(eepromFields["dataAddress"]) +
          String(eepromFields["sfrWriteAge"]) +
          String(eepromFields["dataWriteAge"]);
      } else {
        input_value =
          fieldData.type !== SFR_Type.Bool
            ? fieldInputRef.current.value
            : fieldInputRef.current.checked.toString();
      }
      // validate input: make sure field is not empty, ints and floats are valid, input within min and max values
      let error = "";
      let int_check = new RegExp("^-?\\d+$");
      let float_check = new RegExp("^-?\\d+(\\.\\d+)?$");
      if (!input_value) {
        error = "Field cannot be empty.";
      } else if (
        (fieldData.type === undefined ||
          fieldData.type === SFR_Type.Second ||
          fieldData.type === SFR_Type.Minute ||
          fieldData.type === SFR_Type.Hour) &&
        !int_check.test(input_value)
      ) {
        error = "Not a valid integer.";
      } else if (
        fieldData.type === SFR_Type.Float &&
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

    // convert minutes and hours to seconds
    if (fieldData.type === SFR_Type.Second) {
      input_value *= 1000;
    } else if (fieldData.type === SFR_Type.Minute) {
      input_value *= 60 * 1000;
    } else if (fieldData.type === SFR_Type.Hour) {
      input_value *= 3600 * 1000;
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
    if (
      new_command["opcode"] === "Deploy" ||
      new_command["opcode"] === "Arm" ||
      new_command["opcode"] === "Fire"
    ) {
      setDisabledOpcodes(["Deploy", "Arm", "Fire"]);
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

      {/* Opcode dropdown selection */}
      <Row className="d-flex flex-wrap">
        <Col className="col-md-4">
          <span style={{ fontWeight: "bold" }}>Opcode</span>
          <Dropdown>
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
          <Row>
            {/* Namespace dropdown selection */}
            <Col>
              <span style={{ fontWeight: "bold" }}>Namespace</span>
              <Form>
                <Typeahead
                  id="namespace-dropdown"
                  labelKey="namespace"
                  options={namespaceList}
                  disabled={selectedOpCode !== OpCodes.SFR_Override}
                  placeholder="Select"
                  ref={namespaceRef}
                  onChange={(selected) => handleNamespaceSelect(selected)}
                  onInputChange={(selected) => handleNamespaceSelect(selected)}
                  renderMenuItemChildren={(option, { text }) => <>{option}</>}
                />
              </Form>
            </Col>

            {/* SFR field dropdown selection */}
            <Col>
              <span style={{ fontWeight: "bold" }}>Field</span>
              <Typeahead
                id="field-dropdown"
                labelKey="field"
                options={fieldList}
                ref={fieldRef}
                disabled={
                  selectedOpCode !== OpCodes.SFR_Override ||
                  !(selectedNamespace in namespaces)
                }
                placeholder="Select"
                onChange={(select) => handleFieldSelect(select)}
                onInputChange={(select) => handleFieldSelect(select)}
                renderMenuItemChildren={(option, { text }) => <>{option}</>}
              />
            </Col>
          </Row>
          <Row>
            <Col>
              {/* SFR field input */}
              <Form
                onSubmit={handleSubmit}
                noValidate
                className="col-lg-12 mt-2"
              >
                {fieldData.type && (
                  <span style={{ fontWeight: "bold" }}>Argument</span>
                )}
                {console.log(fieldData.type)}
                {(fieldData.type === SFR_Type.Minute ||
                  fieldData.type === SFR_Type.Hour ||
                  fieldData.type === SFR_Type.Float ||
                  fieldData.type === SFR_Type.Int ||
                  fieldData.type === SFR_Type.Second) && (
                  <InputField
                    name="sfr_override"
                    type="number"
                    className="mt-1"
                    placeholder={
                      fieldData.type === SFR_Type.Minute
                        ? "Minutes"
                        : fieldData.type === SFR_Type.Hour
                        ? "Hours"
                        : "Value"
                    }
                    error={inputError}
                    fieldRef={fieldInputRef}
                  />
                )}
                {fieldData.type === SFR_Type.Bool && (
                  <div className="mt-2">
                    <Form.Check
                      name="sfr_override"
                      label="true"
                      type="radio"
                      inline
                      defaultChecked
                      ref={fieldInputRef}
                    />
                    <Form.Check
                      name="sfr_override"
                      label="false"
                      type="radio"
                      inline
                    />
                  </div>
                )}

                {fieldData.type === SFR_Type.Multi && (
                  <>
                    <Row className="mb-2">
                      {" "}
                      {/* 1st Row */}
                      <Col>
                        <InputField
                          name="bootCount"
                          type="number"
                          className="mt-1"
                          placeholder={"Boot count"}
                          error={inputError}
                          onChange={handleEepromChange}
                        />
                      </Col>
                      <Col className="d-flex flex-column justify-content-center align-items-center">
                        <div>
                          <Form.Check
                            name="lightSwitch"
                            label="Light 1"
                            type="radio"
                            inline
                            defaultChecked
                            onChange={handleEepromChange}
                          />
                          <Form.Check
                            name="lightSwitch"
                            label="Light 0"
                            type="radio"
                            inline
                            onChange={handleEepromChange}
                          />
                        </div>
                      </Col>
                    </Row>
                    <Row className="mb-2">
                      {" "}
                      {/* 2nd Row */}
                      <Col>
                        <InputField
                          name="sfrAddress"
                          type="number"
                          className="mt-1"
                          placeholder={"SFR address"}
                          error={inputError}
                          onChange={handleEepromChange}
                        />
                      </Col>
                      <Col>
                        <InputField
                          name="dataAddress"
                          type="number"
                          className="mt-1"
                          placeholder={"Data address"}
                          error={inputError}
                          onChange={handleEepromChange}
                        />
                      </Col>
                    </Row>
                    <Row className="mb-2">
                      {" "}
                      {/* 3rd Row */}
                      <Col>
                        <InputField
                          name="sfrWriteAge"
                          type="number"
                          className="mt-1"
                          placeholder={"SFR write age"}
                          error={inputError}
                          onChange={handleEepromChange}
                        />
                      </Col>
                      <Col>
                        <InputField
                          name="dataWriteAge"
                          type="number"
                          className="mt-1"
                          placeholder={"Data write age"}
                          error={inputError}
                          onChange={handleEepromChange}
                        />
                      </Col>
                    </Row>
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
