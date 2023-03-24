import {
  Button,
  Modal,
  Container,
  Col,
  Row,
  Card,
  CloseButton,
} from "react-bootstrap";
import InputField from "../components/InputField";
import Form from "react-bootstrap/Form";
import { useRef, useState } from "react";

export default function AdminEditUsers({ show, setShow }) {
  const username = useRef();
  const password = useRef();
  const commandPerm = useRef();
  const [formErrors, setFormErrors] = useState({});
  const [allUsers, setAllUsers] = useState([
    "Admin",
    "Josh",
    "Jonathan",
    "Eric",
  ]);

  const handleClose = () => setShow(false);

  const handleConfirm = () => {
    setShow(false);
  };

  const onSubmit = (ev) => {};

  return (
    <Modal show={show} onHide={handleClose} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>User Management</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container fluid className="p-0">
          <Row>
            <Col sm="7">
              <h5>Add New User</h5>
              <Form onSubmit={onSubmit}>
                <InputField
                  label="Username"
                  placeholder="Enter a username"
                  error={formErrors.username}
                  fieldRef={username}
                />
                <InputField
                  label="Password"
                  placeholder="Enter a password"
                  error={formErrors.password}
                  fieldRef={password}
                />
                <Form.Check
                  type="checkbox"
                  label="Can Send Commands"
                  ref={commandPerm}
                  className="m-2"
                />
                <Button variant="secondary" type="submit" className="mt-2">
                  Add User
                </Button>
              </Form>
            </Col>
            <Col>
              <h5>Current Users</h5>
              {allUsers.map((user, i) => (
                <Card body className="m-2">
                  <div className="d-flex">
                    <p className="flex-grow-1 m-0">{user}</p>
                    <CloseButton
                    // onClick={() => removeUser(user.id)}
                    />
                  </div>
                </Card>
              ))}
            </Col>
          </Row>
        </Container>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="success" onClick={handleConfirm}>
          Save Changes
        </Button>
      </Modal.Footer>
    </Modal>
  );
}
