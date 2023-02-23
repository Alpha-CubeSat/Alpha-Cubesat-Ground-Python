import { useState } from "react";
import Dropdown from 'react-bootstrap/Dropdown';
import { Container, Row, Col, Button, Form} from 'react-bootstrap';
import {selectArguments, opcodeList } from "./Commands"
import { useDashboard } from "../contexts/DashboardProvider";


export default function CommandSelector() {
  
  const { commandStack, setCommandStack, count, setCount } = useDashboard();

  //Selected argument values
  const [selectedOpCode, setSelectedOpCode] = useState("Select Opcode")
  const [firstArg, setFirstArg] = useState("None")
  const [fieldArg, setFieldArg] = useState([])

  //Handles conditional rendering
  const [firstArgList, setFirstArgList] = useState([])
  const [listInput, setListInput] = useState([])

  //for command title and command description
  const [title, setTitle] = useState("No command selected")
  const [desc, setDesc] = useState("Select a command")

  //Resets command arguments and selects OpCode
  const handleOpCodeSelection = (opcode) => () => {
    setSelectedOpCode(opcode)
    setFirstArgList(selectArguments[opcode].arg)
    setFirstArg("None")
    setListInput([])
    setTitle("No command selected")
    setDesc("Select a command")
  }

  /* Handles the dropdown for the first argument by setting the selected argument
   * equal to firstArg, and checking whether an input field is required.
   */
  const handleFirstArgSelection = (arg1) => () => {
    setFirstArg(arg1)
    setTitle(selectedOpCode + " " + arg1)
    setDesc("Select a command")
    setDesc(selectArguments[selectedOpCode].desc[(selectArguments[selectedOpCode].arg).indexOf(arg1)])

    //If arg1 exists as a key in selectArguments[selectedOpCode], the command requires an input field
    if (arg1 in selectArguments[selectedOpCode]) {
      setListInput(selectArguments[selectedOpCode][arg1])
    }
  }

  //Updates fieldArg to whatever is in the input field
  const handleInputChange = (event, index) => {
    const updatedField = fieldArg
    updatedField[index] = (event.target.value)
    setFieldArg(updatedField)
  }

  //Handles submit button press. 
  function handleSubmit(event) {
    event.preventDefault();
    let new_command = { // substitute variable names as appropriate
      id: count,
      name: selectedOpCode,
      title: firstArg,
      fields: fieldArg,
    };
  setCommandStack([...commandStack, new_command]);
  setCount(count + 1);
  setSelectedOpCode("Select Opcode")
  setFirstArg("None")
  setFieldArg([])
  setListInput([])
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
          <Col className = 'col-sm-8'>
                <Form onSubmit={handleSubmit}>
                {listInput !== [] ? (
                  listInput.map((option,index) => (
                    <Form.Group controlId={index}>
                      <span style={{ fontWeight: 'bold' }}>{option}</span>
                          <Form.Control
                            style={{ fontSize: '20px', height: '50px' }}
                            type="text"
                            placeholder="Enter argument"
                            value={fieldArg[index]}
                            onChange = {(e) => handleInputChange(e, index)}
                          />
                    </Form.Group>
                ))) : null}
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
