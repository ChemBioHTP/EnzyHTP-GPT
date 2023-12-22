import { React, useState } from "react";
import { Accordion } from "./components/Accordion";
import { Button } from "./components/Button";
import { DirectionHorizontalWrapper } from "./components/DirectionHorizontalWrapper";
import { ModalPanel } from "./components/ModalPanel";
import { ModalPanelTargets } from "./components/ModalPanelTargets";
import { NavigationHeader } from "./components/NavigationHeader";
import { NavigationPage } from "./components/NavigationPage";
import { NavigationSideNav } from "./components/NavigationSideNav";
import { TabsItems } from "./components/TabsItems";
import { CircleDash8 } from "./icons/CircleDash8";
import { IconAlertCircle } from "./icons/IconAlertCircle";
import { IconArrowRight1 } from "./icons/IconArrowRight1";
import { IconMoreHorizontal2 } from "./icons/IconMoreHorizontal2";
import { IconSend1 } from "./icons/IconSend1";
import { Incomplete3 } from "./icons/Incomplete3";
import "./style.css";
import { useNavigate } from "react-router-dom";

import { MolStarWrapper } from "./molstar";

export const ElementCreateTarget = () => {
  let navigate = useNavigate();
  const [inputValue, setInputValue] = useState("");
  const [mutationPattern, setMutationPattern] = useState("");
  const [errorMessage, setErrorMessage] = useState(null);
  const api_key = "TODO";

  const handleClick = async () => {
    // Make a POST request to the backend
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/generate_pattern",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ mut_request: inputValue, api_key: api_key }),
        }
      );

      // If we get a response, set our mutation pattern to it
      if (response.ok) {
        const responseData = await response.json();
        setMutationPattern(responseData.mutations);
        console.log(mutationPattern);
        setInputValue("");
      } else {
        setErrorMessage("API error");
      }
    } catch (error) {
      console.log(error);
    }
  };

  const routeChange = () => {
    try {
      navigate("/run_simulation");
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  return (
    <div className="element-create-target">
      <div className="div-2" data-breakpoints-mode="max-max-plus-1584px-1784px">
        <NavigationHeader className="navigation-header-instance" />
        <NavigationPage
          buttonIcon={<IconMoreHorizontal2 className="icon-instance-node-3" />}
          className="navigation-page-header"
          override={<IconAlertCircle className="icon-instance-node-3" />}
        />
        <div className="frame-11">
          <TabsItems
            alignment="auto-width"
            className="tabs-items-instance"
            labelText="Results"
            selected={false}
            size="medium"
            stateProp="enabled"
            type="text-icon"
          />
        </div>
        <div>
          <div className="text-area-content">
            <div className="text-2">
              <textarea
                className="text-2"
                rows={3}
                cols={100}
                maxLength={200}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type in anything"
                style={{
                  border: "none",
                  width: "100%",
                  height: "100%",
                  padding: "8px",
                  boxSizing: "border-box",
                  resize: "none",
                }}
              />
            </div>
            <div className="frame-12">
              <div className="text-3">{inputValue.length}/200</div>
              <div onClick={handleClick}>
                <Button
                  className="design-component-instance-node"
                  override={<IconSend1 className="icon-instance-node-3" />}
                  size="small"
                  stateProp="enabled"
                  type="icon-only"
                />
              </div>
            </div>
            <div className="text-2">
              {(errorMessage && <p>Error: {errorMessage}</p>) ||
                (mutationPattern && <p>Pattern: {mutationPattern}</p>)}
            </div>
          </div>
        </div>
        <div className="label-description">
          <div className="label-3">Generate mutants with AI</div>
          <p className="description">
            Use natural language or HTP to describe what mutation you want to
            apply to the wild type. You can apply multiple mutants to the wild
            type.
          </p>
        </div>
        <Accordion
          accordionItem={
            <ModalPanel className="design-component-instance-node-2" />
          }
          accordionItemExpanded
          accordionItemExpanded1
          accordionItemHasDiv={false}
          accordionItemSize="medium"
          accordionItemSize1="medium"
          accordionItemTitleText="Prompt templates"
          accordionItemTitleText1="Targets"
          accordionItemVisible={false}
          className="accordion-instance"
          override={
            <ModalPanelTargets className="modal-panel-targets-instance" />
          }
          visible={false}
          visible1={false}
        />
        <div className="progress-indicator-2">
          <DirectionHorizontalWrapper
            className="design-component-instance-node-2"
            direction="vertical"
            icon={
              <Incomplete3 className="icon-instance-node-3" color="#0F62FE" />
            }
            optionalLabel={false}
            progressIndicatorStepText="Target mutants"
            state="current"
          />
          <DirectionHorizontalWrapper
            className="design-component-instance-node-2"
            direction="vertical"
            icon={<CircleDash8 className="icon-instance-node-3" />}
            optionalLabel={false}
            progressIndicatorStepText="Workflow"
            state="incomplete"
          />
        </div>
        <div className="frame-13" onClick={routeChange}>
          <Button
            buttonText="Next"
            className="button-3"
            icon1={<IconArrowRight1 className="icon-instance-node-3" />}
            iconClassName="button-2"
            size="large"
            stateProp="disabled"
            type="text-icon"
          />
        </div>
        <NavigationSideNav
          UIShellLeftPanelLinkText="My awesome experime..."
          UIShellLeftPanelSelected={false}
          UIShellLeftPanelSelected1
          UIShellLeftPanelStateProp="enabled"
          UIShellLeftPanelStateProp1="selected"
          className="navigation-side-nav-2"
          version="version-5"
        />
        <div className="molstar-wrapper">
          <MolStarWrapper />
        </div>
      </div>
    </div>
  );
};
