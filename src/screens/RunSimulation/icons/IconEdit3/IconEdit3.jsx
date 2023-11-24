/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const IconEdit3 = ({ color = "#0F62FE", className }) => {
  return (
    <svg
      className={`icon-edit-3 ${className}`}
      fill="none"
      height="16"
      viewBox="0 0 16 16"
      width="16"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g className="g" clipPath="url(#clip0_11307_11273)">
        <path
          className="path"
          d="M7.3335 2.6665H2.66683C2.31321 2.6665 1.97407 2.80698 1.72402 3.05703C1.47397 3.30708 1.3335 3.64622 1.3335 3.99984V13.3332C1.3335 13.6868 1.47397 14.0259 1.72402 14.276C1.97407 14.526 2.31321 14.6665 2.66683 14.6665H12.0002C12.3538 14.6665 12.6929 14.526 12.943 14.276C13.193 14.0259 13.3335 13.6868 13.3335 13.3332V8.6665"
          stroke={color}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          className="path"
          d="M12.3335 1.66665C12.5987 1.40144 12.9584 1.25244 13.3335 1.25244C13.7086 1.25244 14.0683 1.40144 14.3335 1.66665C14.5987 1.93187 14.7477 2.29158 14.7477 2.66665C14.7477 3.04173 14.5987 3.40144 14.3335 3.66665L8.00016 9.99999L5.3335 10.6667L6.00016 7.99999L12.3335 1.66665Z"
          stroke={color}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </g>
      <defs className="defs">
        <clipPath className="clip-path" id="clip0_11307_11273">
          <rect className="rect" fill="white" height="16" width="16" />
        </clipPath>
      </defs>
    </svg>
  );
};

IconEdit3.propTypes = {
  color: PropTypes.string,
};
