import { BsCheckCircleFill, BsXCircleFill } from "react-icons/bs";
// import { useState } from "react";
// import { Button, Collapse } from "react-bootstrap";

// LogRow (component of CommandLog)
// Shows the status, command name, command fields, submission time, an API response message
// for every sent command
export default function LogRow({ entry }) {
  // const [fieldsOpen, setOpen] = useState(false);

  return (
    <tr>
      <td>
        {entry.status === "success" ? (
          <BsCheckCircleFill color="green" />
        ) : (
          <BsXCircleFill color="red" />
        )}
      </td>
      <td>
        <>
          {entry.commands.map((command, i) => (
            // TODO: find better way to seperate commands + show command arguments
            <p
              key={i}
              title={Object.entries(command.args).map(([k, v]) => k + ": " + v)}
            >
              {command.operation}
            </p>
          ))}
          {/*  Button to view command fields if they exist */}
          {/*{Object.entries(entry.fields).length > 0 && (*/}
          {/*  <>*/}
          {/*    <Button*/}
          {/*      onClick={() => setOpen(!fieldsOpen)}*/}
          {/*      variant="secondary"*/}
          {/*      size="sm"*/}
          {/*      aria-controls="fields-text"*/}
          {/*      aria-expanded={fieldsOpen}*/}
          {/*    >*/}
          {/*      View Fields*/}
          {/*    </Button>*/}
          {/*    <Collapse in={fieldsOpen}>*/}
          {/*      <div id="fields-text" className="py-2">*/}
          {/*        {Object.entries(entry.fields).map(([k, v]) => k + ": " + v)}*/}
          {/*      </div>*/}
          {/*    </Collapse>*/}
          {/*  </>*/}
          {/*)}*/}
        </>
      </td>
      <td>{new Date(parseFloat(entry.timestamp)).toLocaleString()}</td>
      <td>{entry.error_message}</td>
    </tr>
  );
}