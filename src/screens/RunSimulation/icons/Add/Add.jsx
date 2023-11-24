/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const Add = ({ opacity = "unset", color = "#161616", className }) => {
  return (
    <svg
      className={`add ${className}`}
      fill="none"
      height="20"
      viewBox="0 0 20 20"
      width="20"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect
        className="rect"
        fill="white"
        fillOpacity={opacity}
        height="20"
        style={{mixBlendMode: 'multiply'}}
        width="20"
      />
      <path
        className="path"
        d="M10.625 9.375V5H9.375V9.375H5V10.625H9.375V15H10.625V10.625H15V9.375H10.625Z"
        fill={color}
      />
    </svg>
  );
};

Add.propTypes = {
  opacity: PropTypes.string,
  color: PropTypes.string,
};
