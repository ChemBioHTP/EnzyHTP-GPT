/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const Search = ({ opacity = "unset", color = "#161616", fillOpacity = "unset", className }) => {
  return (
    <svg
      className={`search ${className}`}
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
        d="M14.5 13.7929L10.7239 10.0169C11.6313 8.92758 12.0838 7.53038 11.9872 6.11596C11.8907 4.70153 11.2525 3.37879 10.2055 2.42288C9.15855 1.46698 7.78335 0.951515 6.366 0.983723C4.94865 1.01593 3.59828 1.59333 2.59581 2.59581C1.59333 3.59828 1.01593 4.94865 0.983723 6.366C0.951515 7.78335 1.46698 9.15855 2.42288 10.2055C3.37879 11.2525 4.70153 11.8907 6.11596 11.9872C7.53038 12.0838 8.92758 11.6313 10.0169 10.7239L13.7929 14.5L14.5 13.7929ZM2 6.5C2 5.60998 2.26392 4.73995 2.75838 3.99993C3.25285 3.25991 3.95565 2.68313 4.77792 2.34254C5.60019 2.00194 6.50499 1.91283 7.3779 2.08646C8.25082 2.2601 9.05264 2.68868 9.68198 3.31802C10.3113 3.94735 10.7399 4.74918 10.9135 5.62209C11.0872 6.495 10.998 7.3998 10.6575 8.22207C10.3169 9.04434 9.74008 9.74714 9.00006 10.2416C8.26004 10.7361 7.39001 11 6.5 11C5.30693 10.9987 4.1631 10.5241 3.31948 9.68052C2.47585 8.83689 2.00132 7.69306 2 6.5Z"
        fill={color}
        fillOpacity={fillOpacity}
      />
    </svg>
  );
};

Search.propTypes = {
  opacity: PropTypes.string,
  color: PropTypes.string,
  fillOpacity: PropTypes.string,
};
