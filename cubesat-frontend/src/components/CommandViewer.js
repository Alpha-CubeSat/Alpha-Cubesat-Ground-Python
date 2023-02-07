import {Button, Col, Container, Row} from "react-bootstrap";
import {createRef, useRef, useState} from "react";
import InputField from "./InputField";
import Form from "react-bootstrap/Form";

export default function CommandViewer ({ command }) {

    // store form errors and input field references
    const [formErrors, setFormErrors] = useState({});
    const fieldRefs = useRef([]);

    // fill references list with empty references
    const numFields = command.fields ? command.fields.length : 0;
    if (fieldRefs.current.length !== numFields) {
        fieldRefs.current = Array(numFields).fill()
            .map((_, i) => fieldRefs.current[i] || createRef());
    }

    const onSubmit = async (ev) => {
        ev.preventDefault();

        // validate form inputs
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

        // API request to send command
        console.log({
            name: command.name,
            fields: fieldsBody
        })
    }

    return (
        <>
            <h3>{command.title}</h3>
            <hr />
            <Container fluid className="p-0">
                <Row>
                    <Col sm='8'>
                        <h5>Description</h5>
                        <p>{command.description}</p>
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
                            <Button variant='success' type='submit'>Send Command</Button>
                        </Form>
                    </Col>
                </Row>
            </Container>
        </>
    );
}