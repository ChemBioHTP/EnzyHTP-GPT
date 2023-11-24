/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { SizeLarge } from "../../icons/SizeLarge";
import { TooltipCaretItem1 } from "../../icons/TooltipCaretItem1";
import { TooltipCaretItem15 } from "../../icons/TooltipCaretItem15";
import { TooltipCaretItem18 } from "../../icons/TooltipCaretItem18";
import { TooltipCaretItem19 } from "../../icons/TooltipCaretItem19";
import { TooltipCaretItem20 } from "../../icons/TooltipCaretItem20";
import { TooltipCaretItem4 } from "../../icons/TooltipCaretItem4";
import { TooltipCaretItem7 } from "../../icons/TooltipCaretItem7";
import { TooltipCaretItem8 } from "../../icons/TooltipCaretItem8";
import "./style.css";

export const TooltipItem = ({ tooltipText = "Tooltip text", type, position, alignment, className }) => {
  return (
    <div className={`tooltip-item ${type} position-${position} ${alignment} ${className}`}>
      {position === "bottom" && type === "icon" && <TooltipCaretItem4 className="tooltip-caret-item" />}

      {type === "icon" && ["bottom", "left", "top"].includes(position) && (
        <div className="body">
          <div className="tooltip-content">
            <div className="tooltip-text">{tooltipText}</div>
            <div className="background-4" />
          </div>
          <div className="min-width-3" />
        </div>
      )}

      {position === "left" && type === "icon" && <TooltipCaretItem7 className="tooltip-caret-item-2" />}

      {type === "icon" && position === "right" && (
        <>
          <TooltipCaretItem8 className="tooltip-caret-item" />
          <div className="body-2">
            <div className="tooltip-content">
              <div className="tooltip-text">{tooltipText}</div>
              <div className="background-4" />
            </div>
            <div className="min-width-3" />
          </div>
        </>
      )}

      {((position === "left" && type === "standard") ||
        (position === "top" && type === "standard") ||
        (position === "top" && type === "definition")) && (
        <div className="body-3">
          <div className="tooltip-text">{tooltipText}</div>
          <div className="background-5" />
        </div>
      )}

      {alignment === "center" && position === "top" && ["definition", "standard"].includes(type) && (
        <TooltipCaretItem15 className="tooltip-caret-item-2" />
      )}

      {((alignment === "end" && position === "top" && type === "definition") ||
        (alignment === "end" && position === "top" && type === "standard") ||
        (alignment === "start" && position === "top" && type === "definition") ||
        (alignment === "start" && position === "top" && type === "standard")) && (
        <SizeLarge className="tooltip-caret-item-2" />
      )}

      {position === "bottom" && ["definition", "standard"].includes(type) && (
        <>
          <TooltipCaretItem18 className="tooltip-caret-item" />
          <div className="body-4">
            <div className="tooltip-text">{tooltipText}</div>
            <div className="background-6" />
          </div>
        </>
      )}

      {type === "standard" && position === "right" && (
        <>
          <TooltipCaretItem19 className="tooltip-caret-item" />
          <div className="body-5">
            <div className="tooltip-text">{tooltipText}</div>
            <div className="background-7" />
          </div>
        </>
      )}

      {type === "standard" && position === "left" && <TooltipCaretItem20 className="tooltip-caret-item-2" />}

      {position === "top" && type === "icon" && <TooltipCaretItem1 className="tooltip-caret-item-2" />}
    </div>
  );
};

TooltipItem.propTypes = {
  tooltipText: PropTypes.string,
  type: PropTypes.oneOf(["definition", "icon", "standard"]),
  position: PropTypes.oneOf(["left", "right", "top", "bottom"]),
  alignment: PropTypes.oneOf(["end", "center", "start"]),
};
