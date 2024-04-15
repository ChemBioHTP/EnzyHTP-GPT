/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const Add2 = ({ opacity = "unset", color = "#161616", className }) => {
  return (
<svg xmlns="http://www.w3.org/2000/svg" className={`add ${className}`} width="undefined" height="undefined" viewBox="0 0 32 32">
    <path fill="currentColor" d="M17 15V8h-2v7H8v2h7v7h2v-7h7v-2z"/>
</svg>
  );
};

Add2.propTypes = {
  opacity: PropTypes.string,
  color: PropTypes.string,
};
