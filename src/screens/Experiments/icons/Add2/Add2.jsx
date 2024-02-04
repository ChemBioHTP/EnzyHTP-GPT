/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import {AddLarge} from '@carbon/icons-react';

export const Add2 = ({ opacity = "unset", color = "#161616", className }) => {
  return (
    // <svg
    //   className={`add-2 ${className}`}
    //   fill="none"
    //   height="20"
    //   viewBox="0 0 20 20"
    //   width="20"
    //   xmlns="http://www.w3.org/2000/svg"
    // >
    //   <rect
    //     className="rect"
    //     fill="white"
    //     fillOpacity={opacity}
    //     height="20"
    //     style={{ mixBlendMode: 'multiply'}}
    //     width="20"
    //   />
    //   <path
    //     className="path"
    //     d="M10.625 9.375V5H9.375V9.375H5V10.625H9.375V15H10.625V10.625H15V9.375H10.625Z"
    //     fill={color}
    //   />
    // </svg>
      // <svg 
      //     className={`add-2 ${className}`}
      //     width="16" 
      //     height="16" 
      //     viewBox="0 0 16 16" 
      //     fill="none" 
      //     xmlns="http://www.w3.org/2000/svg"
      // >
      //   <g id="Add">
      //     <rect 
      //       width="16" 
      //       height="16" 
      //       fill="white" 
      //       style={{ mixBlendMode: 'multiply'}}
      //       fillOpacity={opacity}
      //       />
      //     <path id="Vector" d="M8.5 7.5V4H7.5V7.5H4V8.5H7.5V12H8.5V8.5H12V7.5H8.5Z" fill={color}/>
      //   </g>
      // </svg>
      <AddLarge style={{backgroundColor: 'transparent'}} />
  );
};

Add2.propTypes = {
  opacity: PropTypes.string,
  color: PropTypes.string,
};
