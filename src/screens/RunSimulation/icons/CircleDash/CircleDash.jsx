/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const CircleDash = ({ opacity = "unset", className }) => {
  return (
    <svg
      className={`circle-dash ${className}`}
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
        d="M3.85 2.35C3.27649 2.79009 2.77105 3.31238 2.35 3.9L3.15 4.5C3.51722 3.99071 3.95493 3.53617 4.45 3.15L3.85 2.35Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M2.3 6.15L1.35 5.85C1.10848 6.54068 0.990016 7.26838 0.999998 8H2C1.99797 7.37106 2.09932 6.74606 2.3 6.15Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M1.35 10.2C1.58188 10.8972 1.91912 11.5548 2.35 12.15L3.15 11.55C2.78854 11.0439 2.50224 10.4881 2.3 9.9L1.35 10.2Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M3.9 13.65C4.49516 14.0809 5.15278 14.4181 5.85 14.65L6.15 13.7C5.56187 13.4978 5.0061 13.2115 4.5 12.85L3.9 13.65Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M5.85 1.35L6.15 2.3C6.74606 2.09932 7.37106 1.99797 8 2V0.999998C7.26838 0.990016 6.54068 1.10848 5.85 1.35Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M12.1 13.65C12.6889 13.2111 13.2111 12.6889 13.65 12.1L12.85 11.5C12.4782 12.0219 12.0219 12.4782 11.5 12.85L12.1 13.65Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M13.7 9.85L14.65 10.15C14.8675 9.45343 14.9853 8.72959 15 8H14C14.002 8.62894 13.9007 9.25393 13.7 9.85Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M14.6 5.8C14.3681 5.10278 14.0309 4.44516 13.6 3.85L12.8 4.45C13.1615 4.9561 13.4478 5.51187 13.65 6.1L14.6 5.8Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M12.05 2.3C11.4548 1.86912 10.7972 1.53188 10.1 1.3L9.8 2.25C10.3881 2.45224 10.9439 2.73854 11.45 3.1L12.05 2.3Z"
        fill="#161616"
      />
      <path
        className="path"
        d="M10.15 14.65L9.85 13.7C9.25393 13.9007 8.62894 14.002 8 14V15C8.7267 14.9567 9.44709 14.8394 10.15 14.65Z"
        fill="#161616"
      />
    </svg>
  );
};

CircleDash.propTypes = {
  opacity: PropTypes.string,
};
