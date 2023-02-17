import {Card} from "react-bootstrap";

// Widget Card
// Allows main dashboard components to be displayed separately from each other
export default function WidgetCard({ title, children }) {
  return (
    <Card className="p-0 h-100">
      <Card.Header className="bg-dark bg-opacity-75 text-light">
        {title}
      </Card.Header>
      <Card.Body className="overflow-auto">{children}</Card.Body>
    </Card>
  );
}
