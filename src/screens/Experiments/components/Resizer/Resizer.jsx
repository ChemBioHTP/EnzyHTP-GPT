/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import "./style.css";

export const Resizer = ({ className }) => {
  return (
    <div className={`resizer ${className}`}>
      <div className="start" />
      <div className="end" />
    </div>
  );
};
