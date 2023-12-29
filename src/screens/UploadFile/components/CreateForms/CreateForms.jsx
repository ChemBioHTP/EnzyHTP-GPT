/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { FileUploaderDrag } from "../FileUploaderDrag";
import "./style.css";

export const CreateForms = ({ state, className }) => {
  return (
    <div className={`create-forms ${className}`}>
      <div className="frame-9">
        <div className="label-text-wrapper">
          <div className="label-text-3">Upload wild type</div>
        </div>
        {state === "empty" && (
          <FileUploaderDrag
            className="instance-node-6"
            helperText="Drag and drop .pdb files here or click to upload"
            state="enabled"
          />
        )}
        </div>
      </div>
  );
};

CreateForms.propTypes = {
  state: PropTypes.oneOf(["success", "error", "empty"]),
};
