import React from "react";
import { NavigationHeader } from "./components/NavigationHeader";
import { NavigationPage } from "./components/NavigationPage";
import "./style.css";
import { NavigationSideNav } from "../CreateMutants/components/NavigationSideNav";
import { IconMoreHorizontal2 } from "../CreateMutants/icons/IconMoreHorizontal2";
import { IconAlertCircle } from "../CreateMutants/icons/IconAlertCircle";
import { Button } from "../CreateMutants/components/Button";
import { DirectionHorizontalWrapper } from "../CreateMutants/components/DirectionHorizontalWrapper";
import { CircleDash8 } from "../CreateMutants/icons/CircleDash8";
import { Incomplete3 } from "../CreateMutants/icons/Incomplete3";
import WorkflowDisplay from "./components/WorkflowDisplay/WorkflowDisplay";
import TargetMetrics from "./components/TargetMetrics/TargetMetrics";
import GeometryConstraint from "./components/GeometryConstraint/GeometryConstraint";

export const RunSimulation = () => {
  return (
    <div className="element-create-target">
      <div className="div-2" data-breakpoints-mode="max-max-plus-1584px-1784px">
        <NavigationHeader className="navigation-header-instance" />
        <NavigationPage
          buttonIcon={<IconMoreHorizontal2 className="icon-instance-node-3" />}
          className="navigation-page-header"
          override={<IconAlertCircle className="icon-instance-node-3" />}
        />
        <div>
          <div className="label-description">
            <div className="label-3">Review your workflow</div>
            <p className="description">
              Use natural language or HTP to describe what mutation you want to
              apply to the wild type. You can apply multiple mutants to the wild
              type.
            </p>
            <div className="WorkflowDisplay">
              <WorkflowDisplay />
            </div>
            <div className="TargetMetrics">
              <TargetMetrics />
            </div>
            <div className="GeometryConstraint">
              <GeometryConstraint />
            </div>
          </div>
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
          <div className="frame-13">
            <div style={{ cursor: "pointer" }}>
              <Button
                buttonText="Run experiment"
                className="button-3"
                icon1={""}
                iconClassName="button-2"
                stateProp="enabled"
                size="large"
                type="text-icon"
              />
            </div>
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
        </div>
      </div>
    </div>
  );
  // return (
  //   <div className="element-create">
  //     <div className="div-2" data-breakpoints-mode="max-max-plus-1584px-1784px">
  //       <NavigationHeader className="navigation-header-instance" />
  //       <NavigationPage
  //         buttonIcon={<IconMoreHorizontal className="icon-instance-node-3" />}
  //         className="navigation-page-header"
  //         override={<IconAlertCircle2 className="icon-instance-node-3" />}
  //       />
  //       <NavigationSideNav
  //         UIShellLeftPanelLinkText="My awesome experime..."
  //         UIShellLeftPanelSelected={false}
  //         UIShellLeftPanelSelected1
  //         UIShellLeftPanelStateProp="enabled"
  //         UIShellLeftPanelStateProp1="selected"
  //         className="navigation-side-nav-2"
  //         version="version-5"
  //       />
  //       <div className="progress-indicator">
  //         <div className="progress-indicator-2">
  //           <div className="content">
  //             <div className="icon-label-wrapper">
  //               <div className="icon-label" />
  //             </div>
  //             <div className="min-width" />
  //           </div>
  //           <div className="min-height" />
  //         </div>
  //         <div className="progress-indicator-2">
  //           <div className="content">
  //             <div className="icon-label-wrapper">
  //               <div className="icon-label" />
  //             </div>
  //             <div className="min-width" />
  //           </div>
  //           <div className="min-height" />
  //         </div>
  //       </div>
  //       <div className="label-description">
  //         <div className="label">Review your workflow</div>
  //         <p className="description">
  //           Use natural language or HTP to describe what mutation you want to
  //           apply to the wild type. You can apply multiple mutants to the wild
  //           type.
  //         </p>
  //       </div>
  //       <div className="frame-6" />
  //       <div className="frame-5">
  //         <div className="frame-5" />
  //       </div>
  //       <div className="frame-5">
  //         <div className="frame-5">
  //           <div className="UI-shell-left-panel-2" />
  //         </div>
  //       </div>
  //       <div className="frame-7">
  //         <div className="frame-8">
  //           <div className="frame-9">
  //             <div className="text-wrapper-6">Workflow</div>
  //             <IconEdit3 className="icon-edit" color="#0F62FE" />
  //           </div>
  //   <div className="frame-10">
  //   <div className="tile" />
  //   <img className="line" alt="Line" src="/img/line-15.svg" />
  //   <div className="tile" />
  //   <img className="line" alt="Line" src="/img/line-16.svg" />
  //   <div className="tile-2" />
  //   <img className="line" alt="Line" src="/img/line-17.svg" />
  //   <div className="tile" />
  // </div>
  //         </div>
  //         <div className="frame-8">
  //           <div className="frame-9">
  //             <div className="frame-11">
  //               <div className="text-wrapper-6">Target metrics</div>
  //               <p className="text-wrapper-7">
  //                 SIP, AI metrics, MMPB/GBSA binding, Trajectories, Stabilities
  //               </p>
  //             </div>
  //             <IconEdit3 className="icon-edit" color="#0F62FE" />
  //           </div>
  //         </div>
  //         <div className="frame-8">
  //           <div className="frame-9">
  //             <div className="frame-11">
  //               <div className="text-wrapper-8">Geometry constraint</div>
  //               <div className="text-wrapper-7">Whole enzyme</div>
  //             </div>
  //             <IconEdit3 className="icon-edit" color="#0F62FE" />
  //           </div>
  //         </div>
  //       </div>
  //     </div>
  //   </div>
  // );
};
