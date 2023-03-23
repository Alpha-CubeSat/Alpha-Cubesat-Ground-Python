import { Container, Navbar } from "react-bootstrap";
import alpha from "../AlphaPatch.png";

export default function TopBar() {
  return (
    <Navbar style={{ backgroundColor: "#595c5f" }} className="p-1">
      <Container fluid>
        <Navbar.Brand>
          <img src={alpha} width="30" height="30" alt="Alpha Logo" />
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
}
