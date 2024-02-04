/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Resizer } from "../Resizer";
import "./style.css";

export const DataTableRowCell = ({
  showText = true,
  cellText = "Content",
  slot = false,
  size,
  state,
  className,
  minHeightClassName,
  resizerResizerClassName,
}) => {
  return (
    <div className={`data-table-row-cell size-7-${size} state-7-${state} ${className}`}>
      <Resizer className={resizerResizerClassName} />
      <div className="cell">
        <div className="content">{showText && <div className="text-2">{cellText}</div>}</div>
        <img className={`min-height ${minHeightClassName}`} alt="Min height" src="/img/min-height-35.png" />
      </div>
    </div>
  );
};

DataTableRowCell.propTypes = {
  showText: PropTypes.bool,
  cellText: PropTypes.string,
  slot: PropTypes.bool,
  size: PropTypes.oneOf(["large", "extra-large", "extra-small", "small", "medium"]),
  state: PropTypes.oneOf(["disabled", "focus", "enabled"]),
};
