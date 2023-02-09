import {useDashboard} from "../contexts/DashboardProvider";
import {burnwire_arm_time} from "./Commands";
import {Button} from "react-bootstrap";

export default function CommandPalette() {

    // call onCommandSelect when user selects command and pass in the command as a parameter
    const { setSelectedCommand } = useDashboard();

    // for testing only: remove when implementing
    return (
        <Button onClick={() => setSelectedCommand(burnwire_arm_time)}>Test</Button>
    );
}