import React from "react";
import { Accordion } from "../components/Accordion"
import { useState, useReducer, useEffect} from 'react';
import { Button } from "../components/Button";
import { DirectionHorizontalWrapper } from "../components/DirectionHorizontalWrapper";
import { ModalPanel } from "../components/ModalPanel";
import { ModalPanelTargets } from "../components/ModalPanelTargets";
import { NavigationHeader } from "../components/NavigationHeader";
import { NavigationPage } from "../components/NavigationPage";
import { NavigationSideNav } from "../components/NavigationSideNav";
import { TabsItems } from "../components/TabsItems";
import { CircleDash1 } from "../icons/CircleDash1";
import { IconAlertCircle2 } from "../icons/IconAlertCircle2";
import { IconArrowRight } from "../icons/IconArrowRight";
import { IconMoreHorizontal } from "../icons/IconMoreHorizontal";
import { IconSend } from "../icons/IconSend";
import { Incomplete } from "../icons/Incomplete";
import "./style.css";
import { NavigationSideBar } from "../components/NavigationSideBar/NavigationSideBar";

export const ElementCreateTarget = () => {
  const [isVisible, setIsVisible] = useState(true);

  const [titleText, setTitleText] = useState("Example experiment 01");

  const [sideLabel, setSideLabel] = useState(["Example experiment 01", "Example experiment 02", "Example experiment 03", "Example experiment 04", "Example experiment 05"]);
  const handleButtonClick = (buttonId) => {
    if (buttonId === 0) {
      setIsVisible(!isVisible);
    }
    if (buttonId > 5) {
      setTitleText(sideLabel[buttonId - 6]);
    }
  };

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
  return (
    <div className="element-create-target" data-theme-mode="white-theme">
      <div className="div-2" data-breakpoints-mode="max-max-plus-1584px-1784px">
        <NavigationHeader className="navigation-header-instance" />
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
        <NavigationSideBar className="navigation-side-nav-instance" />
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
          accordionItem={<ModalPanel className="design-component-instance-node-2" />}
          accordionItemExpanded
          accordionItemExpanded1
          accordionItemHasDiv={false}
          accordionItemSize="medium"
          accordionItemSize1="medium"
          accordionItemTitleText="Prompt templates"
          accordionItemTitleText1="Targets"
          accordionItemVisible={false}
          className="accordion-instance"
          override={<ModalPanelTargets className="modal-panel-targets-instance" />}
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
          />
          <DirectionHorizontalWrapper
            className="design-component-instance-node-2"
            direction="vertical"
            icon={<CircleDash1 className="icon-instance-node-3" />}
            optionalLabel={false}
            progressIndicatorStepText="Workflow"
            state="incomplete"
          />
        </div>
        <div className="frame-13">
          <Button
            buttonText="Next"
            className="button-3"
            icon1={<IconArrowRight className="icon-instance-node-3" />}
            iconClassName="button-2"
            size="large"
            stateProp="disabled"
            style="primary"
            type="text-icon"
          />
        </div>
        {isVisible && <NavigationSideNav
          UIShellLeftPanelLinkText={sideLabel}
          UIShellLeftPanelSelected1={[true, false, false, false, false]}
          UIShellLeftPanelStateProp1={["selected", "enabled", "enabled", "enabled", "enabled"]}
          className="navigation-side-nav-2"
          version="version-5"
          onButtonClick={handleButtonClick}
        />}
      </div>
    </div>
  );
};

export default ElementCreateTarget;