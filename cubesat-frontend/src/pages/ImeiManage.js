import { Container, Form, Modal } from "react-bootstrap";
import { useDashboard } from "../contexts/DashboardProvider";
import { IMEI_MAP } from "../constants";
import { useState } from "react";

// IMEI Management Modal
// Allows user to change the active RockBlock IMEI commands are being sent to
export default function ImeiManage({ show, setShow }) {
  const { imei, setImei } = useDashboard();
  const [remember, setRemember] = useState(true);

  // update imei and saved local storage value
  const updateImei = (newImei) => {
    setImei(newImei);
    if (remember) localStorage.setItem("IMEI", newImei);
    else localStorage.removeItem("IMEI");
  };

  // toggle whether to save imei in local storage
  const updateRemember = () => {
    if (remember) localStorage.removeItem("IMEI");
    else localStorage.setItem("IMEI", imei);
    setRemember(!remember);
  };

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
              onChange={() => updateImei(imei_num)}
              className="mb-3"
            />
          ))}
        </Container>
        <Form.Check
          name="imei_remember"
          label="Remember IMEI Selection"
          defaultChecked={true}
          onChange={() => updateRemember()}
        />
      </Modal.Body>
    </Modal>
  );
}
