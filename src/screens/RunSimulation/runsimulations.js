import React from "react";
import { NavigationHeader } from "./components/NavigationHeader";
import { NavigationPage } from "./components/NavigationPage";
import { IconAlertCircle2 } from "./icons/IconAlertCircle2";
import { IconEdit3 } from "./icons/IconEdit3";
import { IconGitMerge2 } from "./icons/IconGitMerge2";
import { IconGrid4 } from "./icons/IconGrid4";
import { IconHelpCircle } from "./icons/IconHelpCircle";
import { IconMessageSquare2 } from "./icons/IconMessageSquare2";
import { IconMoreHorizontal } from "./icons/IconMoreHorizontal";
import { IconSettings3 } from "./icons/IconSettings3";
import "./style.css";

export const RunSimulation = () => {
  return (
    <div className="element-create">
      <div className="div-2" data-breakpoints-mode="max-max-plus-1584px-1784px">
        <NavigationHeader className="navigation-header-instance" />
        <NavigationPage
          buttonIcon={<IconMoreHorizontal className="icon-instance-node-3" />}
          className="navigation-page-header"
          override={<IconAlertCircle2 className="icon-instance-node-3" />}
        />
        <div className="navigation-side-nav">
          <div className="frame-4">
            <div className="UI-shell-left-panel">
              <IconGrid4 className="icon-instance-node-3" />
            </div>
            <div className="frame-5">
              <div className="frame-5">
                <div className="UI-shell-left-panel">
                  <IconGitMerge2 className="icon-instance-node-3" />
                </div>
              </div>
            </div>
            <div className="spacer-wrapper">
              <div className="spacer" />
            </div>
            <div className="spacer-wrapper">
              <div className="spacer" />
            </div>
            <div className="spacer-wrapper">
              <div className="spacer" />
            </div>
            <div className="spacer-wrapper">
              <div className="spacer" />
            </div>
          </div>
          <div className="frame-4">
            <div className="UI-shell-left-panel">
              <IconHelpCircle className="icon-instance-node-3" />
            </div>
            <div className="UI-shell-left-panel">
              <IconMessageSquare2 className="icon-instance-node-3" />
            </div>
            <div className="UI-shell-left-panel">
              <IconSettings3 className="icon-instance-node-3" />
            </div>
          </div>
        </div>
        <div className="progress-indicator">
          <div className="progress-indicator-2">
            <div className="content">
              <div className="icon-label-wrapper">
                <div className="icon-label" />
              </div>
              <div className="min-width" />
            </div>
            <div className="min-height" />
          </div>
          <div className="progress-indicator-2">
            <div className="content">
              <div className="icon-label-wrapper">
                <div className="icon-label" />
              </div>
              <div className="min-width" />
            </div>
            <div className="min-height" />
          </div>
        </div>
        <div className="label-description">
          <div className="label">Review your workflow</div>
          <p className="description">
            Use natural language or HTP to describe what mutation you want to
            apply to the wild type. You can apply multiple mutants to the wild
            type.
          </p>
        </div>
        <div className="frame-6" />
        <div className="navigation-side-nav-2">
          <div className="frame-5">
            <div className="frame-5" />
          </div>
          <div className="frame-5">
            <div className="frame-5">
              <div className="UI-shell-left-panel-2" />
            </div>
          </div>
        </div>
        <div className="frame-7">
          <div className="frame-8">
            <div className="frame-9">
              <div className="text-wrapper-6">Workflow</div>
              <IconEdit3 className="icon-edit" color="#0F62FE" />
            </div>
            <div className="frame-10">
              <div className="tile" />
              <img className="line" alt="Line" src="/img/line-15.svg" />
              <div className="tile" />
              <img className="line" alt="Line" src="/img/line-16.svg" />
              <div className="tile-2" />
              <img className="line" alt="Line" src="/img/line-17.svg" />
              <div className="tile" />
            </div>
          </div>
          <div className="frame-8">
            <div className="frame-9">
              <div className="frame-11">
                <div className="text-wrapper-6">Target metrics</div>
                <p className="text-wrapper-7">
                  SIP, AI metrics, MMPB/GBSA binding, Trajectories, Stabilities
                </p>
              </div>
              <IconEdit3 className="icon-edit" color="#0F62FE" />
            </div>
          </div>
          <div className="frame-8">
            <div className="frame-9">
              <div className="frame-11">
                <div className="text-wrapper-8">Geometry constraint</div>
                <div className="text-wrapper-7">Whole enzyme</div>
              </div>
              <IconEdit3 className="icon-edit" color="#0F62FE" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
