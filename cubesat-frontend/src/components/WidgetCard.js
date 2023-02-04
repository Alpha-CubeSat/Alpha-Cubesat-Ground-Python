import {Card} from "react-bootstrap";

export default function WidgetCard({ title, children }) {
    return (
        <Card className='mb-3 p-0'>
            <Card.Header className='bg-dark bg-opacity-75 text-light'>{title}</Card.Header>
            <Card.Body>
                {children}
            </Card.Body>
        </Card>
    );
}