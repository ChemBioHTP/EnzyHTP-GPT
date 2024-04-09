/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";

export const CheckboxChecked = ({ className }) => {
  return (
    <svg
      className={`checkbox-checked ${className}`}
      fill="none"
      height="20"
      viewBox="0 0 20 20"
      width="20"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect className="rect" fill="white" height="20" style={{ mixBlendMode: 'multiply'}} width="20" />
      <path
        className="path"
        d="M16.25 2.5H3.75C3.41848 2.5 3.10054 2.6317 2.86612 2.86612C2.6317 3.10054 2.5 3.41848 2.5 3.75V16.25C2.5 16.5815 2.6317 16.8995 2.86612 17.1339C3.10054 17.3683 3.41848 17.5 3.75 17.5H16.25C16.5815 17.5 16.8995 17.3683 17.1339 17.1339C17.3683 16.8995 17.5 16.5815 17.5 16.25V3.75C17.5 3.41848 17.3683 3.10054 17.1339 2.86612C16.8995 2.6317 16.5815 2.5 16.25 2.5ZM3.75 16.25V3.75H16.25V16.25H3.75Z"
        fill="#161616"
        fillOpacity="0.25"
      />
      <path
        className="path"
        d="M8.75 13.4375L5.625 10.3375L6.61875 9.375L8.75 11.4688L13.3813 6.875L14.375 7.8625L8.75 13.4375Z"
        fill="#161616"
        fillOpacity="0.25"
      />
    </svg>
  );
};
