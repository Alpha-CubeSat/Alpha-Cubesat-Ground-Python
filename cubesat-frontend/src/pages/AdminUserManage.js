import {
  Button,
  Modal,
  Container,
  Col,
  Row,
  Card,
  CloseButton,
  Form,
} from "react-bootstrap";
import InputField from "../components/InputField";
import { useRef, useState } from "react";

// User Management Modal (For admin user only)
// Modal to allow the admin to create usernames + passwords for new users
// as well as deleting current users
export default function AdminUserManage({ show, setShow }) {
  const usernameField = useRef();
  const passwordField = useRef();
  const commandPermField = useRef();
  const [formErrors, setFormErrors] = useState({});
  const [allUsers, setAllUsers] = useState([
    "Admin",
    "Josh",
    "Jonathan",
    "Eric",
  ]);

  // keeps track of which users are added and deleted:
  // added users mapped to password while deleted users mapped to null
  const [statusMap, setStatusMap] = useState({});

  const handleClose = () => {
    setStatusMap({});
    setShow(false);
  };

  const onAddSubmit = (ev) => {
    ev.preventDefault();
    let username = usernameField.current.value;
    let password = passwordField.current.value;

    // TODO: implement send command perm?

    let errors = {};
    if (!username) {
      errors.username = "Username must not be empty.";
    } else if (allUsers.includes(username)) {
      errors.username = "Username already exists.";
    }

    // enforces password requirements: 8+ chars, 1+ lowercase letter, 1+ uppercase letter,
    // 1+ number, and 1+ special char
    let pwd_regex = new RegExp(
      "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*?[_#?!@$%^&*-])(?=.{8,})"
    );
    if (!password || !pwd_regex.test(password)) {
      errors.password =
        "Password must have ≥ 8 chars and ≥ 1 of each: uppercase letters, lowercase letters, numbers, and special chars.";
    }
    setFormErrors(errors);
    if (Object.keys(errors).length > 0) return;

    setAllUsers([...allUsers, username]);
    setStatusMap({ ...statusMap, [username]: password });
  };

  const removeUser = (username) => {
    if (username === "Admin") return; // disallow deleting admin user
    setAllUsers(allUsers.filter((user) => user !== username));
    setStatusMap({ ...statusMap, [username]: null });
  };

  const saveChanges = () => {
    handleClose();

    // api logic
  };

  return (
    <Modal
      show={show}
      onHide={handleClose}
      size="lg"
      backdrop="static"
      keyboard={false}
      scrollable
    >
      <Modal.Header closeButton>
        <Modal.Title>User Management</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container fluid className="p-0">
          <Row>
            {/* Add new user form */}
            <Col sm="7" className="overflow-auto">
              <h5>Add New User</h5>
              <Form onSubmit={onAddSubmit}>
                <InputField
                  label="Username"
                  placeholder="Enter a username"
                  error={formErrors.username}
                  fieldRef={usernameField}
                  className="mb-2"
                />
                <InputField
                  label="Password"
                  placeholder="Enter a password"
                  error={formErrors.password}
                  fieldRef={passwordField}
                  className="mb-2"
                />
                <Form.Check
                  type="checkbox"
                  label="Can Send Commands"
                  ref={commandPermField}
                  className="mb-2 ms-1"
                />
                <Button variant="secondary" type="submit">
                  + Add
                </Button>
              </Form>
            </Col>
            {/* List of current users with remove buttons */}
            <Col>
              <h5>Current Users</h5>
              {allUsers.map((user, i) => (
                <Card key={i} className="m-2">
                  <Card.Body className="pt-2 pb-2">
                    <div className="d-flex">
                      <p className="flex-grow-1 m-0">{user}</p>
                      {user !== "Admin" && (
                        <CloseButton onClick={() => removeUser(user)} />
                      )}
                    </div>
                  </Card.Body>
                </Card>
              ))}
            </Col>
          </Row>
        </Container>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="success" onClick={saveChanges}>
          Save Changes
        </Button>
        <Button variant="secondary" onClick={handleClose}>
          Cancel
        </Button>
      </Modal.Footer>
    </Modal>
  );
}
