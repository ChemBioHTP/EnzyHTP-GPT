import React from "react";
import { NavigationHeader } from "./components/NavigationHeader";
import { NavigationSideNav } from "./components/NavigationSideNav";
import { NewExperimentModal } from "./components/NewExperimentModal";
import chemistImage from "../../assets/images/Experiments/group-11.png";
import "./style.css";

export const ElementExperiments = () => {
  return (
    <div className="element-experiments">
      <div className="div-2" data-breakpoints-mode="max-max-plus-1584px-1784px">
        <NavigationHeader className="navigation-header-instance" />
        <NavigationSideNav className="navigation-side-nav-instance" version="version-4" />
        <div className="div-wrapper">
          <div className="text-wrapper-4">All experiments</div>
        </div>
        <div className="frame-9">
          <div className="text-wrapper-5">No experiments yet</div>
          <p className="p">Once you create experiments, they will show up here</p>
        </div>
        <NewExperimentModal className="new-experiment-modal-instance" />

        <img className="group" alt="Group" src={chemistImage} />
      </div>
    </div>
  );
};
