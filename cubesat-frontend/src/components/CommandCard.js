import { Accordion, Button } from "react-bootstrap";
import { useRef } from "react";
import { useDrag, useDrop } from "react-dnd";

// Command Card (component of CommandList)
// Shows the title and arguments of a created command.
// Includes drag and drop support to allow easy reordering + deletion
export default function CommandCard({
  index,
  command,
  moveCommand,
  deleteCommand,
}) {
  // serves as unique ID for drag/drop
  const ref = useRef(null);

  // dropping functionality
  const [, drop] = useDrop({
    accept: "Command",
    hover(item) {
      if (!ref.current) return;

      const dragIndex = item.index;
      const hoverIndex = index;
      // If the dragged element is hovered in the same place, then do nothing
      if (dragIndex === hoverIndex) return;

      // If dragged around other elements, update command stack with position changes
      moveCommand(dragIndex, hoverIndex);
      // Update the index for dragged item directly to avoid flickering
      item.index = hoverIndex;
    },
  });

  // dragging functionality
  const [{ isDragging }, drag] = useDrag({
    type: "Command",
    // data of the item to be available to the drop methods
    item: { index },
    // collects additional data for drop handling like whether is currently being dragged
    collect: (monitor) => {
      return {
        isDragging: monitor.isDragging(),
      };
    },
  });

  // initialize drag/drop
  drag(drop(ref));

  return (
    <Accordion
      className="mb-2 p-0"
      ref={ref}
      style={{ opacity: isDragging ? 0 : 1 }}
    >
      <Accordion.Item eventKey="0">
        <Accordion.Header>{index + 1 + ". " + command.name}</Accordion.Header>
        <Accordion.Body>
          <>
            {/* Display all command fields */}
            {Object.entries(command.fields).map(([k, v]) => k + ": " + v)}
            <Button
              onClick={() => deleteCommand(index)}
              variant="link"
              size="sm"
              className="ps-0"
            >
              Delete Command
            </Button>
          </>
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
  );
}
