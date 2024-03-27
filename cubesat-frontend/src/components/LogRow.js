import { BsCheckCircleFill, BsQuestionCircleFill, BsXCircleFill } from "react-icons/bs";
import React, { useRef, useState } from "react";
import Overlay from "react-bootstrap/Overlay";
import { isDeploymentOpcode, stringifyCommand } from "../constants";

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
          !isDeploymentOpcode(command.opcode) ? (
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
                    {stringifyCommand(command)}
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
          <p key={i}>
            {command.processed === "processed" && <BsCheckCircleFill color="green" />}
            {command.processed === "missing" && <BsXCircleFill color="red" />}
            {command.processed === "unknown" && <BsQuestionCircleFill color="orange" />}
          </p>
        ))}

      </td>
      {/* timestamp and rockblock message */}
      <td>{new Date(parseFloat(entry.timestamp)).toLocaleString()}</td>
      <td>{entry.message}</td>
    </tr>
  );
}
