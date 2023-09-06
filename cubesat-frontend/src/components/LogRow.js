import { BsCheckCircleFill, BsXCircleFill } from "react-icons/bs";
import { OpCodes } from "./CommandSelector";
import React, { useState, useRef } from 'react';
import Overlay from 'react-bootstrap/Overlay';

export default function LogRow({ entry }) {
  const [show, setShow] = useState(() => entry.commands.map(() => false));
  const targets = useRef(entry.commands.map(() => React.createRef()));

  const toggleTooltip = (index) => {
    const newShow = [...show];
    newShow[index] = !newShow[index];
    setShow(newShow);
  };

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
            command.namespace ? (
              <>
                <p className="clickable-text" ref={targets.current[i]} onClick={() => toggleTooltip(i)}>
                  {command.opcode}
                </p>
                <Overlay target={targets.current[i].current} show={show[i]} placement="right">
                  {props => (
                    <div
                      {...props}
                      style={{
                        position: 'relative',
                        backgroundColor: 'lightblue',
                        padding: '2px 8px',
                        color: 'black',
                        borderRadius: 5,
                        ...props.style,
                      }}
                    >
                      {command.namespace + ":" + command.field + "=" + command.value}
                    </div>
                  )}
                </Overlay>
              </>
            ) : command.opcode))}
        </>
      </td>
      <td>
        {entry.commands.map((command, i) => (
          <p
            key={i}
            title={
              command.opcode === OpCodes.SFR_Override
                ? `${command.namespace}::${command.field} = ${command.value}`
                : ""
            }
          >
            {command.processed === "true"
              ? <BsCheckCircleFill color="green" />
              : <BsXCircleFill color="red" />}
          </p>
        ))}
      </td>
      <td>{new Date(parseFloat(entry.timestamp)).toLocaleString()}</td>
      <td>{entry.message}</td>
    </tr >
  );
}
