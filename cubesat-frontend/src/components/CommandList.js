import { useDashboard } from "../contexts/DashboardProvider";
import CommandCard from "./CommandCard";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import update from "immutability-helper";

// Command List (component of CommandBuilder)
// Provides drag and drop interface to allow easy reordering + deletion of commands.
export default function CommandList() {
  const { commandStack, setCommandStack } = useDashboard();

  // callback function when command position changed due to drag/drop
  const moveCommand = (dragIndex, hoverIndex) => {
    setCommandStack(
      update(commandStack, {
        $splice: [
          // Remove the previous reference of dragged element
          [dragIndex, 1],
          // Copy the dragged command before hovered element
          [hoverIndex, 0, commandStack[dragIndex]],
        ],
      })
    );
  };

  // callback function to delete a command from the stack
  const deleteCommand = (index) => {
    setCommandStack([
      ...commandStack.slice(0, index),
      ...commandStack.slice(index + 1),
    ]);
  };

  return (
    <>
      {commandStack.length === 0 && <p>No commands</p>}
      <DndProvider backend={HTML5Backend}>
        {commandStack.map((cmd, i) => (
          <CommandCard
            key={cmd.id}
            index={i}
            command={cmd}
            moveCommand={moveCommand}
            deleteCommand={deleteCommand}
          />
        ))}
      </DndProvider>
    </>
  );
}
