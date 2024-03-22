/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const Checkmark1 = ({ color = "#8D8D8D", stroke = "#8D8D8D", className }) => {
  return (
    <svg
      className={`checkmark-1 ${className}`}
      fill="none"
      height="6"
      viewBox="0 0 6 6"
      width="6"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g className="g" clipPath="url(#clip0_5166_234623)">
        {/* <rect className="rect" fill="white" height="6" style="mix-blend-mode:multiply" width="6" /> */}
        <path
          className="path"
          d="M2.4375 4.49999L0.75 2.81249L1.01513 2.54736L2.4375 3.96955L4.98488 1.42236L5.25 1.68749L2.4375 4.49999Z"
          fill={color}
          stroke={stroke}
        />
      </g>
      <defs className="defs">
        <clipPath className="clip-path" id="clip0_5166_234623">
          <rect className="rect" fill="white" height="6" width="6" />
        </clipPath>
      </defs>
    </svg>
  );
};

Checkmark1.propTypes = {
  color: PropTypes.string,
  stroke: PropTypes.string,
};
