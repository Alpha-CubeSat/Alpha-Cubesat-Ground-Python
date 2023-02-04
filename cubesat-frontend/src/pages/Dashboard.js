import {Col, Container, Row} from "react-bootstrap";
import CommandPalette from "../components/CommandPalette";
import CommandViewer from "../components/CommandViewer";
import ImageViewer from "../components/ImageViewer";
import CommandLog from "../components/CommandLog";
import WidgetCard from "../components/WidgetCard";

export default function Dashboard() {
    return (
        <Container fluid className='overflow-hidden'>
            <Row className='gx-5'>
                <Col lg='2'>
                    <Row className='vh-100'>
                        <WidgetCard title='Commands' children={<CommandPalette />} />
                    </Row>
                </Col>
                <Col lg='5'>
                    <Row className='h-50'>
                        <WidgetCard title='Command Selection' children={<CommandViewer />} />
                    </Row>
                    <Row className='h-50'>
                        <WidgetCard title='CubeSat Images' children={<ImageViewer />} />
                    </Row>
                </Col>
                <Col lg='5'>
                    <Row className='vh-100'>
                        <WidgetCard title='Command History' children={<CommandLog />} />
                    </Row>
                </Col>
            </Row>
        </Container>
    );
}