/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Close97 } from "../../icons/Close97";
import { Resizer } from "../Resizer";
import { TagCloseButton } from "../TagCloseButton";
import "./style.css";

export const Tag = ({ filter = true, tagText = "Tag", size, color, state, className, labelClassName }) => {
  return (
    <div className={`tag ${state} ${color} ${size} ${className}`}>
      {["disabled", "enabled", "focus", "hover"].includes(state) && (
        <div className="tag-content">
          <div className="label">
            <div
              className={`text-wrapper ${
                color === "blue" ||
                color === "cool-gray" ||
                color === "cyan" ||
                color === "gray" ||
                color === "green" ||
                color === "high-contrast" ||
                color === "magenta" ||
                color === "purple" ||
                color === "red" ||
                color === "teal" ||
                color === "warm-gray"
                  ? labelClassName
                  : undefined
              }`}
            >
              {tagText}
            </div>
            {/* <Resizer className="resizer-instance" /> */}
          </div>
          {filter && (
            <TagCloseButton
              className="tag-close-button-instance"
              close97Color={
                color === "warm-gray" && state === "focus"
                  ? "#171414"
                  : state === "focus" && color === "red"
                  ? "#A2191F"
                  : (color === "cool-gray" && state === "focus") ||
                    (color === "gray" && state === "focus") ||
                    (color === "outline" && state === "enabled") ||
                    (color === "outline" && state === "focus") ||
                    (color === "outline" && state === "hover") ||
                    state === "disabled"
                  ? "#161616"
                  : color === "green" && state === "focus"
                  ? "#0E6027"
                  : state === "focus" && ["magenta", "purple"].includes(color)
                  ? "#9F1853"
                  : color === "cyan" && state === "focus"
                  ? "#00539A"
                  : undefined
              }
              color={
                color === "high-contrast" || (color === "teal" && size === "medium" && state === "disabled")
                  ? "high-contrast"
                  : color === "warm-gray"
                  ? "warm-gray"
                  : color === "red"
                  ? "red"
                  : color === "gray"
                  ? "gray"
                  : color === "green"
                  ? "green"
                  : color === "magenta"
                  ? "magenta"
                  : color === "purple"
                  ? "purple"
                  : color === "cyan"
                  ? "cyan"
                  : color === "cool-gray"
                  ? "cool-gray"
                  : color === "blue"
                  ? "blue"
                  : color === "outline"
                  ? "outline"
                  : "teal"
              }
              size={size === "small" ? "small" : "medium"}
              stateProp={
                state === "hover"
                  ? "hover"
                  : state === "focus"
                  ? "focus"
                  : state === "disabled"
                  ? "disabled"
                  : "enabled"
              }
            />
          )}
        </div>
      )}

      {state === "skeleton" && (
        <>
          <div className="text-line-margin">
            <div className="text-line" />
          </div>
          <>
            {filter && (
              <div className="icon-margin">
                <Close97 className="close" color="#161616" />
              </div>
            )}
          </>
        </>
      )}
    </div>
  );
};

Tag.propTypes = {
  filter: PropTypes.bool,
  tagText: PropTypes.string,
  size: PropTypes.oneOf(["medium", "small"]),
  color: PropTypes.oneOf([
    "teal",
    "gray",
    "cool-gray",
    "outline",
    "warm-gray",
    "blue",
    "high-contrast",
    "green",
    "magenta",
    "red",
    "purple",
    "cyan",
  ]),
  state: PropTypes.oneOf(["enabled", "focus", "hover", "skeleton", "disabled"]),
};
