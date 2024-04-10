/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React, { useState } from "react";
import { AccordionItem } from "../AccordionItem";
import { AccordionToggle } from "../AccordionToggle";
import "./style.css";

export const Accordion = ({
  className,
  accordionItemSize = "large",
  accordionItemHasDiv,
  accordionItemTitleText = "Title of accordion",
  accordionItemExpanded = false,
  accordionItem1,
  accordionItem2,
  accordionItem3,
  accordionItemSize1 = "large",
  accordionItemVisible,
  accordionItemTitleText1 = "Title of accordion",
  accordionItemTitleText2 = "Title of accordion",
  accordionItemExpanded1 = false,
  visible = true,
  visible1 = true,
  onSwitchClick=()=>{},
}) => {
  const [toggleState, setToggleState] = useState(false);

  const handelSwitchClick = () => {
    setToggleState(toggleState => !toggleState);
    onSwitchClick(toggleState);
  }
  return (
    <div className={`accordion ${className}`}>
      <AccordionToggle 
        className="accordion-with-toggle"
        state={toggleState?"on":"off"} 
        onSwitchClick={handelSwitchClick}
      />
      <AccordionItem
        alignment="right"
        className="accordion-item-instance"
        expanded={accordionItemExpanded}
        flush={false}
        hasDiv={accordionItemHasDiv}
        override={accordionItem2}
        size={accordionItemSize}
        stateProp="enabled"
        titleText={accordionItemTitleText1}
      />
      {visible && (
        <AccordionItem
          alignment="right"
          className="accordion-item-instance"
          expanded={accordionItemExpanded1}
          flush={false}
          hasDiv={accordionItemVisible}
          override={accordionItem3}
          size={accordionItemSize1}
          stateProp="enabled"
          titleText={accordionItemTitleText2}
        />
      )}

      {visible1 && (
        <AccordionItem
          alignment="right"
          className="accordion-item-instance"
          expanded={false}
          flush={false}
          size="large"
          stateProp="enabled"
          titleText="Title of accordion"
        />
      )}
    </div>
  );
};

Accordion.propTypes = {
  accordionItemSize: PropTypes.string,
  accordionItemHasDiv: PropTypes.bool,
  accordionItemTitleText: PropTypes.string,
  accordionItemExpanded: PropTypes.bool,
  accordionItemSize1: PropTypes.string,
  accordionItemVisible: PropTypes.bool,
  accordionItemTitleText1: PropTypes.string,
  accordionItemExpanded1: PropTypes.bool,
  visible: PropTypes.bool,
  visible1: PropTypes.bool,
};
