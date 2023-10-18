import { forwardRef, useImperativeHandle, useRef, useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import { Typeahead } from "react-bootstrap-typeahead";
import InputField from "./InputField";

// SFR field types
const SFR_Type = Object.freeze({
  Int: "INT",
  Float: "FLOAT",
  Time: "TIME",
  Bool: "BOOL",
});
export const SFR_Override = forwardRef(({ sfr_data, setTitle }, ref) => {
  // Selected dropdown values
  const [selectedNamespace, setNamespace] = useState("None");
  const [selectedField, setField] = useState("None");

  // Dropdown item lists for namespaces and fields
  const [fieldList, setFieldList] = useState([]);
  const namespaceRef = useRef();
  const fieldRef = useRef();

  // Input field data and form error
  const [fieldData, setFieldData] = useState({});
  const [inputError, setInputError] = useState();
  const fieldInputRef = useRef();
  const [timeUnit, setTimeUnit] = useState("SEC");

  useImperativeHandle(ref, () => ({
    // Validates input field before adding command to the command builder
    handleSubmit() {
      console.log("hi");

      if (selectedNamespace === "None" || selectedField === "None") return;

      let input_value = "";
      // extract value from text field or boolean value from radios
      input_value =
        fieldData.type !== SFR_Type.Bool
          ? fieldInputRef.current.value
          : fieldInputRef.current.checked.toString();

      // validate input: make sure field is not empty, ints and floats are valid, input within min and max values
      let error = "";
      let int_check = new RegExp("^-?\\d+$");
      let float_check = new RegExp("^-?\\d+(\\.\\d+)?$");
      if (!input_value) {
        error = "Field cannot be empty.";
      } else if (
        (fieldData.type === SFR_Type.Int || fieldData.type === SFR_Type.Time) &&
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

      // convert minutes and hours to seconds
      if (fieldData.type === SFR_Type.Time) {
        if (timeUnit === "SEC") {
          input_value *= 1000;
        } else if (timeUnit === "MIN") {
          input_value *= 60 * 1000;
        } else if (timeUnit === "HOUR") {
          input_value *= 3600 * 1000;
        }
      }

      // reset dropdowns
      setFieldList([]);
      setNamespace("None");
      setField("None");
      setFieldData({});
      setInputError();

      fieldRef.current.clear();
      namespaceRef.current.clear();

      // add to command builder
      return {
        namespace: selectedNamespace + "",
        field: selectedField + "",
        value: input_value,
      };
    },
  }));

  // Updates dropdown menus based on selected SFR namespace
  const handleNamespaceSelect = (namespace) => {
    setNamespace(namespace);
    if (namespace in sfr_data) {
      setFieldList(Object.keys(sfr_data[namespace]));
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
    if (field in sfr_data[selectedNamespace]) {
      setField(field);
      setFieldData(sfr_data[selectedNamespace][field]);
      setInputError();
      setTitle("sfr::" + selectedNamespace + "::" + field);
    }
  };

  return (
    <div>
      <Row>
        {/* Namespace dropdown selection */}
        <Col>
          <span style={{ fontWeight: "bold" }}>Namespace</span>
          <Typeahead
            id="namespace-dropdown"
            labelKey="namespace"
            options={Object.keys(sfr_data)}
            placeholder="Select"
            ref={namespaceRef}
            onChange={(selected) => handleNamespaceSelect(selected)}
            onInputChange={(selected) => handleNamespaceSelect(selected)}
            renderMenuItemChildren={(option) => <>{option}</>}
          />
        </Col>

        {/* SFR field dropdown selection */}
        <Col>
          <span style={{ fontWeight: "bold" }}>Field</span>
          <Typeahead
            id="field-dropdown"
            labelKey="field"
            options={fieldList}
            ref={fieldRef}
            disabled={!(selectedNamespace in sfr_data)}
            placeholder="Select"
            onChange={(select) => handleFieldSelect(select)}
            onInputChange={(select) => handleFieldSelect(select)}
            renderMenuItemChildren={(option) => <>{option}</>}
          />
        </Col>
      </Row>
      {fieldData.type && (
        <Row>
          <Col>
            {/* SFR field input */}
            <div className="col-lg-12 mt-2">
              <span style={{ fontWeight: "bold" }}>Argument</span>

              {(fieldData.type === SFR_Type.Time ||
                fieldData.type === SFR_Type.Float ||
                fieldData.type === SFR_Type.Int) && (
                <>
                  <InputField
                    name="sfr_override"
                    type="number"
                    className="mt-1"
                    placeholder="Value"
                    error={inputError}
                    fieldRef={fieldInputRef}
                  />
                  {/* Time unit selector */}
                  {fieldData.type === SFR_Type.Time && (
                    <div className="mt-2">
                      <Form.Check
                        name="time_unit"
                        label="seconds"
                        type="radio"
                        inline
                        defaultChecked
                        onChange={() => setTimeUnit("SEC")}
                      />
                      <Form.Check
                        name="time_unit"
                        label="minutes"
                        id="unit_minutes"
                        type="radio"
                        onChange={() => setTimeUnit("MIN")}
                        inline
                      />
                      <Form.Check
                        name="time_unit"
                        label="hours"
                        id="unit_hours"
                        type="radio"
                        onChange={() => setTimeUnit("HOUR")}
                        inline
                      />
                    </div>
                  )}
                </>
              )}
              {fieldData.type === SFR_Type.Bool && (
                <div className="mt-2">
                  <Form.Check
                    name="sfr_override"
                    label="true"
                    type="radio"
                    ref={fieldInputRef}
                    inline
                    defaultChecked
                  />
                  <Form.Check
                    name="sfr_override"
                    label="false"
                    type="radio"
                    inline
                  />
                </div>
              )}
            </div>
          </Col>
          <Col className="mt-2">
            <div>
              <div className="mb-2">
                <span style={{ fontWeight: "bold" }}>Set Restore</span>
                <Form.Check className="ms-2" inline />
              </div>
              <Form.Check
                name="restore"
                label="true"
                type="radio"
                inline
                defaultChecked
              />
              <Form.Check name="restore" label="false" type="radio" inline />
            </div>
          </Col>
        </Row>
      )}
    </div>
  );
});

export const EEPROM_Reset = forwardRef(({}, ref) => {
  const [inputError, setInputError] = useState();
  const [eepromFields, setEepromFields] = useState({
    byteCount: "112211",
    bootCount: "",
    sfrAddress: "",
    dataAddress: "",
    sfrWriteAge: "",
    dataWriteAge: "",
    lightSwitch: false,
  });

  useImperativeHandle(ref, () => ({
    handleSubmit() {
      return {
        byteCount: eepromFields["byteCount"],
        bootCount: eepromFields["bootCount"],
        lightSwitch: eepromFields["lightSwitch"],
        sfrAddress: eepromFields["sfrAddress"],
        dataAddress: eepromFields["dataAddress"],
        sfrWriteAge: Math.floor(parseInt(eepromFields["sfrWriteAge"]) / 373),
        dataWriteAge: Math.floor(parseInt(eepromFields["dataWriteAge"]) / 373),
      };
    },
  }));

  const handleEepromChange = (event) => {
    const { name, value } = event.target;
    setEepromFields((prevFields) => ({
      ...prevFields,
      [name]: value,
    }));
  };

  return (
    <div>
      <Row className="mb-2">
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
              value="true"
              inline
              defaultChecked
              onChange={handleEepromChange}
            />
            <Form.Check
              name="lightSwitch"
              label="Light 0"
              type="radio"
              value="false"
              inline
              onChange={handleEepromChange}
            />
          </div>
        </Col>
      </Row>
      <Row className="mb-2">
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
    </div>
  );
});
