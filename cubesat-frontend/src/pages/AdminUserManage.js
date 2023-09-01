import {
  Button,
  Card,
  CloseButton,
  Col,
  Container,
  Form,
  Modal,
  Row,
  Spinner,
} from "react-bootstrap";
import InputField from "../components/InputField";
import { useEffect, useRef, useState } from "react";
import { useApi } from "../contexts/ApiProvider";

// User Management Modal (For admin user only)
// Modal to allow the admin to create usernames + passwords for new users
// as well as deleting current users
export default function AdminUserManage({ show, setShow }) {
  const usernameField = useRef("");
  const passwordField = useRef("");
  // const commandPermField = useRef();
  const [formErrors, setFormErrors] = useState({});

  const [allUsers, setAllUsers] = useState();

  const api = useApi();

  // load list of users with modal opened
  useEffect(() => {
    (async () => {
      const response = await api.get("/user/list");
      if (response.status === 200) {
        setAllUsers(response.data["users"]);
      } else {
        setAllUsers([]);
      }
    })();
  }, [api]);

  const handleClose = () => {
    setShow(false);
  };

  // validates and makes API request to create new GSW users
  const onAddSubmit = async (ev) => {
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
    // let pwd_regex = new RegExp(
    //     "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*?[_#?!@$%^&*-])(?=.{8,})"
    // );
    // if (!password || !pwd_regex.test(password)) {
    //   errors.password =
    //       "Password must have ≥ 8 chars and ≥ 1 of each: uppercase letters, lowercase letters, numbers, and special chars.";
    // }

    // temporary, enable restrictions when deployed
    if (!password) {
      errors.password = "Password must not be empty";
    }
    setFormErrors(errors);
    if (Object.keys(errors).length > 0) return;

    const response = await api.post("/user/", {
      username: username,
      password: password,
    });
    if (response.status === 200) {
      setAllUsers([...allUsers, username]);
    }
  };

  // makes API request to remove GSW users
  const removeUser = async (username) => {
    if (username === "admin") return; // disallow deleting admin user
    const response = await api.delete("/user/?username=" + username);
    if (response.status === 204) {
      setAllUsers(allUsers.filter((user) => user !== username));
    }
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
                  className="mb-3"
                />
                {/*<Form.Check*/}
                {/*  type="checkbox"*/}
                {/*  label="Can Send Commands"*/}
                {/*  ref={commandPermField}*/}
                {/*  className="mb-2 ms-1"*/}
                {/*/>*/}
                <Button variant="secondary" type="submit">
                  + Add
                </Button>
              </Form>
            </Col>
            {/* List of current users with remove buttons */}
            <Col>
              <h5>Current Users</h5>
              {allUsers === undefined ? (
                <Spinner animation="border" />
              ) : (
                <>
                  {allUsers.map((user, i) => (
                    <Card key={i} className="m-2">
                      <Card.Body className="pt-2 pb-2">
                        <div className="d-flex">
                          <p className="flex-grow-1 m-0">{user}</p>
                          {user !== "admin" && (
                            <CloseButton onClick={() => removeUser(user)} />
                          )}
                        </div>
                      </Card.Body>
                    </Card>
                  ))}
                </>
              )}
            </Col>
          </Row>
        </Container>
      </Modal.Body>
    </Modal>
  );
}
