import {Col, Container, Row} from "react-bootstrap";
import CommandPalette from "../components/CommandPalette";
import CommandViewer from "../components/CommandViewer";
import ImageViewer from "../components/ImageViewer";
import CommandLog from "../components/CommandLog";
import WidgetCard from "../components/WidgetCard";
import DashboardProvider from "../contexts/DashboardProvider";

// Main CubeSat Control Dashboard
// Contains widgets for command selection, command sending, image viewing, and a command history log.
export default function Dashboard() {

    return (
        <DashboardProvider>
            <Container fluid className='overflow-hidden'>
                <Row className='gx-5 px-2'>
                    <Col sm='2'>
                        <Row className='vh-100 py-2'>
                            <WidgetCard title='Commands' children={<CommandPalette />} />
                        </Row>
                    </Col>
                    <Col sm='5'>
                        <Row className='h-50 pt-2'>
                            <WidgetCard title='Command Selection' children={<CommandViewer />} />
                        </Row>
                        <Row className='h-50 pt-3 pb-2'>
                            <WidgetCard title='CubeSat Images' children={<ImageViewer />} />
                        </Row>
                    </Col>
                    <Col sm='5'>
                        <Row className='vh-100 py-2'>
                            <WidgetCard title='Command History' children={<CommandLog />} />
                        </Row>
                    </Col>
                </Row>
            </Container>
        </DashboardProvider>
    );
}