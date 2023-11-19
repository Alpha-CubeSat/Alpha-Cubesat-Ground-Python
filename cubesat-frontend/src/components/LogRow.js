import { BsCheckCircleFill, BsXCircleFill } from "react-icons/bs";
import { OpCodes } from "./CommandSelector";
import React, { useRef, useState } from "react";
import Overlay from "react-bootstrap/Overlay";

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
      {/* status indicator */}
      <td>
        {entry.status === "success" ? (
          <BsCheckCircleFill color="green" />
        ) : (
          <BsXCircleFill color="red" />
        )}
      </td>
      {/* command(s) */}
      <td>
        {entry.commands.map((command, i) =>
          command.namespace ? (
            <div key={i}>
              <p
                className="clickable-text"
                ref={targets.current[i]}
                onClick={() => toggleTooltip(i)}
              >
                {command.opcode}
              </p>
              <Overlay
                target={targets.current[i]}
                show={show[i]}
                placement="right"
              >
                {({
                  placement: _placement,
                  arrowProps: _arrowProps,
                  show: _show,
                  popper: _popper,
                  hasDoneInitialMeasure: _hasDoneInitialMeasure,
                  ...props
                }) => (
                  <div
                    {...props}
                    style={{
                      position: "relative",
                      backgroundColor: "lightblue",
                      padding: "2px 8px",
                      color: "black",
                      borderRadius: 5,
                      ...props.style,
                    }}
                  >
                    {command.namespace +
                      "::" +
                      command.field +
                      "=" +
                      (command.opcode === "SFR_Override"
                        ? command.value.value
                        : command.value)}
                  </div>
                )}
              </Overlay>
            </div>
          ) : (
            <p key={i}>{command.opcode}</p>
          )
        )}
      </td>
      <td>
        {/* command processed indicator */}
        {entry.commands.map((command, i) => (
          <p
            key={i}
            title={
              command.opcode === OpCodes.SFR_Override
                ? `${command.namespace}::${command.field} = ${command.value}`
                : ""
            }
          >
            {command.processed === "true" ? (
              <BsCheckCircleFill color="green" />
            ) : (
              <BsXCircleFill color="red" />
            )}
          </p>
        ))}
      </td>
      {/* timestamp and rockblock message */}
      <td>{new Date(parseFloat(entry.timestamp)).toLocaleString()}</td>
      <td>{entry.message}</td>
    </tr>
  );
}
