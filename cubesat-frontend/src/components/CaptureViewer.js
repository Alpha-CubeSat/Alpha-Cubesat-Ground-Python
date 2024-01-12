import {Col, Row, Spinner} from "react-bootstrap";
import {useEffect, useState} from "react";
import ListGroup from "react-bootstrap/ListGroup";
import Image from "react-bootstrap/Image";
import {useApi} from "../contexts/ApiProvider";
import {useDashboard} from "../contexts/DashboardProvider";

// CaptureViewer
// Allows user to view the latest captures from the CubeSat
export default function CaptureViewer() {
  const { imei } = useDashboard();
  const [captureData, setCaptureData] = useState();
  const [captureList, setCaptureList] = useState();
  const api = useApi();

  useEffect(() => {
    setCaptureList();
    setCaptureData();
    (async () => {
      // fetches last 5 captures by default
      const response = await api.get(`/cubesat/capture/${imei}/recent`);
      if (response.status === 200) {
        setCaptureList(response.data["captures"]);
      } else {
        setCaptureList([]);
      }
    })();
  }, [api, imei]);

  const handleCaptureSelection = async (file) => {
    const response = await api.get(`/cubesat/capture/${imei}/${file}`);
    if (response.status === 200) {
      setCaptureData(response.data);
    }
  };

  return (
    <Row className="h-100">
      {/* Capture selection ListGroup */}
      <Col className="col-sm-3">
        <h5>Select Capture</h5>
        {captureList === undefined ? (
          <Spinner animation="border" />
        ) : (
          <ListGroup>
            {captureList.length === 0 ? (
              <p>No Captures</p>
            ) : (
              captureList.map((item) => (
                <ListGroup.Item
                  key={item}
                  active={captureData !== undefined && captureData["name"] === item} // Set active state for specific item
                  onClick={() => handleCaptureSelection(item)}
                >
                  {item}
                </ListGroup.Item>
              ))
            )}
          </ListGroup>
        )}
      </Col>
      {/* Renders capture if an capture is selected */}
      <Col>
        {captureData !== undefined && (
          <Image
            src={`data:image/jpg;base64,${captureData["base64"]}`}
            alt={captureData["name"]}
            title={new Date(
              parseFloat(captureData["timestamp"]) * 1000
            ).toLocaleString()}
            className="h-100 mx-auto d-block"
            fluid
            rounded
          />
        )}
      </Col>
    </Row>
  );
}
