import {createContext, useContext, useState} from "react";

const DashboardContext = createContext();

// Dashboard Context Provider
// Contains variables shared across different widgets to make access/updating easier.
export default function DashboardProvider({ children }) {

    // notify command viewer when user selects command
    const [selectedCommand, setSelectedCommand] = useState({});

    // ***grab prev command history from api on initial render

    // notify command log of API response when user sends command
    const [commandLog, setCommandLog] = useState([
        {
            name: 'mission_mode_low_power',
            fields: [],
            submitted: new Date().toLocaleString(),
            status: 'success',
            message: 'command successfully transmitted'
        },
        {
            name: 'burnwire_burn_time',
            fields: [],
            submitted: new Date().toLocaleString(),
            status: 'failure',
            message: 'connection timed out'
        },
        {
            name: 'take_photo_true',
            fields: [],
            submitted: new Date().toLocaleString(),
            status: 'failure',
            message: 'connection timed out'
        }
    ]);

    return (
        <DashboardContext.Provider value={{selectedCommand, setSelectedCommand, commandLog, setCommandLog}}>
            {children}
        </DashboardContext.Provider>
    );
}

export function useDashboard() {
    return useContext(DashboardContext);
}