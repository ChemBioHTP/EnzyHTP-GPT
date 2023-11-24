/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const Incomplete3 = ({ opacity = "unset", color = "#0F62FE", className }) => {
  return (
    <svg
      className={`incomplete-3 ${className}`}
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
        d="M11.8821 3.42965L12.5246 2.6639C11.904 2.13853 11.1963 1.72553 10.4336 1.4435L10.0918 2.3823C10.745 2.62459 11.3508 2.97902 11.8821 3.42965Z"
        fill={color}
      />
      <path
        className="path"
        d="M13.905 7L14.8889 6.7936C14.7506 5.99468 14.4734 5.22616 14.07 4.52285L13.2044 5C13.5499 5.622 13.7868 6.29836 13.905 7Z"
        fill={color}
      />
      <path
        className="path"
        d="M10.0918 13.6177L10.4336 14.5565C11.1963 14.2745 11.904 13.8615 12.5246 13.3361L11.8821 12.5703C11.3508 13.021 10.745 13.3754 10.0918 13.6177Z"
        fill={color}
      />
      <path
        className="path"
        d="M13.2044 11L14.07 11.5C14.4737 10.7886 14.7508 10.0126 14.8891 9.2064L13.905 9.03295C13.7867 9.72415 13.5497 10.3897 13.2044 11Z"
        fill={color}
      />
      <path
        className="path"
        d="M8 15V1C6.14348 1 4.36301 1.7375 3.05025 3.05025C1.7375 4.36301 1 6.14348 1 8C1 9.85652 1.7375 11.637 3.05025 12.9497C4.36301 14.2625 6.14348 15 8 15Z"
        fill={color}
      />
    </svg>
  );
};

Incomplete3.propTypes = {
  opacity: PropTypes.string,
  color: PropTypes.string,
};
