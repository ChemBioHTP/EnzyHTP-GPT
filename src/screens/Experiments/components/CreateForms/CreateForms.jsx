/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { CheckmarkFilled3 } from "../../icons/CheckmarkFilled3";
import { Close } from "../../icons/Close";
import { FileUploaderDrag } from "../FileUploaderDrag";
import { FileUploaderFile } from "../FileUploaderFile";
import { SizeLargeStateWrapper } from "../SizeLargeStateWrapper";
import "./style.css";

export const CreateForms = ({
  state,
  className,
  fileUploaderFile = <CheckmarkFilled3 className="checkmark-filled" />,
  fileUploaderFileIcon = <Close className="close-instance" />,
}) => {
  return (
    <div className={`create-forms ${className}`}>
      <SizeLargeStateWrapper
        DEPRECATEDTextBackgroundClassName="DEPRECATED-text-input"
        DEPRECATEDTextInputText="My experiment 01"
        className="instance-node-2"
        filled={false}
        labelText="Name"
        showHelper={false}
        size="medium"
        state="enabled"
      />
      <div className="frame">
        <div className="label-text-wrapper">
          <div className="text-wrapper">Upload wild type</div>
        </div>
        {state === "empty" && (
          <FileUploaderDrag
            className="instance-node-2"
            helperText="Drag and drop .pdb files here or click to upload"
            state="enabled"
          />
        )}

        {["error", "success"].includes(state) && (
          <FileUploaderFile
            className={`${state === "error" ? "class-7" : "class-8"}`}
            divider="/img/divider-1.svg"
            errorShortClassName={`${state === "success" && "class-4"}`}
            fileName={state === "error" ? "Filename.png" : "Filename.pdb"}
            icon={fileUploaderFileIcon}
            longDesc={state === "error" ? "Please do something specific to fix it and upload again." : undefined}
            shortDesc={
              state === "error"
                ? "Wild type doesn’t pass the variety check."
                : "Wild type has been successfully uploaded and verified as accurate."
            }
            size="large"
            stateProp={state === "error" ? "error-long" : "error-short"}
            statusIconIcon={fileUploaderFile}
            statusIconState={state === "error" ? "warning-red" : "success-blue"}
            statusIconStateSuccessGreenClassName={`${state === "error" ? "class-5" : "class-6"}`}
          />
        )}
      </div>
    </div>
  );
};

CreateForms.propTypes = {
  state: PropTypes.oneOf(["success", "error", "empty"]),
};
