import { forwardRef, useImperativeHandle, useRef, useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import { Typeahead } from "react-bootstrap-typeahead";
import InputField from "./InputField";
import { SFR_Type } from "../constants";

// forwardRef allows access to the ref prop passed in by the CommandSelector component
export const SfrOverride = forwardRef(({ SFR_Data, setTitle }, ref) => {
  // Selected dropdown values
  const [selectedNamespace, setNamespace] = useState("None");
  const [selectedField, setField] = useState("None");

  // Dropdown item lists for namespaces and fields
  const [fieldList, setFieldList] = useState([]);
  const namespaceDropRef = useRef();
  const fieldDropRef = useRef();

  // Input field data and form error
  const initialFieldData = {
    value: "",
    setValue: true,
    setRestore: false,
    restoreValue: false,
  };
  const [commandFields, setCommandFields] = useState(initialFieldData);
  const [fieldData, setFieldData] = useState({});
  const [inputError, setInputError] = useState();
  const [timeUnit, setTimeUnit] = useState("SEC");

  // useImperativeHandle allows the CommandSelector component to call the handleSubmit() function,
  // which checks if the command fields are valid and returns the command if so
  useImperativeHandle(ref, () => ({
    // Validates input field before adding command to the command builder
    handleSubmit() {
      if (selectedNamespace === "None" || selectedField === "None") return;

      // validate input: make sure field is not empty, ints and floats are valid, input within min and max values
      let error = "";
      let int_check = new RegExp("^-?\\d+$");
      let float_check = new RegExp("^-?\\d+(\\.\\d+)?$");
      if (commandFields.setValue) {
        if (!commandFields.value) {
          error = "Field cannot be empty.";
        } else if (
          (fieldData.type === SFR_Type.Int ||
            fieldData.type === SFR_Type.Time) &&
          !int_check.test(commandFields.value)
        ) {
          error = "Not a valid integer.";
        } else if (
          fieldData.type === SFR_Type.Float &&
          !float_check.test(commandFields.value)
        ) {
          error = "Not a valid float.";
        } else if (
          fieldData.min !== undefined &&
          commandFields.value < fieldData.min
        ) {
          error = "Minimum value is " + fieldData.min;
        } else if (
          fieldData.max !== undefined &&
          commandFields.value > fieldData.max
        ) {
          error = "Maximum value is " + fieldData.max;
        }
      }
      setInputError(error);
      if (error.length > 0) return;

      // convert seconds, minutes, and hours to milliseconds
      if (fieldData.type === SFR_Type.Time) {
        if (timeUnit === "SEC") {
          commandFields.value *= 1000;
        } else if (timeUnit === "MIN") {
          commandFields.value *= 60 * 1000;
        } else if (timeUnit === "HOUR") {
          commandFields.value *= 3600 * 1000;
        }
      }

      // send to CommandSelector component
      return {
        namespace: selectedNamespace[0],
        field: selectedField[0],
        value: commandFields,
      };
    },
  }));

  // Updates dropdown menus based on selected SFR namespace
  const handleNamespaceSelect = (namespace) => {
    setNamespace(namespace);
    setFieldList(namespace in SFR_Data ? Object.keys(SFR_Data[namespace]) : []);

    resetFieldState();
    setTitle("No command selected");
  };

  // Updates input field based on selected SFR field
  const handleFieldSelect = (field) => {
    if (field in SFR_Data[selectedNamespace]) {
      setField(field);
      setFieldData(SFR_Data[selectedNamespace][field]);
      setInputError();
      setTitle("sfr::" + selectedNamespace + "::" + field);

      // by default boolean radio is set to true for boolean type SFR fields
      if (SFR_Data[selectedNamespace][field].type === SFR_Type.Bool) {
        setCommandFields((prevFields) => ({
          ...prevFields,
          value: true,
        }));
      }
    }
  };

  // Update the command argument dictionary when a form element is changed
  const handleFieldChange = (event) => {
    let { name, value } = event.target;
    if (name === "setValue") value = !commandFields.setValue;
    else if (name === "setRestore") value = !commandFields.setRestore;

    setCommandFields((prevFields) => ({
      ...prevFields,
      [name]: value,
    }));
  };

  // reset states relating to the currently selected SFR field only
  const resetFieldState = () => {
    setField("None");
    setFieldData({});
    setInputError();
    setCommandFields(initialFieldData);
    setTimeUnit("SEC");
    fieldDropRef.current.clear();
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
            options={Object.keys(SFR_Data)}
            placeholder="Select"
            ref={namespaceDropRef}
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
            ref={fieldDropRef}
            disabled={!(selectedNamespace in SFR_Data)}
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
            <div className="mt-2">
              <div className="mb-2">
                <span style={{ fontWeight: "bold" }}>Set Value</span>
                <Form.Check
                  name="setValue"
                  className="ms-2"
                  onChange={handleFieldChange}
                  defaultChecked
                  inline
                />
              </div>

              {(fieldData.type === SFR_Type.Time ||
                fieldData.type === SFR_Type.Float ||
                fieldData.type === SFR_Type.Int) && (
                <>
                  {/* Numerical SFR field input */}
                  <InputField
                    name="value"
                    type="number"
                    className="mt-1"
                    placeholder="Value"
                    error={inputError}
                    onChange={handleFieldChange}
                    disabled={!commandFields.setValue}
                  />
                  {/* Time unit selector */}
                  {fieldData.type === SFR_Type.Time && (
                    <div className="mt-2">
                      <Form.Check
                        name="time_unit"
                        label="sec"
                        type="radio"
                        disabled={!commandFields.setValue}
                        onChange={() => setTimeUnit("SEC")}
                        inline
                        defaultChecked
                        className="me-2"
                      />
                      <Form.Check
                        name="time_unit"
                        label="min"
                        id="unit_minutes"
                        type="radio"
                        disabled={!commandFields.setValue}
                        onChange={() => setTimeUnit("MIN")}
                        inline
                        className="me-2"
                      />
                      <Form.Check
                        name="time_unit"
                        label="hr"
                        id="unit_hours"
                        type="radio"
                        disabled={!commandFields.setValue}
                        onChange={() => setTimeUnit("HOUR")}
                        inline
                        className="me-2"
                      />
                    </div>
                  )}
                </>
              )}
              {fieldData.type === SFR_Type.Bool && (
                <div className="mt-2">
                  {/* Boolean SFR field input */}
                  <Form.Check
                    name="value"
                    type="radio"
                    label="true"
                    value="true"
                    disabled={!commandFields.setValue}
                    onChange={handleFieldChange}
                    inline
                    defaultChecked
                  />
                  <Form.Check
                    name="value"
                    type="radio"
                    label="false"
                    value="false"
                    disabled={!commandFields.setValue}
                    onChange={handleFieldChange}
                    inline
                  />
                </div>
              )}
            </div>
          </Col>
          <Col className="mt-2">
            {/* SFR Restore options */}
            <div>
              <div className="mb-2">
                <span style={{ fontWeight: "bold" }}>Set Restore</span>
                <Form.Check
                  name="setRestore"
                  className="ms-2"
                  onChange={handleFieldChange}
                  inline
                />
              </div>
              <Form.Check
                name="restoreValue"
                type="radio"
                label="true"
                value="true"
                disabled={!commandFields.setRestore}
                onChange={handleFieldChange}
                inline
              />
              <Form.Check
                name="restoreValue"
                type="radio"
                label="false"
                value="false"
                disabled={!commandFields.setRestore}
                onChange={handleFieldChange}
                inline
                defaultChecked
              />
            </div>
          </Col>
        </Row>
      )}
    </div>
  );
});

export const Fault = forwardRef(({ Fault_Data, setTitle }, ref) => {
  // Selected dropdown values
  const [selectedNamespace, setNamespace] = useState("None");
  const [selectedFault, setFault] = useState("None");
  const [activeCheckbox, setActiveCheckbox] = useState("Force");

  const namespaceDropRef = useRef();
  const fieldDropRef = useRef();

  // Fault list
  const [faultList, setFaultList] = useState([]);

  // Updates dropdown menus based on selected Fault namespace
  const handleNamespaceSelect = (namespace) => {
    setNamespace(namespace);
    setFaultList(
      namespace in Fault_Data ? Object.keys(Fault_Data[namespace]) : []
    );
    setTitle("No command selected");
    setFault("None");
    fieldDropRef.current.clear();
  };

  // Updates input field based on selected SFR field
  const handleFieldSelect = (field) => {
    if (field in Fault_Data[selectedNamespace]) {
      setFault(field);
      setTitle("fault_groups::" + selectedNamespace + "::" + field);
    }
  };

  // useImperativeHandle allows the CommandSelector component to call the handleSubmit() function,
  // which checks if the command fields are valid and returns the command if so
  useImperativeHandle(ref, () => ({
    handleSubmit() {
      if (selectedNamespace === "None" || selectedFault === "None") return;
      // send to CommandSelector component
      return {
        namespace: selectedNamespace[0],
        field: selectedFault[0],
        value: activeCheckbox,
      };
    },
  }));

  return (
    <div>
      <Row>
        {/* Namespace dropdown selection */}
        <Col>
          <span style={{ fontWeight: "bold" }}>Namespace</span>
          <Typeahead
            id="namespace-dropdown"
            labelKey="namespace"
            options={Object.keys(Fault_Data)}
            placeholder="Select"
            ref={namespaceDropRef}
            onChange={(selected) => handleNamespaceSelect(selected)}
            onInputChange={(selected) => handleNamespaceSelect(selected)}
            renderMenuItemChildren={(option) => <>{option}</>}
          />
        </Col>
        {/* Fault field dropdown selection */}
        <Col>
          <span style={{ fontWeight: "bold" }}>Fault</span>
          <Typeahead
            id="field-dropdown"
            labelKey="field"
            options={faultList}
            ref={fieldDropRef}
            disabled={!(selectedNamespace in Fault_Data)}
            placeholder="Select"
            onChange={(select) => handleFieldSelect(select)}
            onInputChange={(select) => handleFieldSelect(select)}
            renderMenuItemChildren={(option) => <>{option}</>}
          />
        </Col>
      </Row>
      {selectedFault !== "None" && (
        <div className="mt-3">
          {/* Checkbox for Force */}
          <Form.Check
            name="Force"
            type="radio"
            label="Force"
            onChange={() => setActiveCheckbox("Force")}
            checked={activeCheckbox === "Force"}
            className="mb-3"
          />
          {/* Checkbox for setSuppress */}
          <Form.Check
            name="Suppress"
            type="radio"
            label="Suppress"
            onChange={() => setActiveCheckbox("Suppress")}
            checked={activeCheckbox === "Suppress"}
            className="mb-3"
          />
          {/* Checkbox for Restore */}
          <Form.Check
            name="Restore"
            type="radio"
            label="Restore"
            onChange={() => setActiveCheckbox("Restore")}
            checked={activeCheckbox === "Restore"}
            className="mb-3"
          />
        </div>
      )}
    </div>
  );
});

export const FragmentRequest = forwardRef(({}, ref) => {
  // Selected values
  const [fragmentType, setFragmentType] = useState("Image");
  const [serialNum, setSerialNum] = useState("");
  const [fragmentNum, setFragmentNum] = useState("");
  const [inputError, setInputError] = useState();

  // useImperativeHandle allows the CommandSelector component to call the handleSubmit() function,
  // which checks if the command fields are valid and returns the command if so
  useImperativeHandle(ref, () => ({
    handleSubmit() {
      if (fragmentNum === "" || (fragmentType === "Image" && serialNum === ""))
        return;

      return {
        value: {
          type: fragmentType,
          fragmentNum: fragmentNum,
          ...(fragmentType === "Image" && { serialNum: serialNum }),
        },
      };
    },
  }));

  const handleFieldChange = (event) => {
    let { name, value } = event.target;
    if (name === "serialNum") setSerialNum(value);
    else if (name === "fragmentNum") setFragmentNum(value);
  };

  return (
    <div>
      <Row>
        <Col>
          <span style={{ fontWeight: "bold" }}>Type</span>
          <Form.Check
            name="fragType"
            type="radio"
            label="Image"
            onChange={() => setFragmentType("Image")}
            defaultChecked
          />
          <Form.Check
            name="fragType"
            type="radio"
            label="IMU"
            onChange={() => setFragmentType("IMU")}
          />
        </Col>
        {fragmentType === "Image" && (
          <Col>
            <span style={{ fontWeight: "bold" }}>Serial #</span>
            <InputField
              name="serialNum"
              type="number"
              className="mt-1"
              placeholder="Value"
              // error={inputError}
              onChange={handleFieldChange}
            />
          </Col>
        )}
        <Col>
          <span style={{ fontWeight: "bold" }}>Fragment #</span>
          <InputField
            name="fragmentNum"
            type="number"
            className="mt-1"
            placeholder="Value"
            // error={inputError}
            onChange={handleFieldChange}
          />
        </Col>
      </Row>
    </div>
  );
});

export const EepromReset = forwardRef(({}, ref) => {
  const [inputError, setInputError] = useState();
  const [eepromFields, setEepromFields] = useState({
    bootCount: "",
    sfrAddress: "",
    dataAddress: "",
    sfrWriteAge: "",
    dataWriteAge: "",
    lightSwitch: false,
  });

  useImperativeHandle(ref, () => ({
    handleSubmit() {
      if (
        eepromFields.bootCount === "" ||
        eepromFields.sfrAddress === "" ||
        eepromFields.dataAddress === "" ||
        eepromFields.sfrWriteAge === "" ||
        eepromFields.dataWriteAge === ""
      )
        return;

      return {
        value: eepromFields,
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
              label="Light True"
              type="radio"
              value="true"
              inline
              onChange={handleEepromChange}
            />
            <Form.Check
              name="lightSwitch"
              label="Light False"
              type="radio"
              value="false"
              inline
              defaultChecked
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
