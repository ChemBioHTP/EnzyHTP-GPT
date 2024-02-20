/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { AccordionItem } from "../AccordionItem";
import "./style.css";

export const Accordion = ({
  className,
  accordionItemSize = "large",
  accordionItemHasDiv,
  accordionItemTitleText = "Title of accordion",
  accordionItemExpanded = false,
  accordionItem,
  accordionItemSize1 = "large",
  accordionItemVisible,
  accordionItemTitleText1 = "Title of accordion",
  accordionItemExpanded1 = false,
  override,
  visible = true,
  visible1 = true,
}) => {
  return (
    <div className={`accordion ${className}`}>
      <AccordionItem
        alignment="right"
        className="accordion-item-instance"
        expanded={accordionItemExpanded}
        flush={false}
        hasDiv={accordionItemHasDiv}
        override={accordionItem}
        size={accordionItemSize}
        stateProp="enabled"
        titleText={accordionItemTitleText}
      />
      <AccordionItem
        alignment="right"
        className="accordion-item-instance"
        expanded={accordionItemExpanded1}
        flush={false}
        hasDiv={accordionItemVisible}
        override={override}
        size={accordionItemSize1}
        stateProp="enabled"
        titleText={accordionItemTitleText1}
      />
      {visible && (
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
