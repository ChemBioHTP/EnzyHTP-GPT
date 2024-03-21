import React from "react";
import { Accordion } from "../components/Accordion"
import { useState, useReducer, useEffect} from 'react';
import { Button } from "../components/Button";
import { DirectionHorizontalWrapper } from "../components/DirectionHorizontalWrapper";
import { ModalPanel } from "../components/ModalPanel";
import { ModalPanelTargets } from "../components/ModalPanelTargets";
import { NavigationPage } from "../components/NavigationPage";
import { TabsItems } from "../components/TabsItems";
import { CircleDash1 } from "../icons/CircleDash1";
import { IconAlertCircle2 } from "../icons/IconAlertCircle2";
import { IconArrowRight } from "../icons/IconArrowRight";
import { IconMoreHorizontal } from "../icons/IconMoreHorizontal";
import { IconSend } from "../icons/IconSend";
import { Incomplete } from "../icons/Incomplete";
import "./style.css";

export const ElementCreateTarget = ({ titleText= "Example experiment 01", onClickWrapper = () => { }}) => {

  const handleSubmitButtonClick = () => {
    console.log(textInputValue);
  };

  const [textInputValue, setTextInputValue] = useState("");

  const handleInputChange = (event) => {
    const value = event.target.value;
    if (event.target.value.length <= 200) {
      setTextInputValue(value);
    }
  };

  const handleTagClick = (tagItem) => {
    setTextInputValue(tagItem);
  };

  const handleWrapperClick = (id) => {
    onClickWrapper(id);
  };

  return (
    <div className="element-create-target" data-theme-mode="white-theme">
      <NavigationPage
        buttonIcon={<IconMoreHorizontal className="icon-instance-node-3" />}
        className="navigation-page-header"
        override={<IconAlertCircle2 className="icon-instance-node-3" />}
        titleText={titleText}
      />
      <div className="frame-11">
        <TabsItems
          alignment="auto-width"
          className="tabs-items-instance"
          labelText="Input"
          selected
          size="medium"
          stateProp="selected"
          style="line"
          type="text-icon"
        />
        <TabsItems
          alignment="auto-width"
          className="tabs-items-instance"
          labelText="Results"
          selected={false}
          size="medium"
          stateProp="enabled"
          style="line"
          type="text-icon"
        />
      </div>
      <div className="text-area-content">
        <textarea
          className="text-2"
          placeholder="Type in anything"
          value={textInputValue}
          onChange={handleInputChange}
        />
        <div className="frame-12">
          <div className="text-3">{textInputValue.length}/200</div>
          <Button
            className="design-component-instance-node"
            override={<IconSend className="icon-instance-node-3" />}
            size="small"
            stateProp="enabled"
            style="primary"
            type="icon-only"
            onClick={handleSubmitButtonClick}
          />
        </div>
      </div>
      <div className="label-description">
        <div className="label-3">Generate mutants with AI</div>
        <p className="description">
          Use natural language or HTP to describe what mutation you want to apply to the wild type. You can apply
          multiple mutants to the wild type.
        </p>
      </div>
      <Accordion
        accordionItem2={<ModalPanel className="design-component-instance-node-2" onClick={handleTagClick} />}
        accordionItem3={<ModalPanelTargets className="modal-panel-targets-instance" />}
        accordionItemExpanded
        accordionItemExpanded1
        accordionItemHasDiv={false}
        accordionItemSize="medium"
        accordionItemSize1="medium"
        accordionItemTitleText="Input with GUI"
        accordionItemTitleText1="Prompt templates"
        accordionItemVisible={false}
        className="accordion-instance"
        
        visible={false}
        visible1={false}
      />
      <div className="progress-indicator-2">
        <DirectionHorizontalWrapper
          className="design-component-instance-node-2"
          direction="vertical"
          icon={<Incomplete className="icon-instance-node-3" color="#0F62FE" />}
          optionalLabel={false}
          progressIndicatorStepText="Target mutants"
          state="current"
          onClick={()=>handleWrapperClick(0)}
        />
        <DirectionHorizontalWrapper
          className="design-component-instance-node-2"
          direction="vertical"
          icon={<CircleDash1 className="icon-instance-node-3" />}
          optionalLabel={false}
          progressIndicatorStepText="Workflow"
          state="incomplete"
          onClick={()=>handleWrapperClick(1)}
        />
      </div>
      <div className="frame-13">
        <Button
          buttonText="Next"
          className="button-3"
          disabled={true}
          icon1={<IconArrowRight className="icon-instance-node-3" />}
          iconClassName="button-2"
          size="large"
          stateProp="disabled"
          style="primary"
          type="text-icon"
        />
      </div>       
      </div>
  );
};

export default ElementCreateTarget;