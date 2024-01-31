/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import { IconAlertCircle2 } from "../../icons/IconAlertCircle2";
import { IconMoreHorizontal } from "../../icons/IconMoreHorizontal";
import { Button } from "../Button";
import "./style.css";

export const NavigationPage = ({
  className,
  buttonIcon = <IconMoreHorizontal className="icon-instance-node-2" />,
  override = <IconAlertCircle2 className="icon-instance-node-2" />,
}) => {
  return (
    <div className={`navigation-page ${className}`}>
      <div className="frame-2">
        <div className="text-wrapper-4">Back to all experiments</div>
        <div className="text-wrapper-5">My awesome experiment 01</div>
      </div>
      <div className="frame-3">
        <Button
          className="button-instance"
          override={buttonIcon}
          size="large"
          stateProp="enabled"
          type="icon-only"
        />
        <Button
          className="button-instance"
          override={override}
          size="large"
          stateProp="enabled"
          type="icon-only"
        />
      </div>
    </div>
  );
};
