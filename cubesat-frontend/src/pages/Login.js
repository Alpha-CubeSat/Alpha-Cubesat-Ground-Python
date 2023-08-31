import { useState } from "react";
import { Button, Form } from "react-bootstrap";
import Modal from "react-bootstrap/Modal";
import alpha from "../AlphaPatch.png";
import { useUser } from "../contexts/UserProvider";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(true);
  const { navigate } = useNavigate();

  const { user, login } = useUser();

  const handleClose = () => setShow(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    await login(username, password);
    if (user) {
      navigate("/");
    } else {
      alert("Wrong username or password");
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
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formBasicEmail">
            <Form.Label>Username</Form.Label>
            <Form.Control
              type="username"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </Form.Group>
          <Form.Group controlId="formBasicPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </Form.Group>
          <hr />
          <Button my={10} variant="primary" type="submit">
            Login
          </Button>
        </Form>
      </Modal.Body>
    </Modal>
  );
}
