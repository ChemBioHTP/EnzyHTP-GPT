/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import { IconBell } from "../../icons/IconBell";
import { IconUser } from "../../icons/IconUser";
import "./style.css";

export const NavigationHeader = ({ className }) => {
  return (
    <div className={`navigation-header ${className}`}>
      <div className="frame">
        <div className="text-wrapper">EnzyHTP</div>
      </div>
      <div className="div">
        <IconBell className="icon-instance-node" color="white" />
        <IconUser className="icon-instance-node" color="white" />
      </div>
    </div>
  );
};
