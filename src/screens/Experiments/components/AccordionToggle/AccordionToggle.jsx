import PropTypes from "prop-types";
import React, { useState } from "react";
import { ToggleItem } from "../ToggleItem";
import "./style.css";

export const AccordionToggle = ({ text="Input with GUI", state, className, onSwitchClick }) => {
  const [currentState, setCurrentState] = useState(state);

  const handleClick = () => {
    const newState = currentState === "off" ? "on" : "off";
    setCurrentState(newState);
    onSwitchClick(newState);
  };

  return (
    <div className={`accordion-with ${className}`} onClick={handleClick}>
      <div className="accordion-header">
        <div className="text-wrapper">{text}</div>
        {currentState === "off" && <ToggleItem className="toggle-item-instance" size="small" state="enabled" />}

        {currentState === "on" && (
          <div className="toggle">
            <div className="toggle-value">
              <ToggleItem className="instance-node" size="small" state="enabled" />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

AccordionToggle.propTypes = {
  state: PropTypes.oneOf(["off", "on"]).isRequired,
  onSwitchClick: PropTypes.func.isRequired,
};
