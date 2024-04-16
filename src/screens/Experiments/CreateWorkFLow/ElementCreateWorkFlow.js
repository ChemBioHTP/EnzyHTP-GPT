import React, { useEffect, useState } from "react";
import { Button } from "../components/Button";
import { DirectionHorizontalWrapper } from "../components/DirectionHorizontalWrapper";
import { NavigationHeader } from "../components/NavigationHeader";
import { NavigationPage } from "../components/NavigationPage";
import { NavigationSideNav } from "../components/NavigationSideNav";
import { TabsItems } from "../components/TabsItems";
import { Tile } from "../components/Tile";
import { CheckmarkOutline } from "../icons/CheckmarkOutline";
import { IconAlertCircle2 } from "../icons/IconAlertCircle2";
import { IconArrowRight } from "../icons/IconArrowRight";
import { IconEdit3 } from "../icons/IconEdit3";
import { IconMoreHorizontal } from "../icons/IconMoreHorizontal";
import { Incomplete } from "../icons/Incomplete";
import line15 from "../../../assets/images/Experiments/ElementCreate/line-15.svg"
import "./style.css";
import { ModalPanelWorkflow } from "../components/ModalPanelWorkflow";
import navRock from "../../../assets/images/Experiments/navigate-rock-the-boat-1.png"
import ElementChangeWorkFLow from "../ChangeWorkFlow/ElementChangeWorkFlow";
import { useNavigate } from "react-router-dom";
import { ModalPanelMetrics } from "../components/ModalPanelMetrics/ModalPanelMetrics";
import { ModalPanelBond } from "../components/ModalPanelBond/ModalPanelBond";
import { ModalPanelMultiBonds } from "../components/ModalPanelMultiBonds/ModalPanelMultiBonds";
import { ModalPanelChoose } from "../components/ModalPanelChoose";

export const ElementCreateWorkFlow = ({ sideVisible = true,  titleText= "My awesome experiment", onClickWrapper = () => { }}) => {
  const handleWrapperClick = (id) => {
    onClickWrapper(id);
  };

  useEffect(() => {
    if (sideVisible) {
      document.body.style.setProperty('--flow-left-distance', '0px');
    } else {
      document.body.style.setProperty('--flow-left-distance', '-214px');
    }

  }, [sideVisible]);

  let navigate = useNavigate();

  const [changeFlow, setChangeFlow] = useState(false);
  const [changeTarget, setChangeTarget] = useState(false);
  const [changeBond, setChangeBond] = useState(false);
  const [changeBonds, setChangeBonds] = useState(false);
  const [chooseMd, setchooseMd] = useState(false);

  const handleChangeFlowClick = () => {
    
    setChangeFlow(changeFlow => !changeFlow);
  };

  const handleChangeTargetClick = () => {
    
    setChangeTarget(changeTarget => !changeTarget);
  };

  const handleChangeBondClick = () => {
    
    setChangeBond(changeBond => !changeBond);
  };

  const handleChangeBondsClick = (value) => {

    setChangeBonds(changeBonds => !changeBonds);
  };

  const handleChooseMdClick = () => {

    setchooseMd(chooseMd => !chooseMd);
  };

  const handleSaveMdOption = () => {
    navigate("/exp/result");
  };



  const handleBackToList = () => {
    let path = '/exp'; 
    navigate(path);
  };

  const [sideLabel, setSideLabel] = useState(["Example experiment 01", "Example experiment 02", "Example experiment 03", "Example experiment 04", "Example experiment 05"]);
  return (
    <div className="element-create">      
      <NavigationPage
        buttonIcon={<IconMoreHorizontal className="icon-instance-node-3" />}
        className="navigation-page-header"
        override={<IconAlertCircle2 className="icon-instance-node-3" />}
        onClick={handleBackToList}
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
      {changeFlow && (
        <>
          <div className="frame-cover" onClick={handleChangeFlowClick}></div>
          <div className="frame-side">
            <ElementChangeWorkFLow
              title="Change workflow"
              content="Choose a workflow to determine the processes to apply to the wild type."
              slotItem={<ModalPanelWorkflow
                backgroundClassName="modal-panel-workflow-2"
                className="modal-panel-workflow-instance"
                navigateRockThe={navRock}
              />}
              onCloseClick={handleChangeFlowClick}
            />
          </div>
        </>
      )}

      {changeTarget && (
        <>
          <div className="frame-cover"></div>
          <div className="frame-side">
            <ElementChangeWorkFLow
              title="Select target metrics"
              content="Choose the metrics you'd like to view following the experiment."
              slotItem={
                <ModalPanelMetrics
                  className="modal-panel-metrics-instance"
                  onClickEidt={(value)=>handleChangeBondsClick(value)}
                />
              }
              onCloseClick={handleChangeTargetClick}
            />
          </div>
        </>
      )}

      {changeBond && (
        <>
          <div className="frame-cover"></div>
          <div className="frame-side">
            <ElementChangeWorkFLow
              title="Adding inputs for EF"
              content="The metric you selected (EF) needs further details. Please provide the following inputs."
              slotItem={<ModalPanelBond/>}
              onCloseClick={handleChangeBondClick}
            />
          </div>
        </>
      )}

      {changeBonds && (
        <>
          <div className="frame-cover"></div>
          <div className="frame-side">
            <ElementChangeWorkFLow
              title="Adding inputs for EF"
              content="The metric you selected (EF) needs further details. Please provide the following inputs."
              slotItem={<ModalPanelMultiBonds/>}
              onCloseClick={handleChangeBondsClick}
            />
          </div>
        </>
      )}

      {chooseMd && (
        <>
          <div className="frame-cover"></div>
          <div className="frame-window">
            <ElementChangeWorkFLow
              title="Choose Your MD Simulation Option"
              content="Please select one of the options below based on your preference and resources:"
              slotItem={
                <ModalPanelChoose/>
              }
              onCloseClick={handleChooseMdClick}
              onSaveClick={handleSaveMdOption}
            />
          </div>
        </>
      )}
      <div className="progress-indicator-2">
        <DirectionHorizontalWrapper
          className="progress-indicator-item"
          direction="vertical"
          icon={<CheckmarkOutline className="icon-instance-node-3" color="#0F62FE" />}
          optionalLabel={false}
          progressIndicatorStepText="Target mutants"
          state="completed"

        />
        <DirectionHorizontalWrapper
          className="progress-indicator-item"
          direction="vertical"
          icon={<Incomplete className="icon-instance-node-3" color="#0F62FE" />}
          optionalLabel={false}
          progressIndicatorStepText="Workflow"
          state="current"

        />

        {/* <DirectionHorizontalWrapper
          className="progress-indicator-item"
          direction="vertical"
          icon={<Incomplete className="icon-instance-node-3" color="#0F62FE" />}
          optionalLabel={false}
          progressIndicatorStepText="MD simulation"
          state="current"

        /> */}

      </div>
      <div className="label-description">
        <div className="label">Review your workflow</div>
        <p className="p">
          Use natural language or HTP to describe what mutation you want to apply to the wild type. You can apply
          multiple mutants to the wild type.
        </p>
      </div>
      <div className="frame-12">
        <Button
          buttonText="Back"
          className="button-3"
          divClassName="design-component-instance-node"
          icon={false}
          size="large"
          stateProp="enabled"
          style="tertiary"
          type="text-icon"
          onClick={()=>handleWrapperClick(0)}
        />
        <Button
          buttonText="Run experiment"
          className="button-5"
          divClassName="button-6"
          icon1={<IconArrowRight className="icon-instance-node-3" />}
          iconClassName="button-4"
          size="large"
          stateProp="enabled"
          style="primary"
          type="text-icon"
          onClick={handleChooseMdClick}
        />
      </div>
      
      <div className="frame-13">
        <div className="frame-14">
          <div className="frame-15">
            <div className="text-wrapper-7">Workflow</div>
            <IconEdit3 className="icon-edit" color="#0F62FE" onClick={handleChangeFlowClick}/>
          </div>
          <div className="frame-16">
            <Tile
              accessible={false}
              className="tile-instance"
              descText="Remove water, loop fixing, protonate."
              divClassName="tile-2"
              divClassNameOverride="tile-3"
              stateProp="enabled"
              titleText="Structure preparation"
              type="base"
            />
            <img className="line-2" alt="Line" src={line15} />
            <Tile
              accessible={false}
              className="tile-instance"
              descText={
                <>
                  Coordinate manipulation,
                  <br />
                  mutation.
                </>
              }
              divClassName="tile-2"
              divClassNameOverride="tile-3"
              stateProp="enabled"
              titleText="Structure operation"
              type="base"
            />
            <img className="line-2" alt="Line" src={line15} />
            <Tile
              accessible={false}
              className="tile-4"
              descText="MD simulation"
              divClassName="tile-2"
              divClassNameOverride="tile-3"
              stateProp="enabled"
              titleText="Conformation exploration"
              type="base"
            />
            <img className="line-2" alt="Line" src={line15} />
            <Tile
              accessible={false}
              className="tile-instance"
              descText="QM/MM..."
              divClassName="tile-2"
              divClassNameOverride="tile-3"
              stateProp="enabled"
              titleText={
                <>
                  Energy <br />
                  calculation
                </>
              }
              type="base"
            />
          </div>
        </div>
        <div className="frame-14">
          <div className="frame-15">
            <div className="frame-17">
              <div className="text-wrapper-7">Target metrics</div>
              <p className="text-wrapper-8">SPI, AI metrics, MMPB/GBSA binding, Trajectories, Stabilities</p>
            </div>
            <IconEdit3 className="icon-edit" color="#0F62FE" onClick={handleChangeTargetClick} />
          </div>
        </div>
        <div className="frame-14">
          <div className="frame-15">
            <div className="frame-17">
              <div className="text-wrapper-9">Geometry constraint</div>
              <div className="text-wrapper-8">Whole enzyme</div>
            </div>
            <IconEdit3 className="icon-edit" color="#0F62FE" onClick={handleChangeBondClick} />
          </div>
        </div>
      </div>
      
    </div>
  );
};

export default ElementCreateWorkFlow;
