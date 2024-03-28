/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Add8 } from "../../icons/Add8";
import { Search } from "../../icons/Search";
import { Button } from "../Button";
import { SearchDefault } from "../SearchDefault";
import "./style.css";

import { NewExperimentModal } from "../NewExperimentModal";

export const DataTableToolbar = ({
  size,
  className,
  searchDefaultIcon = <Search className="add-2" color="#525252" />,
  buttonIcon = <Add8 className="add-2" color="#161616" />,
  visible = true,
  override = <Add8 className="add-2" color="#161616" />,
  buttonIconClassName,
  buttonButtonText = "Button",
}) => {
  return (
    <div className={`data-table-toolbar ${className}`}>
      <SearchDefault
        className="search-default-instance"
        expandable
        expanded={false}
        icon={searchDefaultIcon}
        size={size === "SM-XS" ? "small" : "large"}
        stateProp="enabled"
      />
      <Button
        className="button-instance-1"
        override={buttonIcon}
        size={size === "SM-XS" ? "small" : "large"}
        stateProp="disabled"
        style="secondary"
        type="icon-only"
        iconClassName={"IconTrash2"}

      />
      {visible && (
        <Button
          className="button-instance-1"
          override={<Add8 className="add-2" color="#161616" />}
          size={size === "SM-XS" ? "small" : "large"}
          stateProp="enabled"
          style="primary"
          type="icon-only"
        />
      )}

      <Button
        className="button-instance-2"
        override={override}
        size={size === "SM-XS" ? "small" : "large"}
        stateProp="enabled"
        style="secondary"
        type="icon-only"
        iconClassName={"IconSliders"}
      />
      {/* <Button
        buttonText={buttonButtonText}
        className="new-experiment-button"
        divClassName="button-2"
        icon={false}
        
        size={size === "SM-XS" ? "small" : "large"}
        stateProp="enabled"
        style="primary"
        type="text-icon"
      /> */}
      <NewExperimentModal blank={false} className="new-experiment-modal-instance" />
    </div>
  );
};

DataTableToolbar.propTypes = {
  size: PropTypes.oneOf(["XL-LG-MD", "SM-XS"]),
  visible: PropTypes.bool,
  buttonButtonText: PropTypes.string,
};
