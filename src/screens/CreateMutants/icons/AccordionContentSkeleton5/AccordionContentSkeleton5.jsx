/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";

export const AccordionContentSkeleton5 = ({ className }) => {
  return (
    <svg
      className={`accordion-content-skeleton-5 ${className}`}
      fill="none"
      height="96"
      viewBox="0 0 400 96"
      width="400"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect className="rect" fill="white" height="96" style={{mixBlendMode: 'multiply'}} width="400" />
      <path className="path" d="M400 8H32V18H400V8Z" fill="#E8E8E8" />
      <path className="path" d="M400 26H32V36H400V26Z" fill="#E8E8E8" />
      <path className="path" d="M400 44H32V54H400V44Z" fill="#E8E8E8" />
      <path className="path" d="M154.667 62H32V72H154.667V62Z" fill="#E8E8E8" />
      <path className="path" d="M277.333 62H154.667V72H277.333V62Z" fill="#E8E8E8" />
      <path className="path" d="M400 62H277.333V72H400V62Z" fill="white" style={{mixBlendMode: 'multiply'}} />
    </svg>
  );
};
