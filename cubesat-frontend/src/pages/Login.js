import { useState } from 'react';
import { Form, Button, Row, Col} from 'react-bootstrap';
import Modal from 'react-bootstrap/Modal';

//temp dictionary with login information
export const loginDict = {
    "username" : 1,
    "password" : 1
}

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [show, setShow] = useState(true);

  const handleClose = () => setShow(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("test")
    //Temporary code using loginDict before setting up user database
    if (username in loginDict && password in loginDict) {handleClose();}
    else alert('wrong username or password');
  };

  return (
    <Modal
      show ={show} 
      size="md"
      aria-labelledby="contained-modal-title-vcenter"
      centered
      onHide = {handleClose}
      backdrop="static" 
      keyboard={false}
    >
      <Modal.Header>
        <Modal.Title id="contained-modal-title-vcenter">
          Login Required
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
          <Form onSubmit={handleSubmit}>
              <Form.Group controlId="formBasicEmail">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                  type="username"
                  placeholder="Enter username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  />
              </Form.Group>
              <Form.Group controlId="formBasicPassword">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  />
            </Form.Group>
            <hr />
            <Button my = {10} variant="primary" type="submit">
              Submit
            </Button>
          </Form>
      </Modal.Body>
    </Modal>
  );
}
