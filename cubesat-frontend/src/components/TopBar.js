import { Container, Navbar, NavDropdown } from "react-bootstrap";
import alpha from "../AlphaPatch.png";
import AdminUserManage from "../pages/AdminUserManage";
import { useState } from "react";
import { useUser } from "../contexts/UserProvider";
import { useDashboard } from "../contexts/DashboardProvider";
import { IMEI_MAP } from "../constants";
import ImeiManage from "../pages/ImeiManage";

// Top Bar
// Shows info such as alpha logo + name, dropdown for logging out and managing users (admin only)
export default function TopBar() {
  const [userManageShow, setUserManageShow] = useState(false);
  const [imeiManageShow, setImeiManageShow] = useState(false);
  const { user, logout } = useUser();
  const { imei } = useDashboard();

  return (
    <>
      <Navbar style={{ backgroundColor: "#595c5f" }} className="header p-1">
        <Container fluid>
          <Navbar.Brand>
            <img src={alpha} width="30" height="30" alt="Alpha Logo" />
          </Navbar.Brand>
          <Navbar.Text className="text-white">
            Alpha CubeSat Mission Control Dashboard <i>({IMEI_MAP[imei]})</i>
          </Navbar.Text>
          <NavDropdown title="Settings" className="text-white" align="end">
            <NavDropdown.Item onClick={() => setImeiManageShow(true)}>
              Change Active IMEI
            </NavDropdown.Item>
            {user.is_admin && (
              <NavDropdown.Item onClick={() => setUserManageShow(true)}>
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
      {user.is_admin && (
        <AdminUserManage
          key={new Date()}
          show={userManageShow}
          setShow={setUserManageShow}
        />
      )}
      <ImeiManage show={imeiManageShow} setShow={setImeiManageShow} />
    </>
  );
}
