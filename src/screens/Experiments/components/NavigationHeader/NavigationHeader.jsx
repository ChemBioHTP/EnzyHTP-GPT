/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import { IconBell } from "../../icons/IconBell";
import { IconUser1 } from "../../icons/IconUser1";
import "./style.css";

export const NavigationHeader = ({ className, onClick=()=>{} }) => {
  const handleClick = (id) => {
    onClick(id);
  }
  return (
    <div className={`navigation-header ${className}`}>
      <div className="frame">
        <div className="text-wrapper">EnzyHTP</div>
      </div>
      <div className="div">
        <div className="div-bell" onClick={()=>handleClick(0)}>
          <IconBell className="icon-instance-node" color="white" />
        </div>
        <div className="div-user" onClick={()=>handleClick(1)}>
          <IconUser1 className="icon-instance-node" color="white" />
        </div>
      </div>
    </div>
  );
};
