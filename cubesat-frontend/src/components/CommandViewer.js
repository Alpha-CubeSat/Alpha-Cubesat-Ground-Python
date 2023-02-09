import {Button, Col, Container, Row} from "react-bootstrap";
import {createRef, useRef, useState} from "react";
import InputField from "./InputField";
import Form from "react-bootstrap/Form";
import {useDashboard} from "../contexts/DashboardProvider";

// Command Viewer
// Shows the title and description for a selected command.
// Allows user to enter in command arguments (if they exist) and send commands.
export default function CommandViewer() {

    // declare shared variables
    const { selectedCommand : command, commandLog, setCommandLog } = useDashboard();

    // check if a command is selected
    const commandSelected = Object.keys(command).length !== 0

    // store form errors and input field references
    const [formErrors, setFormErrors] = useState({});
    const fieldRefs = useRef([]);

    // fill input references list with empty references
    const numFields = command.fields ? command.fields.length : 0;
    if (fieldRefs.current.length !== numFields) {
        fieldRefs.current = Array(numFields).fill()
            .map((_, i) => fieldRefs.current[i] || createRef());
    }

    const onSubmit = async (ev) => {
        ev.preventDefault();

        // validate form inputs and return if fields are invalid
        let errors = {};
        let fieldsBody = {};
        for (let field of fieldRefs.current) {
            if (!field.current.value) {
                errors[field.current.id] = 'Field must not be empty.';
            } else {
                fieldsBody[field.current.id] = field.current.value;
            }
        }
        setFormErrors(errors);
        if (Object.keys(errors).length > 0) return;

        // API request to send command
        let response = { // mock api response
            name: command.name,
            fields: fieldsBody,
            submitted: new Date().toLocaleString(),
            status: 'success',
            message: 'command successfully transmitted'
        }

        // update command log with API response
        setCommandLog([response, ...commandLog])
    }

    return (
        <>
            <h3>{commandSelected ? command.title : 'No Command Selected'}</h3>
            <hr />
            <Container fluid className="p-0">
                <Row>
                    <Col sm='8'>
                        <h5>Description</h5>
                        <p>{commandSelected ? command.description : 'Select a command.'}</p>
                    </Col>
                    {/* Command Input Fields + Submission */}
                    <Col sm='4'>
                        <Form onSubmit={onSubmit}>
                            {numFields > 0 && <b>Fields</b>}
                            {numFields > 0 && command.fields.map((field, i) =>
                                <InputField className='mb-2' key={field.title} name={'field'+i}
                                            label={field.title} type='number'
                                            error={formErrors['field'+i]} fieldRef={fieldRefs.current[i]} />)
                            }
                            <Button variant='success' type='submit' disabled={!commandSelected}>Send Command</Button>
                        </Form>
                    </Col>
                </Row>
            </Container>
        </>
    );
}