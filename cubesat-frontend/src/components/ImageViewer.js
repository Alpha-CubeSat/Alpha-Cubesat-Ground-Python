import { Col, Row, Spinner } from "react-bootstrap";
import { useEffect, useState } from "react";
import ListGroup from "react-bootstrap/ListGroup";
import Image from "react-bootstrap/Image";
import { useApi } from "../contexts/ApiProvider";
import { useDashboard } from "../contexts/DashboardProvider";

// ImageViewer
// Allows user to view the latest images from the CubeSat
export default function ImageViewer() {
  const { imei } = useDashboard();
  const [imageData, setImageData] = useState();
  const [imageList, setImageList] = useState();
  const api = useApi();

  useEffect(() => {
    setImageList();
    setImageData();
    (async () => {
      // fetches last 5 images by default
      const response = await api.get(`/cubesat/img/${imei}/recent`);
      if (response.status === 200) {
        setImageList(response.data["images"]);
      } else {
        setImageList([]);
      }
    })();
  }, [api, imei]);

  const handleImageSelection = async (file) => {
    const response = await api.get(`/cubesat/img/${imei}/${file}`);
    if (response.status === 200) {
      setImageData(response.data);
    }
  };

  return (
    <Row className="h-100">
      {/* Image selection ListGroup */}
      <Col className="col-sm-3">
        <h5>Select Image</h5>
        {imageList === undefined ? (
          <Spinner animation="border" />
        ) : (
          <ListGroup>
            {imageList.length === 0 ? (
              <p>No Images</p>
            ) : (
              imageList.map((item) => (
                <ListGroup.Item
                  key={item}
                  active={imageData !== undefined && imageData["name"] === item} // Set active state for specific item
                  onClick={() => handleImageSelection(item)}
                >
                  {item}
                </ListGroup.Item>
              ))
            )}
          </ListGroup>
        )}
      </Col>
      {/* Renders image if an image is selected */}
      <Col>
        {imageData !== undefined && (
          <Image
            src={`data:image/jpg;base64,${imageData["base64"]}`}
            alt={imageData["name"]}
            title={new Date(
              parseFloat(imageData["timestamp"]) * 1000
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
