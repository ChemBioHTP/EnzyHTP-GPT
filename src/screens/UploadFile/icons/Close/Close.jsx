/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const Close = ({ opacity = "unset", fillOpacity = "unset", className }) => {
  return (
    <svg
      className={`close ${className}`}
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
        d="M12 4.7L11.3 4L8 7.3L4.7 4L4 4.7L7.3 8L4 11.3L4.7 12L8 8.7L11.3 12L12 11.3L8.7 8L12 4.7Z"
        fill="#161616"
        fillOpacity={fillOpacity}
      />
    </svg>
  );
};

Close.propTypes = {
  opacity: PropTypes.string,
  fillOpacity: PropTypes.string,
};
