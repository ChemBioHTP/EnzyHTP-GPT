/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React, { useEffect } from "react";
import { useReducer } from "react";
import { CheckmarkFilled } from "../../screens/Experiments/icons/CheckmarkFilled";

import "../../content/general.css";
import "./style.css";

export const Tile = ({
  descText = "Description",
  showDesc = true,
  showTitle = true,
  titleText = "Title",
  type,
  stateProp,
  className,
  titleClassName,
  descClassName,
  onClick=()=>{}
}) => {
  const [state, dispatch] = useReducer(reducer, {
    type: type || "base",
    state: stateProp || "enabled",
  });

  const handleClick = () => {
    dispatch("click");
    onClick();
  }

  useEffect(() => {
    if (stateProp === "enabled") {   
      dispatch("unclick");
    }
  }, [stateProp]);

  return (
    <div
      className={`workflow-tile ${state.type} ${state.state} ${className}`}
      onClick={handleClick}
    >
      <div className="content">
        {showTitle && (
          <div className={`title ${titleClassName}`}>
            {titleText}
          </div>
        )}

        {showDesc && (
          <div className={`description ${descClassName}`}>
            {descText}
          </div>
        )}

        {(state.state==="selected")&&(<CheckmarkFilled className="checked-node" color="#161616" />)}
      </div> 
    </div>
  );
};

function reducer(state, action) {
  if (state.type === "single-select") {
    switch (action) {
      case "click":
        return {
          state: "selected",
          type: "single-select",
        };
      case "unclick":
        return {
          state: "enabled",
          type: "single-select",
        };
    }
  }

  return state;
}

Tile.propTypes = {
  descText: PropTypes.string,
  showDesc: PropTypes.bool,
  showTitle: PropTypes.bool,
  titleText: PropTypes.string,
  type: PropTypes.oneOf(["multi-select", "single-select", "base"]),
  stateProp: PropTypes.oneOf([
    "enabled",
    "selected",
    "disabled",
  ]),
};
