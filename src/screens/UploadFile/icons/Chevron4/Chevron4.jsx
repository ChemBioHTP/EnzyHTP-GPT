/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const Chevron4 = ({ color = "#525252", opacity = "unset", className }) => {
  return (
    <svg
      className={`chevron-4 ${className}`}
      fill="none"
      height="16"
      viewBox="0 0 16 16"
      width="16"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect className="rect" fill="white" height="16" style="mix-blend-mode:multiply" width="16" />
      <path className="path" d="M8 5L13 10L12.3 10.7L8 6.4L3.7 10.7L3 10L8 5Z" fill={color} fillOpacity={opacity} />
    </svg>
  );
};

Chevron4.propTypes = {
  color: PropTypes.string,
  opacity: PropTypes.string,
};
