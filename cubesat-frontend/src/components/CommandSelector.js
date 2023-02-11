import { useState } from "react";

export default function CommandSelector() {
  const [opCode, setOpCode] = useState("None");
  const [opCodeDropdown, setOpCodeDropdown] = useState(false);

  const handleOpCodeDropdown = () => {
    setOpCodeDropdown(!opCodeDropdown);
  };

  const handleOpCodeSelection = (opcode) => () => {
    setOpCode(opcode);
    alert(opcode);
    setOpCodeDropdown(false);
  };

  return (
    <Dropdown
      open={opCodeDropdown}
      trigger={<button onClick={handleOpCodeDropdown}>Dropdown</button>}
      menu={[
        <button onClick={handleOpCodeSelection("Opcode 1")}>Opcode 1</button>,
        <button onClick={handleOpCodeSelection("Opcode 2")}>Opcode 2</button>,
      ]}
    />
  );
}

const Dropdown = ({ open, trigger, menu }) => {
  return (
    <div className="dropdown">
      {trigger}
      {open ? (
        <ul className="menu">
          {menu.map((menuItem, index) => (
            <li key={index} className="menu-item">
              {menuItem}
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
};
