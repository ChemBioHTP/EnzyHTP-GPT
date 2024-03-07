import React, { useState } from "react";
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
import { NavigationSideBar } from "../components/NavigationSideBar/NavigationSideBar";

export const ElementCreateWorkFlow = () => {
  const [sideLabel, setSideLabel] = useState(["Example experiment 01", "Example experiment 02", "Example experiment 03", "Example experiment 04", "Example experiment 05"]);
  return (
    <div className="element-create">
      <div className="div-2" data-breakpoints-mode="max-max-plus-1584px-1784px">
        <NavigationHeader className="navigation-header-instance" />
        <NavigationPage
          buttonIcon={<IconMoreHorizontal className="icon-instance-node-3" />}
          className="navigation-page-header"
          override={<IconAlertCircle2 className="icon-instance-node-3" />}
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
        <NavigationSideBar className="navigation-side-nav-instance" version="version-4" />
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
          />
        </div>
        <NavigationSideNav
          UIShellLeftPanelLinkText={sideLabel}
          //UIShellLeftPanelSelected={false}
          UIShellLeftPanelSelected1={[true, false, false, false, false]}
          //UIShellLeftPanelStateProp="enabled"     
          UIShellLeftPanelStateProp1={["selected", "enabled", "enabled", "enabled", "enabled"]}
          className="navigation-side-nav-2"
          version="version-5"
        />
        <div className="frame-13">
          <div className="frame-14">
            <div className="frame-15">
              <div className="text-wrapper-7">Workflow</div>
              <IconEdit3 className="icon-edit" color="#0F62FE" />
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
                <p className="text-wrapper-8">SIP, AI metrics, MMPB/GBSA binding, Trajectories, Stabilities</p>
              </div>
              <IconEdit3 className="icon-edit" color="#0F62FE" />
            </div>
          </div>
          <div className="frame-14">
            <div className="frame-15">
              <div className="frame-17">
                <div className="text-wrapper-9">Geometry constraint</div>
                <div className="text-wrapper-8">Whole enzyme</div>
              </div>
              <IconEdit3 className="icon-edit" color="#0F62FE" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ElementCreateWorkFlow;
