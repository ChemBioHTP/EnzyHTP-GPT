import React from "react";
import { Accordion } from "../components/Accordion"
import { useState, useReducer, useEffect} from 'react';
import { Button } from "../components/Button";
import { DirectionHorizontalWrapper } from "../components/DirectionHorizontalWrapper";
import { DataTableHeader } from "../components/DataTableHeader"
import { DataTableRowCell } from "../components/DataTableRowCell"
import { GenerateStatusBar } from "../components/GenerateStatusBar"
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
import line3 from "../../../assets/images/Experiments/line-1.svg"
import { AccordionToggle } from "../components/AccordionToggle";
import { ExperimentOverview } from "../components/ExperimentOverview";
import { useNavigate } from "react-router-dom";

export const ElementCreateTarget = ({ sideVisible=true, titleText= "Example experiment 01", onClickWrapper = () => { }}) => {

  const handleSubmitButtonClick = () => {
    console.log(textInputValue);
  };

  const [textInputValue, setTextInputValue] = useState("");
  const [inputWithGUI, setInputWithGUI] = useState(false);

  useEffect(() => {
    if (sideVisible) {
      document.body.style.setProperty('--create-left-distance', '0px');
    } else {
      document.body.style.setProperty('--create-left-distance', '-214px');
    }

  }, [sideVisible]);

  let navigate = useNavigate();
  const cellData = [
    "NA22K EA24K KA162L RA163L", 
    "NA23K EA24K KA162L RA1A3L", 
    "NA24K EA26K KA152L RA163L",
    "NA25K EA25K KA162L RA173L",
    "NA26K EA27K KA162L RA183L"
  ];
  const handleInputGUISwitch = (state) => {
    setInputWithGUI(state);
    
  };

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

  const handleBackToList = () => {
    let path = '/exp'; 
    navigate(path);
  };
  return (
    <div className="element-create-target" data-theme-mode="white-theme">
      <NavigationPage
        buttonIcon={<IconMoreHorizontal className="icon-instance-node-3" />}
        className="navigation-page-header"
        override={<IconAlertCircle2 className="icon-instance-node-3" />}
        titleText={titleText}
        onClick={handleBackToList}
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
        onSwitchClick={handleInputGUISwitch}
        visible={false}
        visible1={false}
      />
      <img className="line-3" alt="Line" src={line3} />
      <div className="frame-14">
        <div className="label-6">Mutation generated</div>
        <div className="frame-15">
          <div className="data-table-row-item">
            <DataTableHeader
              cellText="Number"
              className="col"
              resizerResizerClassName="col-2"
              size="small"
              sortable={false}
              sorted="none"
              stateProp="enabled"
            />
            <DataTableHeader
              cellText="Pattern"
              className="data-table-header-cell-item"
              resizerResizerClassName="col-3"
              size="small"
              sortable={false}
              sorted="none"
              stateProp="enabled"
            />
          </div>
          {cellData.map((item, index) => (
            <div className="data-table-row-item-2" key={index}>
              <div className="data-table-row">
                <DataTableRowCell
                  cellText={(index+1).toString().padStart(2, '0')}
                  className="data-table-row-cell-item"
                  minHeightClassName="data-table-row-cell-instance"
                  resizerResizerClassName="col-2"
                  size="small"
                  state="enabled"
                />
                <DataTableRowCell
                  cellText={item}
                  className="data-table-row-cell-item-instance"
                  minHeightClassName="col-4"
                  resizerResizerClassName="col-3"
                  size="small"
                  state="enabled"
                />
              </div>
              <div className="divider-3" />
            </div>
          ))}

        </div>
        <AccordionToggle 
          text= "Show mutation in GUI"
          className="accordion-with-toggle"
          state="off"
        />
      </div>
      <GenerateStatusBar
        className="file-uploader-file-item"
        fileName="Your prompt has been successfully parsed."
        size="large"
        state="success"
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
          disabled={false}
          icon1={<IconArrowRight className="icon-instance-node-3" />}
          iconClassName="button-2"
          size="large"
          stateProp="enabled"
          style="primary"
          type="text-icon"
          onClick={()=>handleWrapperClick(1)}
        />
      </div>
      {/* <div className="frame-17">
        <div className="frame-18">
          <div className="text-wrapper-9">Experiment overview</div>
          <IconX1 className="icon-x" color="white" />
        </div>
        <ExperimentOverview
          className="design-component-instance-node-2"
          frameClassName="experiment-overview-instance"
          heading={false}
          stateProp="default"
          text="Description"
          text1="Click to give a description."
          type="text"
        />
        <ExperimentOverview
          className="design-component-instance-node-2"
          divClassName="experiment-overview-instance"
          heading
          stateProp="default"
          text="Status"
          text1="Please provide the prompt and run the experiment."
          type="text"
        />
      </div>      */}
    </div>
  );
};

export default ElementCreateTarget;