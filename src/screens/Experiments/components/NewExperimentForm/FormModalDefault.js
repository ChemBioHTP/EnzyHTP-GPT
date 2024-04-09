import React from "react";
import { Close } from "./Close";
import { CreateForms } from "./CreateForms";
import { ModalFooterItem } from "./ModalFooterItem";
import "./style.css";

export const FormModalDefault = () => {
  return (
    <div className="form-modal-default">
      <header className="header">
        <div className="label-title">
          <div className="text-wrapper-3">New experiment</div>
        </div>
        <Close className="close-instance" />
      </header>
      <div className="content">
        <div className="slot">
          <CreateForms
            className="design-component-instance-node-2"
            sizeMediumStateWrapperDeprecatedTextBackgroundClassName="create-forms-instance"
            state="empty"
          />
        </div>
      </div>
      <ModalFooterItem
        actions="two"
        buttonButtonText="Cancel"
        buttonButtonText1="Create"
        buttonStateProp="disabled"
        cancel={false}
        className="design-component-instance-node-2"
      />
    </div>
  );
};
