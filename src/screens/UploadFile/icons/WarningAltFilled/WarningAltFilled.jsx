/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const WarningAltFilled = ({ opacity = "unset", color = "#161616", className }) => {
  return (
    <svg
      className={`warning-alt-filled ${className}`}
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
        style="mix-blend-mode:multiply"
        width="16"
      />
      <path
        className="path"
        d="M8.001 3.08571H7.999L2.32435 13.9983L2.3253 14H13.6747L13.6757 13.9983L8.001 3.08571ZM7.4375 6.00001H8.5625V10.5H7.4375V6.00001ZM8 13C7.85167 13 7.70666 12.956 7.58333 12.8736C7.45999 12.7912 7.36386 12.6741 7.30709 12.537C7.25033 12.4 7.23548 12.2492 7.26441 12.1037C7.29335 11.9582 7.36478 11.8246 7.46967 11.7197C7.57456 11.6148 7.7082 11.5434 7.85369 11.5144C7.99917 11.4855 8.14997 11.5003 8.28702 11.5571C8.42406 11.6139 8.54119 11.71 8.62361 11.8333C8.70602 11.9567 8.75 12.1017 8.75 12.25C8.75 12.4489 8.67099 12.6397 8.53033 12.7803C8.38968 12.921 8.19892 13 8 13Z"
        fill={color}
      />
      <path
        className="path"
        d="M14.5 15H1.5C1.4141 15 1.32965 14.9779 1.25478 14.9357C1.17992 14.8936 1.11718 14.8329 1.0726 14.7595C1.02802 14.686 1.00311 14.6024 1.00027 14.5165C0.997436 14.4307 1.01677 14.3455 1.0564 14.2693L7.5564 1.76931C7.59862 1.68812 7.66231 1.62008 7.74053 1.5726C7.81875 1.52511 7.9085 1.5 8 1.5C8.09151 1.5 8.18126 1.52511 8.25948 1.5726C8.3377 1.62008 8.40138 1.68812 8.4436 1.76931L14.9436 14.2693C14.9832 14.3455 15.0026 14.4307 14.9997 14.5165C14.9969 14.6024 14.972 14.686 14.9274 14.7595C14.8828 14.8329 14.8201 14.8936 14.7452 14.9357C14.6704 14.9779 14.5859 15 14.5 15ZM2.3253 14H13.6747L13.6757 13.9983L8.001 3.08571H7.999L2.32435 13.9983L2.3253 14Z"
        fill={color}
      />
    </svg>
  );
};

WarningAltFilled.propTypes = {
  opacity: PropTypes.string,
  color: PropTypes.string,
};
