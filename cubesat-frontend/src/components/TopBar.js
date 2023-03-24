import { Container, Navbar, NavDropdown } from "react-bootstrap";
import alpha from "../AlphaPatch.png";
import AdminEditUsers from "../pages/AdminEditUsers";
import { useState } from "react";

export default function TopBar() {
  const [editShow, setEditShow] = useState(false);

  return (
    <>
      <Navbar style={{ backgroundColor: "#595c5f" }} className="p-1">
        <Container fluid>
          <Navbar.Brand>
            <img src={alpha} width="30" height="30" alt="Alpha Logo" />
          </Navbar.Brand>
          <Navbar.Text className="text-white">
            Alpha CubeSat Mission Control Dashboard
          </Navbar.Text>
          <NavDropdown title="Settings" className="text-white" align="end">
            <NavDropdown.Item onClick={() => setEditShow(true)}>
              ADMIN: Edit Users
            </NavDropdown.Item>
            <NavDropdown.Item>Log Out</NavDropdown.Item>
          </NavDropdown>
        </Container>
      </Navbar>
      <AdminEditUsers show={editShow} setShow={setEditShow} />
    </>
  );
}
