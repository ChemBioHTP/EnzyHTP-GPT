/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import {AddLarge} from '@carbon/icons-react';

export const Add2 = ({ opacity = "unset", color = "#161616", className }) => {
  return (
      <AddLarge opacity={opacity} style={{background: 'transparent', mixBlendMode: 'multiply'}} />
  );
};

Add2.propTypes = {
  opacity: PropTypes.string,
  color: PropTypes.string,
};
