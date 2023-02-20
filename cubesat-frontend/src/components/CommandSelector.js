import { useState } from "react";
import Dropdown from 'react-bootstrap/Dropdown';
import { Container, Row, Col, Button, Form} from 'react-bootstrap';
import {selectArguments } from "./Commands"

export default function CommandSelector() {

/* 
* Dictionary of fields that require input fields. Value is the number of fields needed
*/
  var requiresField = {
    'Burn Time' : 1,
    'Arm Time' : 1,
    'Downlink Period' : 1,
    'Request Image Fragment' : 2
  }
  
  var opcodeList = ["Mission", "Burnwire","Rockblock", "Camera", "Temperature", "ACS", "Faults"]

  //Selected argument values
  const [selectedOpCode, setSelectedOpCode] = useState("Select Opcode")
  const [firstArg, setFirstArg] = useState("None")
  const [fieldArg, setFieldArg] = useState("")

  //Handles conditional rendering
  const [firstArgList, setFirstArgList] = useState([])
  const [isSecInput, setIsSecInput] = useState(false)      //checks if an input field is required
  const [fieldName, setFieldName] = useState("None")

  //for command title and command description
  const [title, setTitle] = useState("No command selected")
  const [desc, setDesc] = useState("Select a command")

  const handleOpCodeSelection = (opcode) => () => {

    console.log(fieldArg)
    setSelectedOpCode(opcode)
    setFirstArgList(selectArguments[opcode].arg)
    setFirstArg("None")
    setIsSecInput(false)
    setTitle("No command selected")
    setDesc("Select a command")
  }

  /* Handles the dropdown for the first argument by setting the selected argument
   * equal to firstArg, and checking whether an input field is required.
   */
  const handleFirstArgSelection = (arg1) => () => {
    setFirstArg(arg1)
    setFieldName(arg1)
    setTitle(selectedOpCode + " " + arg1)
    setDesc("Select a command")
    setDesc(selectArguments[selectedOpCode].desc[(selectArguments[selectedOpCode].arg).indexOf(arg1)])
    
    //Handles if 2nd argument is an input field
    if (arg1 in requiresField) {        
      setIsSecInput(true)
    }
    else {
      setIsSecInput(false)
    }
  }

  //Updates fieldArg to whatever is in the input field
  function handleInputChange(event) {
    setFieldArg(event.target.value);
  }

  //Handles submit button press
  function handleSubmit(event) {
    alert("Input Field: " + fieldArg + " Opcode: " + selectedOpCode + " FirstArg: " + firstArg)
    event.preventDefault();
    //Do something with firstArg, selectedOpCode, and fieldArg. Send to Command Builder and Command List?
  }
 
  return (
      <Container>
        {/* //Command Title and Description */}
        <Row>
          <h1 style={{ fontSize: '2rem' }}>{title !== "No Command Selected"? title : "No Command Selected"}</h1>
          <h2 style={{ fontSize: '1rem' }}>{desc} </h2>
          <hr/>
        </Row>

        {/*Opcode dropdown selection*/}
        <Row>
          <Col className = 'flex col-sm-3'>
            <span style={{ fontWeight: 'bold' }}>Select Opcode</span>
            <Dropdown>
              <Dropdown.Toggle variant="success" id="dropdown-basic">
              {selectedOpCode}
              </Dropdown.Toggle>
              <Dropdown.Menu>
                {opcodeList.map((option, index) => (
                <Dropdown.Item key={index} onClick={handleOpCodeSelection(option)}>
                  {option}
                </Dropdown.Item>
                ))}
              </Dropdown.Menu>
            </Dropdown>
          </Col>
                  
          {/*First argument dropdown selection*/}
          <Col className = 'flex col-sm-3'>
          <span style={{ fontWeight: 'bold' }}>First Argument</span>
            <Dropdown>
              <Dropdown.Toggle variant="success" id="dropdown-basic">
                {firstArg}
              </Dropdown.Toggle>
              <Dropdown.Menu>
                {firstArgList.map((option, index) => (
                  <Dropdown.Item key={index} onClick={handleFirstArgSelection(option)}>
                    {option}
                  </Dropdown.Item>
                ))}
              </Dropdown.Menu>
            </Dropdown>
          </Col>
        </Row>

        {/*Renders input field if required-- 
        renders submit button if first arg and opcode have been selected*/}
        <Row className='mt-3'>
          <Col className = 'col-sm-6'>
                <Form onSubmit={handleSubmit}>
                {isSecInput ? (
                  <Form.Group controlId="formBasicEmail">
                    <span style={{ fontWeight: 'bold' }}>{fieldName}</span>
                        <Form.Control
                          type="text"
                          placeholder="Enter argument"
                          value={fieldArg}
                          onChange={handleInputChange}
                        />
                   </Form.Group>
                ) : null}
                {fieldArg !== 0 && firstArg !== "None" ? 
                (<Button style ={{position: 'absolute', width: '100px', bottom: 20, left: 25}} variant="primary" type="submit">
                  Submit
                </Button>)
                : null}
              </Form>
          </Col>
        </Row>    
      </Container>
  );

}
