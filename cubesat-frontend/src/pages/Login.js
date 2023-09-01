import { useRef, useState } from "react";
import { Button, Form } from "react-bootstrap";
import Modal from "react-bootstrap/Modal";
import alpha from "../AlphaPatch.png";
import { useUser } from "../contexts/UserProvider";
import InputField from "../components/InputField";

export default function Login() {
  const usernameRef = useRef("");
  const passwordRef = useRef("");
  const [formError, setFormError] = useState({});

  const [show, setShow] = useState(true);

  const { login } = useUser();

  const handleClose = () => setShow(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const username = usernameRef.current.value;
    const password = passwordRef.current.value;

    // make sure username and password are non-empty
    let error = {};
    if (!username) error.username = "Username cannot be empty.";
    if (!password) error.password = "Password cannot be empty.";
    setFormError(error);
    if (Object.keys(error).length > 0) return;

    // attempt to login user
    let success = await login(username, password);
    if (!success) {
      setFormError({
        username: "Username or password is incorrect.",
        password: "Username or password is incorrect.",
      });
    }
  };

  return (
    <Modal
      show={show}
      size="md"
      aria-labelledby="contained-modal-title-vcenter"
      centered
      onHide={handleClose}
      backdrop="static"
      keyboard={false}
    >
      <Modal.Header>
        <Modal.Title id="contained-modal-title-vcenter">
          Login Required
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <img
          src={alpha}
          width="200"
          height="200"
          alt="Alpha Logo"
          className="mx-auto d-block"
        />
        <Form noValidate onSubmit={handleSubmit}>
          <InputField
            name="login-username"
            type="username"
            placeholder="Enter username"
            label="Username"
            error={formError.username}
            fieldRef={usernameRef}
          />
          <InputField
            name="login-password"
            type="password"
            placeholder="Enter password"
            label="Password"
            error={formError.password}
            fieldRef={passwordRef}
          />
          <hr />
          <Button my={10} variant="primary" type="submit">
            Login
          </Button>
        </Form>
      </Modal.Body>
    </Modal>
  );
}
