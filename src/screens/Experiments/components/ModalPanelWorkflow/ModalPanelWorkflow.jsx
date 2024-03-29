/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { ChevronDown6 } from "../../icons/ChevronDown6";
import { Tag } from "../Tag";
import "./style.css";
import line11 from "../../../../assets/images/Experiments/line-11-1.svg"
export const ModalPanelWorkflow = ({
  className,
  backgroundClassName,
  navigateRockThe = "/img/navigate-rock-the-boat-1.png",
}) => {
  return (
    <div className={`modal-panel-workflow ${className}`}>
      <div className="div">
        <div className="select-default">
          <div className="label-margin">
            <div className="select-label">Workflow</div>
          </div>
          <div className="select-menu-default">
            <div className="select-items">
              <div className="text-overflow">
                <div className="option">Predefined</div>
              </div>
              <div className="chevron-error">
                <ChevronDown6 className="chevron-down" />
              </div>
              <div className={`background ${backgroundClassName}`} />
            </div>
          </div>
        </div>
        <div className="frame-2">
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="Remove water"
          />
          <img className="line" alt="Line" src={line11} />
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="Loop fixing"
          />
          <img className="line" alt="Line" src={line11} />
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="Protonate"
          />
          <img className="line" alt="Line" src={line11} />
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="Mutate"
          />
          <img className="line" alt="Line" src={line11} />
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="Parameterization"
          />
          <img className="line" alt="Line" src={line11} />
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="MD simulation"
          />
          <img className="line" alt="Line" src={line11} />
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="Calculate metrics"
          />
          <img className="line" alt="Line" src={line11} />
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="Stability"
          />
          <img className="line" alt="Line" src={line11} />
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="Stability"
          />
          <img className="line" alt="Line" src={line11} />
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="Stability"
          />
          <img className="line" alt="Line" src={line11} />
          <Tag
            className="tag-instance"
            color="blue"
            filter={false}
            labelClassName="tag-2"
            size="small"
            state="enabled"
            tagText="Stability"
          />
        </div>
      </div>
      <div className="frame-3">
        <img className="navigate-rock-the" alt="Navigate rock the" src={navigateRockThe} />
        <p className="p">
          In the beta, only predefined workflows are offered. Custom workflows are coming in our next update. Stay
          tuned!
        </p>
      </div>
    </div>
  );
};

ModalPanelWorkflow.propTypes = {
  navigateRockThe: PropTypes.string,
};
