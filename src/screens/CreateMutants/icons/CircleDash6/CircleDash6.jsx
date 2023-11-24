/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const CircleDash6 = ({ opacity = "unset", className }) => {
  return (
    <svg
      className={`circle-dash-6 ${className}`}
      fill="none"
      height="16"
      viewBox="0 0 16 16"
      width="16"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect
        className="rect"
        fill="white"
        height="16"
        style={{mixBlendMode: 'multiply'}}
        transform="translate(0.000488281 0.000976562)"
        width="16"
      />
      <path
        className="path"
        d="M3.85046 2.35095C3.27696 2.79104 2.77152 3.31333 2.35046 3.90095L3.15046 4.50095C3.51768 3.99166 3.95539 3.53712 4.45046 3.15095L3.85046 2.35095Z"
        fill="#161616"
        fillOpacity={opacity}
      />
      <path
        className="path"
        d="M2.30046 6.15095L1.35046 5.85095C1.10894 6.54163 0.990479 7.26933 1.00046 8.00095H2.00046C1.99843 7.37201 2.09978 6.74701 2.30046 6.15095Z"
        fill="#161616"
        fillOpacity={opacity}
      />
      <path
        className="path"
        d="M1.35046 10.2009C1.58234 10.8982 1.91958 11.5558 2.35046 12.1509L3.15046 11.5509C2.789 11.0448 2.5027 10.4891 2.30046 9.90095L1.35046 10.2009Z"
        fill="#161616"
        fillOpacity={opacity}
      />
      <path
        className="path"
        d="M3.90046 13.6509C4.49563 14.0818 5.15324 14.4191 5.85046 14.6509L6.15046 13.7009C5.56233 13.4987 5.00657 13.2124 4.50046 12.8509L3.90046 13.6509Z"
        fill="#161616"
        fillOpacity={opacity}
      />
      <path
        className="path"
        d="M5.85046 1.35095L6.15046 2.30095C6.74653 2.10027 7.37152 1.99892 8.00046 2.00095V1.00095C7.26884 0.990967 6.54114 1.10943 5.85046 1.35095Z"
        fill="#161616"
        fillOpacity={opacity}
      />
      <path
        className="path"
        d="M12.1005 13.6509C12.6894 13.212 13.2115 12.6899 13.6505 12.1009L12.8505 11.5009C12.4786 12.0229 12.0224 12.4791 11.5005 12.8509L12.1005 13.6509Z"
        fill="#161616"
        fillOpacity={opacity}
      />
      <path
        className="path"
        d="M13.7005 9.85095L14.6505 10.1509C14.868 9.45438 14.9858 8.73054 15.0005 8.00095H14.0005C14.0025 8.62989 13.9011 9.25488 13.7005 9.85095Z"
        fill="#161616"
        fillOpacity={opacity}
      />
      <path
        className="path"
        d="M14.6005 5.80095C14.3686 5.10373 14.0313 4.44612 13.6005 3.85095L12.8005 4.45095C13.1619 4.95706 13.4482 5.51282 13.6505 6.10095L14.6005 5.80095Z"
        fill="#161616"
        fillOpacity={opacity}
      />
      <path
        className="path"
        d="M12.0505 2.30095C11.4553 1.87007 10.7977 1.53283 10.1005 1.30095L9.80046 2.25095C10.3886 2.45319 10.9444 2.73949 11.4505 3.10095L12.0505 2.30095Z"
        fill="#161616"
        fillOpacity={opacity}
      />
      <path
        className="path"
        d="M10.1505 14.6509L9.85046 13.7009C9.25439 13.9016 8.6294 14.003 8.00046 14.0009V15.0009C8.72716 14.9577 9.44755 14.8404 10.1505 14.6509Z"
        fill="#161616"
        fillOpacity={opacity}
      />
    </svg>
  );
};

CircleDash6.propTypes = {
  opacity: PropTypes.string,
};
