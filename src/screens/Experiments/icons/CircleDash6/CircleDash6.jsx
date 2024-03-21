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
        fillOpacity={opacity}
        height="16"
        style={{mixBlendMode:'multiply'}}
        width="16"
      />
      <path
        className="path"
        d="M3.84997 2.35C3.27647 2.79009 2.77103 3.31238 2.34997 3.9L3.14997 4.5C3.5172 3.99072 3.9549 3.53618 4.44997 3.15L3.84997 2.35Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M2.29997 6.15L1.34997 5.85C1.10845 6.54068 0.98999 7.26838 0.999972 8H1.99997C1.99794 7.37106 2.09929 6.74607 2.29997 6.15Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M1.34997 10.2C1.58185 10.8972 1.91909 11.5548 2.34997 12.15L3.14997 11.55C2.78851 11.0439 2.50221 10.4881 2.29997 9.9L1.34997 10.2Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M3.89997 13.65C4.49514 14.0809 5.15275 14.4181 5.84997 14.65L6.14997 13.7C5.56184 13.4978 5.00608 13.2115 4.49997 12.85L3.89997 13.65Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M5.84997 1.35L6.14997 2.3C6.74604 2.09932 7.37103 1.99797 7.99997 2V1C7.26835 0.990021 6.54065 1.10848 5.84997 1.35Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M12.1 13.65C12.6889 13.2111 13.211 12.6889 13.65 12.1L12.85 11.5C12.4781 12.0219 12.0219 12.4782 11.5 12.85L12.1 13.65Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M13.7 9.85L14.65 10.15C14.8675 9.45343 14.9853 8.72959 15 8H14C14.002 8.62894 13.9007 9.25394 13.7 9.85Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M14.6 5.8C14.3681 5.10279 14.0309 4.44517 13.6 3.85L12.8 4.45C13.1614 4.95611 13.4477 5.51187 13.65 6.1L14.6 5.8Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M12.05 2.3C11.4548 1.86912 10.7972 1.53188 10.1 1.3L9.79997 2.25C10.3881 2.45224 10.9439 2.73854 11.45 3.1L12.05 2.3Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M10.15 14.65L9.84997 13.7C9.25391 13.9007 8.62891 14.002 7.99997 14V15C8.72667 14.9567 9.44706 14.8394 10.15 14.65Z"
        fill="#161616"
      />
    </svg>
  );
};

CircleDash6.propTypes = {
  opacity: PropTypes.string,
};
