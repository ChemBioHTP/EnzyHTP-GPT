/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";

export const ArrowRight = ({ className }) => {
  return (
    <svg
      className={`arrow-right ${className}`}
      fill="none"
      height="20"
      viewBox="0 0 20 20"
      width="20"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect className="rect" fill="white" height="20" style="mix-blend-mode:multiply" width="20" />
      <path
        className="path"
        d="M11.25 3.75L10.3562 4.62063L15.0938 9.375H2.5V10.625H15.0938L10.3562 15.3581L11.25 16.25L17.5 10L11.25 3.75Z"
        fill="#0F62FE"
      />
    </svg>
  );
};
