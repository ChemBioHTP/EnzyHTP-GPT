/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Renew47 } from "../../icons/Renew47";
import "./style.css";

export const Slot = ({ iconOnly = true, size, className }) => {
  return (
    <div className={`slot size-3-${size} ${className}`}>
      <Renew47 className={`${size === "small" ? "class-6" : "class-7"}`} color="#6929C4" />
      {iconOnly && (
        <div className="text">
          {size === "default" && (
            <>
              <div className="text-wrapper-6">Slot component</div>
              <p className="text-wrapper-7">
                Optional placeholder component. Replace it with any component using the “Component Instance” swapper, or
                delete if not needed.
              </p>
            </>
          )}

          {size === "small" && <>Slot</>}
        </div>
      )}
    </div>
  );
};

Slot.propTypes = {
  iconOnly: PropTypes.bool,
  size: PropTypes.oneOf(["small", "default"]),
};
