import { Container, Navbar, NavDropdown } from "react-bootstrap";
import alpha from "../AlphaPatch.png";
import AdminUserManage from "../pages/AdminUserManage";
import { useState } from "react";
import { useUser } from "../contexts/UserProvider";

// Top Bar
// Shows info such as alpha logo + name, dropdown for logging out and managing users (admin only)
export default function TopBar() {
  const [editShow, setEditShow] = useState(false);
  const { user, logout } = useUser();

  return (
    <>
      <Navbar style={{ backgroundColor: "#595c5f" }} className="header p-1">
        <Container fluid>
          <Navbar.Brand>
            <img src={alpha} width="30" height="30" alt="Alpha Logo" />
          </Navbar.Brand>
          <Navbar.Text className="text-white">
            Alpha CubeSat Mission Control Dashboard
          </Navbar.Text>
          <NavDropdown title="Settings" className="text-white" align="end">
            {user.is_admin && (
              <NavDropdown.Item onClick={() => setEditShow(true)}>
                ADMIN: Edit Users
              </NavDropdown.Item>
            )}
            <NavDropdown.Item onClick={() => logout()}>
              Log Out
            </NavDropdown.Item>
          </NavDropdown>
        </Container>
      </Navbar>
      {/* key prop uses date object to generate random # each time modal is opened to reset state */}
      <AdminUserManage key={new Date()} show={editShow} setShow={setEditShow} />
    </>
  );
}
