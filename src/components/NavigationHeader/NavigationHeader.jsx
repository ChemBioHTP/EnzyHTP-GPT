import React from "react";
import { IconBell } from "../../icons/IconBell";
import { IconUser } from "../../icons/IconUser";
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
          <IconUser className="icon-instance-node" color="white" />
        </div>
      </div>
    </div>
  );
};
