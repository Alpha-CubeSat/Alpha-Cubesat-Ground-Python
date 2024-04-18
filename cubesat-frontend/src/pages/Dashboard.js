import { Col, Container, Row } from "react-bootstrap";
import CommandBuilder from "../components/CommandBuilder";
import CaptureViewer from "../components/CaptureViewer";
import CommandHistory from "../components/CommandHistory";
import WidgetCard from "../components/WidgetCard";
import CommandSelector from "../components/CommandSelector";
import DownlinkHistory from "../components/DownlinkHistory";

// Main CubeSat Control Dashboard
// Contains widgets for command building, command creation, capture viewing, and a command history log.
export default function Dashboard() {
  return (
    <Container fluid className="overflow-hidden">
      <Row className="g-x-4.5 px-2 h-100">
        <Col className="dash_height" sm="2">
          <Row className="h-100 py-2">
            <WidgetCard title="Command Builder" children={<CommandBuilder />} />
          </Row>
        </Col>
        <Col sm="5">
          <Row className="row-height-mobile row-height-non-mobile">
            <WidgetCard
              title="Command Selector"
              children={<CommandSelector />}
            />
          </Row>
          <Row className="h-50 pt-3 pb-2">
            <WidgetCard title="CubeSat Captures" children={<CaptureViewer />} />
          </Row>
        </Col>
        <Col className="dash_height" sm="5">
          <Row className="h-50 pt-2">
            <WidgetCard title="Command History" children={<CommandHistory />} />
          </Row>
          <Row className="h-50 pt-3 pb-2">
            <WidgetCard
              title="Recent Downlinks"
              children={<DownlinkHistory />}
            />
          </Row>
        </Col>
      </Row>
    </Container>
  );
}
