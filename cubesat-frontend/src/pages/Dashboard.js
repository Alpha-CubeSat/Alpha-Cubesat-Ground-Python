import { Col, Container, Row } from "react-bootstrap";
import CommandBuilder from "../components/CommandBuilder";
import ImageViewer from "../components/ImageViewer";
import CommandLog from "../components/CommandLog";
import WidgetCard from "../components/WidgetCard";
import CommandSelector from "../components/CommandSelector";
import CommandViewer from "../components/CommandViewer";

// Main CubeSat Control Dashboard
// Contains widgets for command building, command creation, image viewing, and a command history log.
export default function Dashboard() {
  return (
    <Container fluid className="overflow-hidden flex-fill">
      <Row className="gx-5 px-2 h-100">
        <Col sm="2">
          <Row className="h-100 py-2">
            <WidgetCard title="Command Builder" children={<CommandBuilder />} />
          </Row>
        </Col>
        <Col sm="5">
          <Row className="h-50 pt-2">
            <WidgetCard
              title="Command Selector"
              children={<CommandSelector />}
            />
          </Row>
          <Row className="h-50 pt-3 pb-2">
            <WidgetCard title="CubeSat Images" children={<ImageViewer />} />
          </Row>
        </Col>
        <Col sm="5">
          <Row className="h-100 py-2">
            <WidgetCard title="Command History" children={<CommandLog />} />
          </Row>
        </Col>
      </Row>
    </Container>
  );
}
