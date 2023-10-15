import { Container, Form, Modal } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import { IMEI_MAP } from "../constants";

// IMEI Management Modal
// Allows user to change the active RockBlock IMEI commands are being sent to
export default function ImeiManage({ show, setShow }) {
  const { imei, setImei } = useDashboard();

  return (
    <Modal show={show} onHide={() => setShow(false)}>
      <Modal.Header closeButton>
        <Modal.Title>Change Active IMEI</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container fluid className="p-0">
          {Object.entries(IMEI_MAP).map(([imei_num, name], i) => (
            <Form.Check
              key={i}
              name="imei_select"
              label={name + " (" + imei_num + ")"}
              type="radio"
              defaultChecked={imei_num === imei}
              onChange={() => setImei(imei_num)}
              className="mb-3"
            />
          ))}
        </Container>
      </Modal.Body>
    </Modal>
  );
}
