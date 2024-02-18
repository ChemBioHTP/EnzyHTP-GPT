/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

export const Renew2 = ({ opacity = "unset", color = "#6929C4", className }) => {
  return (
    <svg
      className={`renew-2 ${className}`}
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
        d="M6 5.00002H3.39C4.03667 4.00618 4.9872 3.24794 6.09991 2.83831C7.21261 2.42868 8.4279 2.38961 9.56461 2.72691C10.7013 3.06422 11.6986 3.75984 12.4078 4.71008C13.117 5.66033 13.5001 6.81431 13.5 8.00002H14.5C14.5014 6.66277 14.0903 5.35763 13.3227 4.26257C12.5552 3.16752 11.4686 2.33585 10.2111 1.88096C8.95358 1.42607 7.58637 1.3701 6.29589 1.72069C5.00541 2.07128 3.85446 2.81136 3 3.84002V2.00002H2V6.00002H6V5.00002Z"
        fill={color}
      />
      <path
        className="path"
        d="M10 11H12.61C11.9633 11.9939 11.0128 12.7521 9.90009 13.1617C8.78739 13.5714 7.5721 13.6104 6.43538 13.2731C5.29866 12.9358 4.30139 12.2402 3.59221 11.29C2.88303 10.3397 2.49992 9.18573 2.5 8.00002H1.5C1.49862 9.33728 1.90973 10.6424 2.67726 11.7375C3.4448 12.8325 4.5314 13.6642 5.78891 14.1191C7.04642 14.574 8.41363 14.6299 9.70411 14.2794C10.9946 13.9288 12.1455 13.1887 13 12.16V14H14V10H10V11Z"
        fill={color}
      />
    </svg>
  );
};

Renew2.propTypes = {
  opacity: PropTypes.string,
  color: PropTypes.string,
};
