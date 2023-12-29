/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const DataTableBodyRow = ({
  slot = false,
  text = true,
  cellText = "Expandable table content",
  size,
  className,
  minHeightClassName,
  descriptionClassName,
  contentClassName,
  border = "/img/border.svg",
}) => {
  return (
    <div className={`data-table-body-row ${className}`}>
      <img
        className={`min-height-3 size-25-${size} ${minHeightClassName}`}
        alt="Min height"
        src="/img/min-height-35.png"
      />
      <img className="border" alt="Border" src={border} />
      <div className={`content-3 size-26-${size} ${contentClassName}`}>
        {text && <div className={`description-2 ${descriptionClassName}`}>{cellText}</div>}
      </div>
    </div>
  );
};

DataTableBodyRow.propTypes = {
  slot: PropTypes.bool,
  text: PropTypes.bool,
  cellText: PropTypes.string,
  size: PropTypes.oneOf(["large", "extra-large", "extra-small", "small", "medium"]),
  border: PropTypes.string,
};
