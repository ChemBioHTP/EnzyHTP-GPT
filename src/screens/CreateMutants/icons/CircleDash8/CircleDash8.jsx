/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const CircleDash8 = ({ opacity = "unset", className }) => {
  return (
    <svg
      className={`circle-dash-8 ${className}`}
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
        style={{mixBlendMode: 'multiply'}}
        width="16"
      />
      <path
        className="path"
        d="M3.84997 2.35009C3.27647 2.79018 2.77103 3.31247 2.34997 3.90009L3.14997 4.50009C3.5172 3.99081 3.9549 3.53627 4.44997 3.15009L3.84997 2.35009Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M2.29997 6.15009L1.34997 5.85009C1.10845 6.54077 0.98999 7.26847 0.999972 8.00009H1.99997C1.99794 7.37116 2.09929 6.74616 2.29997 6.15009Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M1.34997 10.2001C1.58185 10.8973 1.91909 11.5549 2.34997 12.1501L3.14997 11.5501C2.78851 11.044 2.50221 10.4882 2.29997 9.90009L1.34997 10.2001Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M3.89997 13.6501C4.49514 14.081 5.15275 14.4182 5.84997 14.6501L6.14997 13.7001C5.56184 13.4979 5.00608 13.2116 4.49997 12.8501L3.89997 13.6501Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M5.84997 1.35009L6.14997 2.30009C6.74604 2.09942 7.37103 1.99806 7.99997 2.00009V1.00009C7.26835 0.990112 6.54065 1.10858 5.84997 1.35009Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M12.1 13.6501C12.6889 13.2111 13.211 12.689 13.65 12.1001L12.85 11.5001C12.4781 12.022 12.0219 12.4783 11.5 12.8501L12.1 13.6501Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M13.7 9.85009L14.65 10.1501C14.8675 9.45352 14.9853 8.72968 15 8.00009H14C14.002 8.62903 13.9007 9.25403 13.7 9.85009Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M14.6 5.80009C14.3681 5.10288 14.0309 4.44526 13.6 3.85009L12.8 4.45009C13.1614 4.9562 13.4477 5.51196 13.65 6.10009L14.6 5.80009Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M12.05 2.30009C11.4548 1.86921 10.7972 1.53197 10.1 1.30009L9.79997 2.25009C10.3881 2.45233 10.9439 2.73863 11.45 3.10009L12.05 2.30009Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M10.15 14.6501L9.84997 13.7001C9.25391 13.9008 8.62891 14.0021 7.99997 14.0001V15.0001C8.72667 14.9568 9.44706 14.8395 10.15 14.6501Z"
        fill="#161616"
      />
    </svg>
  );
};

CircleDash8.propTypes = {
  opacity: PropTypes.string,
};
