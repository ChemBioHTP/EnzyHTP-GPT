/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const ErrorFilled1 = ({ color = "#DA1E28", className }) => {
  return (
    <svg
      className={`error-filled-1 ${className}`}
      fill="none"
      height="16"
      viewBox="0 0 16 16"
      width="16"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect className="rect" fill="white" height="16" style="mix-blend-mode:multiply" width="16" />
      <path
        className="path"
        d="M8.00013 0.999981C7.07929 0.994272 6.16647 1.17143 5.31461 1.5212C4.46275 1.87096 3.68881 2.38636 3.03766 3.03751C2.38651 3.68866 1.87111 4.4626 1.52135 5.31446C1.17159 6.16631 0.994424 7.07913 1.00013 7.99998C0.994424 8.92083 1.17159 9.83365 1.52135 10.6855C1.87111 11.5374 2.38651 12.3113 3.03766 12.9625C3.68881 13.6136 4.46275 14.129 5.31461 14.4788C6.16647 14.8285 7.07929 15.0057 8.00013 15C8.92098 15.0057 9.8338 14.8285 10.6857 14.4788C11.5375 14.129 12.3115 13.6136 12.9626 12.9625C13.6138 12.3113 14.1292 11.5374 14.4789 10.6855C14.8287 9.83365 15.0058 8.92083 15.0001 7.99998C15.0058 7.07913 14.8287 6.16631 14.4789 5.31446C14.1292 4.4626 13.6138 3.68866 12.9626 3.03751C12.3115 2.38636 11.5375 1.87096 10.6857 1.5212C9.8338 1.17143 8.92098 0.994272 8.00013 0.999981ZM10.7226 11.5L4.50013 5.27783L5.27798 4.49998L11.5001 10.7224L10.7226 11.5Z"
        fill={color}
      />
    </svg>
  );
};

ErrorFilled1.propTypes = {
  color: PropTypes.string,
};
