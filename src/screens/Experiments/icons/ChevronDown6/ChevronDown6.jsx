/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const ChevronDown6 = ({ opacity = "unset", fillOpacity = "unset", className }) => {
  return (
    <svg
      className={`chevron-down-6 ${className}`}
      fill="none"
      height="16"
      viewBox="0 0 16 16"
      width="16"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect
        className="rect"
        fill="white"
        fillOpacity={opacity}
        height="16"
        style={{mixBlendMode:'multiply'}}
        width="16"
      />
      <path
        className="path"
        d="M8 11L3 5.99999L3.7 5.29999L8 9.59999L12.3 5.29999L13 5.99999L8 11Z"
        fill="#161616"
        fillOpacity={fillOpacity}
      />
    </svg>
  );
};

ChevronDown6.propTypes = {
  opacity: PropTypes.string,
  fillOpacity: PropTypes.string,
};
