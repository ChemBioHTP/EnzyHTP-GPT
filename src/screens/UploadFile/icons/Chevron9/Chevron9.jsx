/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const Chevron9 = ({ color = "#161616", opacity = "unset", className }) => {
  return (
    <svg
      className={`chevron-9 ${className}`}
      fill="none"
      height="16"
      viewBox="0 0 16 16"
      width="16"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect className="rect" fill="white" height="16" style="mix-blend-mode:multiply" width="16" />
      <path
        className="path"
        d="M8 10.9998L3 5.9998L3.7 5.2998L8 9.5998L12.3 5.2998L13 5.9998L8 10.9998Z"
        fill={color}
        fillOpacity={opacity}
      />
    </svg>
  );
};

Chevron9.propTypes = {
  color: PropTypes.string,
  opacity: PropTypes.string,
};
