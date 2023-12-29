/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Checkbox23 } from "../../icons/Checkbox23";
import { Checkbox24 } from "../../icons/Checkbox24";
import { Checkbox3 } from "../../icons/Checkbox3";
import { CheckboxCheckedFilled } from "../../icons/CheckboxCheckedFilled";
import { CheckboxCheckedFilled14 } from "../../icons/CheckboxCheckedFilled14";
import { CheckboxCheckedFilled17 } from "../../icons/CheckboxCheckedFilled17";
import { CheckboxIndeterminateFilled } from "../../icons/CheckboxIndeterminateFilled";
import { Chevron4 } from "../../icons/Chevron4";
import { Chevron9 } from "../../icons/Chevron9";
import { ChevronDown3 } from "../../icons/ChevronDown3";
import { ChevronUp17 } from "../../icons/ChevronUp17";
import { RadioButton } from "../../icons/RadioButton";
import { RadioButton2 } from "../../icons/RadioButton2";
import { RadioButtonChecked2 } from "../../icons/RadioButtonChecked2";
import { RadioButtonChecked5 } from "../../icons/RadioButtonChecked5";
import { Checkbox } from "../Checkbox";
import { DataTableBodyRow } from "../DataTableBodyRow";
import { DataTableHeader } from "../DataTableHeader";
import { DataTableRowCell } from "../DataTableRowCell";
import "./style.css";

export const DataTableRowItem = ({
  topBorder = true,
  zebraStyle = false,
  type,
  size,
  state,
  selectable,
  selectType,
  selection,
  expandable,
  expanded,
  sortable,
  className,
  dataTableRowCellMinHeightClassName,
  dataTableRowCellCellText = "Content",
  dataTableRowCellMinHeightClassNameOverride,
  dataTableRowCellCellText1 = "Content",
  dataTableRowCellImgClassName,
  dataTableRowCellCellText2 = "Content",
  dataTableRowCellImgClassNameOverride,
  dataTableRowCellCellText3 = "Content",
  dataTableRowCellMinHeightClassName1,
  dataTableRowCellCellText4 = "Content",
  dataTableRowCellMinHeightClassName2,
  dataTableRowCellCellText5 = "Content",
  dataTableRowCellMinHeightClassName3,
  dataTableRowCellCellText6 = "Content",
  visible = true,
  dividerClassName,
  dataTableHeaderCellText = "Header",
  dataTableHeaderCellText1 = "Header",
  dataTableHeaderCellText2 = "Header",
  dataTableHeaderCellText3 = "Header",
  dataTableHeaderCellText4 = "Header",
  dataTableHeaderCellText5 = "Header",
  dataTableHeaderCellText6 = "Header",
  visible1 = true,
}) => {
  return (
    <div
      className={`data-table-row-item ${type} state-3-${state} selectable-${selectable} selection-${selection} expandable-0-${expandable} size-11-${size} expanded-1-${expanded} ${className}`}
    >
      {((!expandable && selectType === "checkbox" && type === "header") ||
        (expandable && selectType === "none" && type === "header") ||
        (selectType === "radio-button" && type === "header")) && (
        <div className={`data-table-select select-type-${selectType} selectable-0-${selectable} size-12-${size}`}>
          {selection === "unchecked" && <Checkbox3 className="instance-node-2" color="#161616" />}

          {["none", "radio-button"].includes(selectType) && <Checkbox />}

          {selection === "checked" && <CheckboxCheckedFilled className="instance-node-2" />}

          {selection === "indeterminate" && <CheckboxIndeterminateFilled className="instance-node-2" />}
        </div>
      )}

      {type === "header" && (!expandable || selectType === "none") && (
        <DataTableHeader
          cellText={
            expandable || selectable ? "Header" : !expandable && !selectable ? dataTableHeaderCellText : undefined
          }
          className="data-table-header-cell-item"
          resizerResizerClassName={`${selectType === "checkbox" && "class-2"} ${
            (expandable || selectType === "radio-button") && "col"
          } ${!expandable && !selectable && "col-2"}`}
          size={
            size === "extra-large"
              ? "extra-large"
              : size === "large"
              ? "large"
              : size === "medium"
              ? "medium"
              : size === "small"
              ? "small"
              : size === "extra-small"
              ? "extra-small"
              : undefined
          }
          sortable={!sortable ? false : sortable ? true : undefined}
          sorted="none"
          stateProp="enabled"
        />
      )}

      {type === "header" && (!expandable || selectType === "none") && (
        <>
          <DataTableHeader
            cellText={
              !expandable && !selectable ? dataTableHeaderCellText1 : expandable || selectable ? "Header" : undefined
            }
            className="data-table-header-cell-item"
            resizerResizerClassName={`${!expandable && !selectable && "col-2"} ${
              selectType === "checkbox" && "class-2"
            } ${(expandable || selectType === "radio-button") && "col"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={!sortable ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText={
              !expandable && !selectable ? dataTableHeaderCellText2 : expandable || selectable ? "Header" : undefined
            }
            className="data-table-header-cell-item"
            resizerResizerClassName={`${!expandable && !selectable && "col-2"} ${
              selectType === "checkbox" && "class-2"
            } ${(expandable || selectType === "radio-button") && "col"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={!sortable ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText={
              !expandable && !selectable ? dataTableHeaderCellText3 : expandable || selectable ? "Header" : undefined
            }
            className="data-table-header-cell-item"
            resizerResizerClassName={`${!expandable && !selectable && "col-2"} ${
              selectType === "checkbox" && "class-2"
            } ${(expandable || selectType === "radio-button") && "col"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={!sortable ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText={
              !expandable && !selectable ? dataTableHeaderCellText4 : expandable || selectable ? "Header" : undefined
            }
            className="data-table-header-cell-item"
            resizerResizerClassName={`${!expandable && !selectable && "col-2"} ${
              selectType === "checkbox" && "class-2"
            } ${(expandable || selectType === "radio-button") && "col"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={!sortable ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
        </>
      )}

      {type === "header" && (!expandable || selectType === "none") && (
        <>
          <DataTableHeader
            cellText={
              expandable || selectable ? "Header" : !expandable && !selectable ? dataTableHeaderCellText5 : undefined
            }
            className="data-table-header-cell-item"
            resizerResizerClassName={`${selectType === "checkbox" && "class-2"} ${
              (expandable || selectType === "radio-button") && "col"
            } ${!expandable && !selectable && "col-2"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={!sortable ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText={
              expandable || selectable ? "Header" : !expandable && !selectable ? dataTableHeaderCellText6 : undefined
            }
            className="data-table-header-cell-item"
            resizerResizerClassName={`${selectType === "checkbox" && "class-2"} ${
              (expandable || selectType === "radio-button") && "col"
            } ${!expandable && !selectable && "col-2"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={!sortable ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
        </>
      )}

      {((!expandable && selectType === "checkbox" && type === "header") ||
        (expandable && selectType === "none" && type === "header") ||
        (selectType === "radio-button" && type === "header")) && (
        <DataTableHeader
          cellText="Header"
          className="data-table-header-cell-item"
          resizerResizerClassName={`${selectType === "checkbox" && "class-2"} ${
            ["none", "radio-button"].includes(selectType) && "col"
          }`}
          size={
            size === "extra-large"
              ? "extra-large"
              : size === "large"
              ? "large"
              : size === "medium"
              ? "medium"
              : size === "small"
              ? "small"
              : size === "extra-small"
              ? "extra-small"
              : undefined
          }
          sortable={!sortable ? false : sortable ? true : undefined}
          sorted="none"
          stateProp="enabled"
        />
      )}

      {type === "header" && expandable && selectType === "checkbox" && (
        <>
          <div className="data-table-expand">
            <Chevron9 className="instance-node-3" color="#161616" />
          </div>
          <div className="data-table-select-2">
            {selection === "unchecked" && <Checkbox3 className="instance-node-2" color="#161616" />}

            {selection === "checked" && <CheckboxCheckedFilled className="instance-node-2" />}

            {selection === "indeterminate" && <CheckboxIndeterminateFilled className="instance-node-2" />}
          </div>
          <DataTableHeader
            cellText="Header"
            className="data-table-header-cell-item"
            resizerResizerClassName="data-table-header-instance"
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={size === "extra-large" ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText="Header"
            className="data-table-header-cell-item"
            resizerResizerClassName="data-table-header-instance"
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={size === "extra-large" ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText="Header"
            className="data-table-header-cell-item"
            resizerResizerClassName="data-table-header-instance"
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={size === "extra-large" ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText="Header"
            className="data-table-header-cell-item"
            resizerResizerClassName="data-table-header-instance"
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={size === "extra-large" ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText="Header"
            className="data-table-header-cell-item"
            resizerResizerClassName="data-table-header-instance"
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={size === "extra-large" ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText="Header"
            className="data-table-header-cell-item"
            resizerResizerClassName="data-table-header-instance"
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={size === "extra-large" ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText="Header"
            className="data-table-header-cell-item"
            resizerResizerClassName="data-table-header-instance"
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={size === "extra-large" ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
          <DataTableHeader
            cellText="Header"
            className="data-table-header-cell-item"
            resizerResizerClassName="data-table-header-instance"
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            sortable={size === "extra-large" ? false : sortable ? true : undefined}
            sorted="none"
            stateProp="enabled"
          />
        </>
      )}

      {((!expandable && selection === "unchecked" && size === "extra-small" && state === "hover") ||
        (!expandable && selection === "unchecked" && size === "large" && state === "hover") ||
        (!expandable && selection === "unchecked" && size === "medium" && state === "hover") ||
        (!expandable && selection === "unchecked" && size === "small" && state === "hover") ||
        (expandable && selection === "unchecked" && state === "hover") ||
        (selection === "checked" && state === "hover") ||
        (selection === "none" && state === "hover") ||
        (selection === "selected" && state === "hover") ||
        (selection === "unselected" && state === "hover") ||
        (state === "enabled" && type === "body")) && (
        <div className="data-table-row">
          {((expandable && !selectable) || (selectable && !expandable)) && (
            <div
              className={`data-table-expand-2 select-type-0-${selectType} size-15-${size} expandable-1-${expandable}`}
            >
              {expanded && ["extra-large", "large", "small"].includes(size) && (
                <Chevron4 className="instance-node-3" color="#161616" />
              )}

              {expanded && ["extra-small", "medium"].includes(size) && <ChevronUp17 className="instance-node-3" />}

              {((selection === "unchecked" && size === "extra-large") ||
                (selection === "unchecked" && size === "extra-small") ||
                (selection === "unchecked" && size === "large") ||
                (selection === "unchecked" && size === "small")) && (
                <Checkbox3 className="instance-node-4" color="#161616" />
              )}

              {((selection === "unselected" && size === "extra-large") ||
                (selection === "unselected" && size === "large") ||
                (selection === "unselected" && size === "medium" && state === "enabled") ||
                (selection === "unselected" && size === "small")) && <RadioButton2 className="instance-node-3" />}

              {((selection === "checked" && size === "extra-large") ||
                (selection === "checked" && size === "extra-small") ||
                (selection === "checked" && size === "large") ||
                (selection === "checked" && size === "small")) && <CheckboxCheckedFilled className="instance-node-4" />}

              {selection === "selected" && ["extra-large", "large", "small"].includes(size) && (
                <RadioButtonChecked2 className="instance-node-3" />
              )}

              {((expandable && !expanded && size === "extra-large") ||
                (expandable && !expanded && size === "large") ||
                (expandable && !expanded && size === "medium" && state === "enabled") ||
                (expandable && !expanded && size === "small")) && (
                <Chevron9 className="instance-node-3" color="#161616" />
              )}

              {selection === "unchecked" && size === "medium" && state === "enabled" && (
                <Checkbox24 className="instance-node-4" />
              )}

              {selection === "unchecked" && state === "hover" && size === "medium" && (
                <Checkbox23 className="instance-node-4" />
              )}

              {selection === "unselected" &&
                ["extra-small", "medium"].includes(size) &&
                (size === "extra-small" || state === "hover") && <RadioButton className="instance-node-3" />}

              {selection === "checked" && size === "medium" && state === "enabled" && (
                <CheckboxCheckedFilled17 className="instance-node-4" />
              )}

              {selection === "selected" && ["extra-small", "medium"].includes(size) && (
                <RadioButtonChecked5 className="instance-node-3" />
              )}

              {selection === "checked" && state === "hover" && size === "medium" && (
                <CheckboxCheckedFilled14 className="instance-node-4" />
              )}

              {((expandable && !expanded && size === "extra-small") ||
                (expandable && !expanded && size === "medium" && state === "hover")) && (
                <ChevronDown3 className="instance-node-3" />
              )}
            </div>
          )}

          {expandable && selectable && (
            <>
              <div className="data-table-expand-3">
                {((expanded && selection === "checked" && size === "large" && state === "hover") ||
                  (expanded && selection === "checked" && size === "medium" && state === "hover") ||
                  (expanded && selection === "checked" && state === "enabled") ||
                  (expanded && selection === "unchecked" && size === "extra-large" && state === "enabled") ||
                  (expanded && selection === "unchecked" && size === "extra-small" && state === "enabled") ||
                  (expanded && selection === "unchecked" && size === "large") ||
                  (expanded && selection === "unchecked" && size === "medium" && state === "enabled") ||
                  (expanded && selection === "unchecked" && size === "small" && state === "hover") ||
                  (expanded && size === "extra-large" && state === "hover") ||
                  (expanded && size === "extra-small" && state === "hover") ||
                  (expanded && size === "small" && state === "enabled") ||
                  (selection === "none" && state === "hover")) && (
                  <Chevron4 className="instance-node-3" color="#161616" />
                )}

                {state === "hover" && expanded && selection === "unchecked" && size === "medium" && (
                  <ChevronUp17 className="instance-node-3" />
                )}

                {((!expanded && size === "extra-large" && state === "hover") ||
                  (!expanded && size === "extra-small" && state === "hover") ||
                  (!expanded && size === "large" && state === "hover") ||
                  (!expanded && size === "small" && state === "hover") ||
                  (!expanded && state === "enabled")) && <Chevron9 className="instance-node-3" color="#161616" />}

                {!expanded && state === "hover" && size === "medium" && <ChevronDown3 className="instance-node-3" />}
              </div>
              <div className="data-table-select-3">
                {((selection === "unchecked" && size === "extra-large" && state === "hover") ||
                  (selection === "unchecked" && size === "extra-small" && state === "hover") ||
                  (selection === "unchecked" && size === "large" && state === "hover") ||
                  (selection === "unchecked" && size === "small" && state === "hover") ||
                  (selection === "unchecked" && state === "enabled")) && (
                  <Checkbox3 className="instance-node-2" color="#161616" />
                )}

                {((expanded && selection === "checked" && size === "medium" && state === "hover") ||
                  (selection === "checked" && size === "extra-large" && state === "hover") ||
                  (selection === "checked" && size === "extra-small" && state === "hover") ||
                  (selection === "checked" && size === "large" && state === "hover") ||
                  (selection === "checked" && size === "small" && state === "hover") ||
                  (selection === "checked" && state === "enabled") ||
                  selection === "none") && <CheckboxCheckedFilled className="instance-node-2" />}

                {selection === "unchecked" && state === "hover" && size === "medium" && (
                  <Checkbox24 className="instance-node-2" />
                )}

                {state === "hover" && !expanded && size === "medium" && selection === "checked" && (
                  <CheckboxCheckedFilled14 className="instance-node-2" />
                )}
              </div>
            </>
          )}

          <DataTableRowCell
            cellText={
              expandable || selectable ? "Content" : !expandable && !selectable ? dataTableRowCellCellText : undefined
            }
            className={`${
              ((!expandable && !selectable && size === "medium") ||
                size === "extra-large" ||
                size === "extra-small" ||
                size === "large" ||
                size === "small") &&
              "data-table-row-cell-item"
            } ${size === "medium" && (expandable || selectable) && "class-3"}`}
            minHeightClassName={`${
              state === "enabled" && expanded && !selectable && size === "extra-large" && "class-4"
            } ${state === "hover" && expanded && !selectable && size === "extra-large" && "class-5"} ${
              state === "enabled" && expanded && !selectable && size === "large" && "class-6"
            } ${state === "hover" && expanded && !selectable && size === "large" && "class-7"} ${
              !selectable && expanded && size === "medium" && state === "enabled" && "class-8"
            } ${state === "hover" && !selectable && expanded && size === "medium" && "class-9"} ${
              expanded && size === "small" && !selectable && state === "enabled" && "class-10"
            } ${state === "hover" && expanded && size === "small" && !selectable && "class-11"} ${
              size === "extra-small" && expanded && !selectable && state === "enabled" && "class-12"
            } ${state === "hover" && size === "extra-small" && expanded && !selectable && "class-13"} ${
              !expandable && selection === "unchecked" && size === "extra-large" && "class-14"
            } ${size === "extra-large" && selection === "unselected" && state === "enabled" && "class-15"} ${
              selection === "unselected" && state === "hover" && size === "extra-large" && "class-16"
            } ${
              state === "enabled" && !expandable && selection === "checked" && size === "extra-large" && "class-17"
            } ${size === "extra-large" && selection === "selected" && state === "enabled" && "class-18"} ${
              state === "hover" && !expandable && selectType === "checkbox" && size === "extra-large" && "class-19"
            } ${selection === "selected" && state === "hover" && size === "extra-large" && "class-20"} ${
              !expanded && expandable && !selectable && size === "extra-large" && state === "enabled" && "class-21"
            } ${!expanded && expandable && !selectable && size === "extra-large" && state === "hover" && "class-22"} ${
              state === "enabled" && !expandable && selection === "unchecked" && size === "large" && "class-23"
            } ${!expandable && selection === "unchecked" && state === "hover" && size === "large" && "class-24"} ${
              state === "enabled" && !expandable && selection === "checked" && size === "large" && "class-25"
            } ${state === "hover" && !expandable && selection === "checked" && size === "large" && "class-26"} ${
              size === "large" && selection === "unselected" && state === "enabled" && "class-27"
            } ${selection === "unselected" && state === "hover" && size === "large" && "class-28"} ${
              size === "large" && selection === "selected" && state === "enabled" && "class-29"
            } ${selection === "selected" && state === "hover" && size === "large" && "class-30"} ${
              !expanded && expandable && !selectable && size === "large" && state === "enabled" && "class-31"
            } ${!expanded && expandable && !selectable && size === "large" && state === "hover" && "class-32"} ${
              !expandable && selection === "unchecked" && size === "medium" && state === "enabled" && "class-33"
            } ${selection === "unselected" && size === "medium" && state === "enabled" && "class-34"} ${
              state === "hover" && !expandable && selection === "unchecked" && size === "medium" && "class-35"
            } ${selection === "unselected" && state === "hover" && size === "medium" && "class-36"} ${
              state === "enabled" && !expandable && size === "medium" && selection === "checked" && "class-37"
            } ${selection === "selected" && size === "medium" && state === "enabled" && "class-38"} ${
              state === "hover" && !expandable && size === "medium" && selection === "checked" && "class-39"
            } ${selection === "selected" && state === "hover" && size === "medium" && "class-40"} ${
              !expanded && size === "medium" && expandable && !selectable && state === "enabled" && "class-41"
            } ${!expanded && size === "medium" && expandable && !selectable && state === "hover" && "class-42"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "enabled" && "class-43"
            } ${size === "small" && selection === "unselected" && state === "enabled" && "class-44"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "hover" && "class-45"
            } ${size === "small" && selection === "unselected" && state === "hover" && "class-46"} ${
              !expandable && size === "small" && selection === "checked" && state === "enabled" && "class-47"
            } ${size === "small" && selection === "selected" && state === "enabled" && "class-48"} ${
              state === "hover" && !expandable && size === "small" && selection === "checked" && "class-49"
            } ${size === "small" && selection === "selected" && state === "hover" && "class-50"} ${
              !expanded && expandable && !selectable && size === "small" && state === "enabled" && "class-51"
            } ${!expanded && expandable && !selectable && size === "small" && state === "hover" && "class-52"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "enabled" && "class-53"
            } ${size === "extra-small" && selection === "unselected" && state === "enabled" && "class-54"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "hover" && "class-55"
            } ${size === "extra-small" && selection === "unselected" && state === "hover" && "class-56"} ${
              size === "extra-small" && !expandable && selection === "checked" && state === "enabled" && "class-57"
            } ${size === "extra-small" && selection === "selected" && state === "enabled" && "class-58"} ${
              state === "hover" && size === "extra-small" && !expandable && selection === "checked" && "class-59"
            } ${size === "extra-small" && selection === "selected" && state === "hover" && "class-60"} ${
              !expanded && expandable && !selectable && size === "extra-small" && state === "enabled" && "class-61"
            } ${!expanded && expandable && !selectable && size === "extra-small" && state === "hover" && "class-62"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "extra-large" && "class-63"
            } ${state === "enabled" && expanded && selection === "checked" && size === "extra-large" && "class-64"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-65"
            } ${state === "hover" && expanded && selection === "checked" && size === "extra-large" && "class-66"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "large" && "class-67"
            } ${state === "enabled" && expanded && selection === "checked" && size === "large" && "class-68"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "large" && "class-69"
            } ${state === "hover" && expanded && selection === "checked" && size === "large" && "class-70"} ${
              expanded && selection === "unchecked" && size === "medium" && state === "enabled" && "class-71"
            } ${state === "hover" && expanded && selection === "unchecked" && size === "medium" && "class-72"} ${
              state === "enabled" && expanded && size === "medium" && selection === "checked" && "class-73"
            } ${state === "hover" && expanded && size === "medium" && selection === "checked" && "class-74"} ${
              size === "small" && expanded && selection === "unchecked" && state === "enabled" && "class-75"
            } ${size === "small" && expanded && selection === "unchecked" && state === "hover" && "class-76"} ${
              selectable && selection === "none" && state === "enabled" && "class-77"
            } ${selection === "none" && state === "hover" && selectable && "class-78"} ${
              size === "extra-small" && expanded && selection === "unchecked" && state === "enabled" && "class-79"
            } ${size === "extra-small" && expanded && selection === "unchecked" && state === "hover" && "class-80"} ${
              size === "extra-small" && expanded && selection === "checked" && state === "enabled" && "class-81"
            } ${state === "hover" && size === "extra-small" && expanded && selection === "checked" && "class-82"} ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-83"
            } ${!expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-84"} ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-85"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "hover" &&
              "class-86"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-87"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "large" &&
              state === "enabled" &&
              "class-88"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-89"
            } ${
              !expanded && expandable && selection === "checked" && size === "large" && state === "hover" && "class-90"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-91"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "enabled" &&
              "class-92"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-93"
            } ${
              !expanded && size === "medium" && expandable && selection === "checked" && state === "hover" && "class-94"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "enabled" &&
              "class-95"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "hover" &&
              "class-96"
            } ${size === "small" && expandable && selection === "checked" && state === "enabled" && "class-97"} ${
              state === "hover" && size === "small" && expandable && selection === "checked" && "class-98"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "enabled" &&
              "class-99"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "hover" &&
              "class-100"
            } ${selectable && state === "enabled" && selectType === "none" && "class-101"} ${
              selectable && state === "hover" && selectType === "none" && "class-102"
            } ${!expandable && !selectable && dataTableRowCellMinHeightClassName}`}
            resizerResizerClassName={`${((expandable && !selectable) || (selectable && !expandable)) && "col"} ${
              expandable && selectable && "data-table-header-instance"
            } ${!expandable && !selectable && "col-2"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            state="enabled"
          />
          <DataTableRowCell
            cellText={
              expandable || selectable ? "Content" : !expandable && !selectable ? dataTableRowCellCellText1 : undefined
            }
            className={`${
              ((!expandable && !selectable && size === "medium") ||
                size === "extra-large" ||
                size === "extra-small" ||
                size === "large" ||
                size === "small") &&
              "data-table-row-cell-item"
            } ${size === "medium" && (expandable || selectable) && "class-3"}`}
            minHeightClassName={`${
              state === "enabled" && expanded && !selectable && size === "extra-large" && "class-103"
            } ${state === "hover" && expanded && !selectable && size === "extra-large" && "class-104"} ${
              state === "enabled" && expanded && !selectable && size === "large" && "class-105"
            } ${state === "hover" && expanded && !selectable && size === "large" && "class-106"} ${
              !selectable && expanded && size === "medium" && state === "enabled" && "class-107"
            } ${state === "hover" && !selectable && expanded && size === "medium" && "class-108"} ${
              expanded && size === "small" && !selectable && state === "enabled" && "class-109"
            } ${state === "hover" && expanded && size === "small" && !selectable && "class-110"} ${
              size === "extra-small" && expanded && !selectable && state === "enabled" && "class-111"
            } ${state === "hover" && size === "extra-small" && expanded && !selectable && "class-112"} ${
              !expandable && selection === "unchecked" && size === "extra-large" && "class-113"
            } ${size === "extra-large" && selection === "unselected" && state === "enabled" && "class-114"} ${
              selection === "unselected" && state === "hover" && size === "extra-large" && "class-115"
            } ${
              state === "enabled" && !expandable && selection === "checked" && size === "extra-large" && "class-116"
            } ${size === "extra-large" && selection === "selected" && state === "enabled" && "class-117"} ${
              state === "hover" && !expandable && selectType === "checkbox" && size === "extra-large" && "class-118"
            } ${selection === "selected" && state === "hover" && size === "extra-large" && "class-119"} ${
              !expanded && expandable && !selectable && size === "extra-large" && state === "enabled" && "class-120"
            } ${!expanded && expandable && !selectable && size === "extra-large" && state === "hover" && "class-121"} ${
              state === "enabled" && !expandable && selection === "unchecked" && size === "large" && "class-122"
            } ${!expandable && selection === "unchecked" && state === "hover" && size === "large" && "class-123"} ${
              state === "enabled" && !expandable && selection === "checked" && size === "large" && "class-124"
            } ${state === "hover" && !expandable && selection === "checked" && size === "large" && "class-125"} ${
              size === "large" && selection === "unselected" && state === "enabled" && "class-126"
            } ${selection === "unselected" && state === "hover" && size === "large" && "class-127"} ${
              size === "large" && selection === "selected" && state === "enabled" && "class-128"
            } ${selection === "selected" && state === "hover" && size === "large" && "class-129"} ${
              !expanded && expandable && !selectable && size === "large" && state === "enabled" && "class-130"
            } ${!expanded && expandable && !selectable && size === "large" && state === "hover" && "class-131"} ${
              !expandable && selection === "unchecked" && size === "medium" && state === "enabled" && "class-132"
            } ${selection === "unselected" && size === "medium" && state === "enabled" && "class-133"} ${
              state === "hover" && !expandable && selection === "unchecked" && size === "medium" && "class-134"
            } ${selection === "unselected" && state === "hover" && size === "medium" && "class-135"} ${
              state === "enabled" && !expandable && size === "medium" && selection === "checked" && "class-136"
            } ${selection === "selected" && size === "medium" && state === "enabled" && "class-137"} ${
              state === "hover" && !expandable && size === "medium" && selection === "checked" && "class-138"
            } ${selection === "selected" && state === "hover" && size === "medium" && "class-139"} ${
              !expanded && size === "medium" && expandable && !selectable && state === "enabled" && "class-140"
            } ${!expanded && size === "medium" && expandable && !selectable && state === "hover" && "class-141"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "enabled" && "class-142"
            } ${size === "small" && selection === "unselected" && state === "enabled" && "class-143"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "hover" && "class-144"
            } ${size === "small" && selection === "unselected" && state === "hover" && "class-145"} ${
              !expandable && size === "small" && selection === "checked" && state === "enabled" && "class-146"
            } ${size === "small" && selection === "selected" && state === "enabled" && "class-147"} ${
              state === "hover" && !expandable && size === "small" && selection === "checked" && "class-148"
            } ${size === "small" && selection === "selected" && state === "hover" && "class-149"} ${
              !expanded && expandable && !selectable && size === "small" && state === "enabled" && "class-150"
            } ${!expanded && expandable && !selectable && size === "small" && state === "hover" && "class-151"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "enabled" && "class-152"
            } ${size === "extra-small" && selection === "unselected" && state === "enabled" && "class-153"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "hover" && "class-154"
            } ${size === "extra-small" && selection === "unselected" && state === "hover" && "class-155"} ${
              size === "extra-small" && !expandable && selection === "checked" && state === "enabled" && "class-156"
            } ${size === "extra-small" && selection === "selected" && state === "enabled" && "class-157"} ${
              state === "hover" && size === "extra-small" && !expandable && selection === "checked" && "class-158"
            } ${size === "extra-small" && selection === "selected" && state === "hover" && "class-159"} ${
              !expanded && expandable && !selectable && size === "extra-small" && state === "enabled" && "class-160"
            } ${!expanded && expandable && !selectable && size === "extra-small" && state === "hover" && "class-161"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "extra-large" && "class-162"
            } ${state === "enabled" && expanded && selection === "checked" && size === "extra-large" && "class-163"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-164"
            } ${state === "hover" && expanded && selection === "checked" && size === "extra-large" && "class-165"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "large" && "class-166"
            } ${state === "enabled" && expanded && selection === "checked" && size === "large" && "class-167"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "large" && "class-168"
            } ${state === "hover" && expanded && selection === "checked" && size === "large" && "class-169"} ${
              expanded && selection === "unchecked" && size === "medium" && state === "enabled" && "class-170"
            } ${state === "hover" && expanded && selection === "unchecked" && size === "medium" && "class-171"} ${
              state === "enabled" && expanded && size === "medium" && selection === "checked" && "class-172"
            } ${state === "hover" && expanded && size === "medium" && selection === "checked" && "class-173"} ${
              size === "small" && expanded && selection === "unchecked" && state === "enabled" && "class-174"
            } ${size === "small" && expanded && selection === "unchecked" && state === "hover" && "class-175"} ${
              selectable && selection === "none" && state === "enabled" && "class-176"
            } ${selection === "none" && state === "hover" && selectable && "class-177"} ${
              size === "extra-small" && expanded && selection === "unchecked" && state === "enabled" && "class-178"
            } ${size === "extra-small" && expanded && selection === "unchecked" && state === "hover" && "class-179"} ${
              size === "extra-small" && expanded && selection === "checked" && state === "enabled" && "class-180"
            } ${state === "hover" && size === "extra-small" && expanded && selection === "checked" && "class-181"} ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-182"
            } ${!expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-183"} ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-184"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "hover" &&
              "class-185"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-186"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "large" &&
              state === "enabled" &&
              "class-187"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-188"
            } ${
              !expanded && expandable && selection === "checked" && size === "large" && state === "hover" && "class-189"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-190"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "enabled" &&
              "class-191"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-192"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "hover" &&
              "class-193"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "enabled" &&
              "class-194"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "hover" &&
              "class-195"
            } ${size === "small" && expandable && selection === "checked" && state === "enabled" && "class-196"} ${
              state === "hover" && size === "small" && expandable && selection === "checked" && "class-197"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "enabled" &&
              "class-198"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "hover" &&
              "class-199"
            } ${selectable && state === "enabled" && selectType === "none" && "class-200"} ${
              selectable && state === "hover" && selectType === "none" && "class-201"
            } ${!expandable && !selectable && dataTableRowCellMinHeightClassNameOverride}`}
            resizerResizerClassName={`${((expandable && !selectable) || (selectable && !expandable)) && "col"} ${
              expandable && selectable && "data-table-header-instance"
            } ${!expandable && !selectable && "col-2"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            state="enabled"
          />
          <DataTableRowCell
            cellText={
              expandable || selectable ? "Content" : !expandable && !selectable ? dataTableRowCellCellText2 : undefined
            }
            className={`${
              ((!expandable && !selectable && size === "medium") ||
                size === "extra-large" ||
                size === "extra-small" ||
                size === "large" ||
                size === "small") &&
              "data-table-row-cell-item"
            } ${size === "medium" && (expandable || selectable) && "class-3"}`}
            minHeightClassName={`${
              state === "enabled" && expanded && !selectable && size === "extra-large" && "class-202"
            } ${state === "hover" && expanded && !selectable && size === "extra-large" && "class-203"} ${
              state === "enabled" && expanded && !selectable && size === "large" && "class-204"
            } ${state === "hover" && expanded && !selectable && size === "large" && "class-205"} ${
              !selectable && expanded && size === "medium" && state === "enabled" && "class-206"
            } ${state === "hover" && !selectable && expanded && size === "medium" && "class-207"} ${
              expanded && size === "small" && !selectable && state === "enabled" && "class-208"
            } ${state === "hover" && expanded && size === "small" && !selectable && "class-209"} ${
              size === "extra-small" && expanded && !selectable && state === "enabled" && "class-210"
            } ${state === "hover" && size === "extra-small" && expanded && !selectable && "class-211"} ${
              !expandable && selection === "unchecked" && size === "extra-large" && "class-212"
            } ${size === "extra-large" && selection === "unselected" && state === "enabled" && "class-213"} ${
              selection === "unselected" && state === "hover" && size === "extra-large" && "class-214"
            } ${
              state === "enabled" && !expandable && selection === "checked" && size === "extra-large" && "class-215"
            } ${size === "extra-large" && selection === "selected" && state === "enabled" && "class-216"} ${
              state === "hover" && !expandable && selectType === "checkbox" && size === "extra-large" && "class-217"
            } ${selection === "selected" && state === "hover" && size === "extra-large" && "class-218"} ${
              !expanded && expandable && !selectable && size === "extra-large" && state === "enabled" && "class-219"
            } ${!expanded && expandable && !selectable && size === "extra-large" && state === "hover" && "class-220"} ${
              state === "enabled" && !expandable && selection === "unchecked" && size === "large" && "class-221"
            } ${!expandable && selection === "unchecked" && state === "hover" && size === "large" && "class-222"} ${
              state === "enabled" && !expandable && selection === "checked" && size === "large" && "class-223"
            } ${state === "hover" && !expandable && selection === "checked" && size === "large" && "class-224"} ${
              size === "large" && selection === "unselected" && state === "enabled" && "class-225"
            } ${selection === "unselected" && state === "hover" && size === "large" && "class-226"} ${
              size === "large" && selection === "selected" && state === "enabled" && "class-227"
            } ${selection === "selected" && state === "hover" && size === "large" && "class-228"} ${
              !expanded && expandable && !selectable && size === "large" && state === "enabled" && "class-229"
            } ${!expanded && expandable && !selectable && size === "large" && state === "hover" && "class-230"} ${
              !expandable && selection === "unchecked" && size === "medium" && state === "enabled" && "class-231"
            } ${selection === "unselected" && size === "medium" && state === "enabled" && "class-232"} ${
              state === "hover" && !expandable && selection === "unchecked" && size === "medium" && "class-233"
            } ${selection === "unselected" && state === "hover" && size === "medium" && "class-234"} ${
              state === "enabled" && !expandable && size === "medium" && selection === "checked" && "class-235"
            } ${selection === "selected" && size === "medium" && state === "enabled" && "class-236"} ${
              state === "hover" && !expandable && size === "medium" && selection === "checked" && "class-237"
            } ${selection === "selected" && state === "hover" && size === "medium" && "class-238"} ${
              !expanded && size === "medium" && expandable && !selectable && state === "enabled" && "class-239"
            } ${!expanded && size === "medium" && expandable && !selectable && state === "hover" && "class-240"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "enabled" && "class-241"
            } ${size === "small" && selection === "unselected" && state === "enabled" && "class-242"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "hover" && "class-243"
            } ${size === "small" && selection === "unselected" && state === "hover" && "class-244"} ${
              !expandable && size === "small" && selection === "checked" && state === "enabled" && "class-245"
            } ${size === "small" && selection === "selected" && state === "enabled" && "class-246"} ${
              state === "hover" && !expandable && size === "small" && selection === "checked" && "class-247"
            } ${size === "small" && selection === "selected" && state === "hover" && "class-248"} ${
              !expanded && expandable && !selectable && size === "small" && state === "enabled" && "class-249"
            } ${!expanded && expandable && !selectable && size === "small" && state === "hover" && "class-250"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "enabled" && "class-251"
            } ${size === "extra-small" && selection === "unselected" && state === "enabled" && "class-252"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "hover" && "class-253"
            } ${size === "extra-small" && selection === "unselected" && state === "hover" && "class-254"} ${
              size === "extra-small" && !expandable && selection === "checked" && state === "enabled" && "class-255"
            } ${size === "extra-small" && selection === "selected" && state === "enabled" && "class-256"} ${
              state === "hover" && size === "extra-small" && !expandable && selection === "checked" && "class-257"
            } ${size === "extra-small" && selection === "selected" && state === "hover" && "class-258"} ${
              !expanded && expandable && !selectable && size === "extra-small" && state === "enabled" && "class-259"
            } ${!expanded && expandable && !selectable && size === "extra-small" && state === "hover" && "class-260"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "extra-large" && "class-261"
            } ${state === "enabled" && expanded && selection === "checked" && size === "extra-large" && "class-262"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-263"
            } ${state === "hover" && expanded && selection === "checked" && size === "extra-large" && "class-264"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "large" && "class-265"
            } ${state === "enabled" && expanded && selection === "checked" && size === "large" && "class-266"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "large" && "class-267"
            } ${state === "hover" && expanded && selection === "checked" && size === "large" && "class-268"} ${
              expanded && selection === "unchecked" && size === "medium" && state === "enabled" && "class-269"
            } ${state === "hover" && expanded && selection === "unchecked" && size === "medium" && "class-270"} ${
              state === "enabled" && expanded && size === "medium" && selection === "checked" && "class-271"
            } ${state === "hover" && expanded && size === "medium" && selection === "checked" && "class-272"} ${
              size === "small" && expanded && selection === "unchecked" && state === "enabled" && "class-273"
            } ${size === "small" && expanded && selection === "unchecked" && state === "hover" && "class-274"} ${
              selectable && selection === "none" && state === "enabled" && "class-275"
            } ${selection === "none" && state === "hover" && selectable && "class-276"} ${
              size === "extra-small" && expanded && selection === "unchecked" && state === "enabled" && "class-277"
            } ${size === "extra-small" && expanded && selection === "unchecked" && state === "hover" && "class-278"} ${
              size === "extra-small" && expanded && selection === "checked" && state === "enabled" && "class-279"
            } ${state === "hover" && size === "extra-small" && expanded && selection === "checked" && "class-280"} ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-281"
            } ${!expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-282"} ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-283"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "hover" &&
              "class-284"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-285"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "large" &&
              state === "enabled" &&
              "class-286"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-287"
            } ${
              !expanded && expandable && selection === "checked" && size === "large" && state === "hover" && "class-288"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-289"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "enabled" &&
              "class-290"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-291"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "hover" &&
              "class-292"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "enabled" &&
              "class-293"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "hover" &&
              "class-294"
            } ${size === "small" && expandable && selection === "checked" && state === "enabled" && "class-295"} ${
              state === "hover" && size === "small" && expandable && selection === "checked" && "class-296"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "enabled" &&
              "class-297"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "hover" &&
              "class-298"
            } ${selectable && state === "enabled" && selectType === "none" && "class-299"} ${
              selectable && state === "hover" && selectType === "none" && "class-300"
            } ${!expandable && !selectable && dataTableRowCellImgClassName}`}
            resizerResizerClassName={`${((expandable && !selectable) || (selectable && !expandable)) && "col"} ${
              expandable && selectable && "data-table-header-instance"
            } ${!expandable && !selectable && "col-2"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            state="enabled"
          />
          <DataTableRowCell
            cellText={
              !expandable && !selectable ? dataTableRowCellCellText3 : expandable || selectable ? "Content" : undefined
            }
            className={`${
              ((!expandable && !selectable && size === "medium") ||
                size === "extra-large" ||
                size === "extra-small" ||
                size === "large" ||
                size === "small") &&
              "data-table-row-cell-item"
            } ${size === "medium" && (expandable || selectable) && "class-3"}`}
            minHeightClassName={`${!expandable && !selectable && dataTableRowCellImgClassNameOverride} ${
              state === "enabled" && expanded && !selectable && size === "extra-large" && "class-301"
            } ${state === "hover" && expanded && !selectable && size === "extra-large" && "class-302"} ${
              state === "enabled" && expanded && !selectable && size === "large" && "class-303"
            } ${state === "hover" && expanded && !selectable && size === "large" && "class-304"} ${
              !selectable && expanded && size === "medium" && state === "enabled" && "class-305"
            } ${state === "hover" && !selectable && expanded && size === "medium" && "class-306"} ${
              expanded && size === "small" && !selectable && state === "enabled" && "class-307"
            } ${state === "hover" && expanded && size === "small" && !selectable && "class-308"} ${
              size === "extra-small" && expanded && !selectable && state === "enabled" && "class-309"
            } ${state === "hover" && size === "extra-small" && expanded && !selectable && "class-310"} ${
              !expandable && selection === "unchecked" && size === "extra-large" && "class-311"
            } ${size === "extra-large" && selection === "unselected" && state === "enabled" && "class-312"} ${
              selection === "unselected" && state === "hover" && size === "extra-large" && "class-313"
            } ${
              state === "enabled" && !expandable && selection === "checked" && size === "extra-large" && "class-314"
            } ${size === "extra-large" && selection === "selected" && state === "enabled" && "class-315"} ${
              state === "hover" && !expandable && selectType === "checkbox" && size === "extra-large" && "class-316"
            } ${selection === "selected" && state === "hover" && size === "extra-large" && "class-317"} ${
              !expanded && expandable && !selectable && size === "extra-large" && state === "enabled" && "class-318"
            } ${!expanded && expandable && !selectable && size === "extra-large" && state === "hover" && "class-319"} ${
              state === "enabled" && !expandable && selection === "unchecked" && size === "large" && "class-320"
            } ${!expandable && selection === "unchecked" && state === "hover" && size === "large" && "class-321"} ${
              state === "enabled" && !expandable && selection === "checked" && size === "large" && "class-322"
            } ${state === "hover" && !expandable && selection === "checked" && size === "large" && "class-323"} ${
              size === "large" && selection === "unselected" && state === "enabled" && "class-324"
            } ${selection === "unselected" && state === "hover" && size === "large" && "class-325"} ${
              size === "large" && selection === "selected" && state === "enabled" && "class-326"
            } ${selection === "selected" && state === "hover" && size === "large" && "class-327"} ${
              !expanded && expandable && !selectable && size === "large" && state === "enabled" && "class-328"
            } ${!expanded && expandable && !selectable && size === "large" && state === "hover" && "class-329"} ${
              !expandable && selection === "unchecked" && size === "medium" && state === "enabled" && "class-330"
            } ${selection === "unselected" && size === "medium" && state === "enabled" && "class-331"} ${
              state === "hover" && !expandable && selection === "unchecked" && size === "medium" && "class-332"
            } ${selection === "unselected" && state === "hover" && size === "medium" && "class-333"} ${
              state === "enabled" && !expandable && size === "medium" && selection === "checked" && "class-334"
            } ${selection === "selected" && size === "medium" && state === "enabled" && "class-335"} ${
              state === "hover" && !expandable && size === "medium" && selection === "checked" && "class-336"
            } ${selection === "selected" && state === "hover" && size === "medium" && "class-337"} ${
              !expanded && size === "medium" && expandable && !selectable && state === "enabled" && "class-338"
            } ${!expanded && size === "medium" && expandable && !selectable && state === "hover" && "class-339"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "enabled" && "class-340"
            } ${size === "small" && selection === "unselected" && state === "enabled" && "class-341"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "hover" && "class-342"
            } ${size === "small" && selection === "unselected" && state === "hover" && "class-343"} ${
              !expandable && size === "small" && selection === "checked" && state === "enabled" && "class-344"
            } ${size === "small" && selection === "selected" && state === "enabled" && "class-345"} ${
              state === "hover" && !expandable && size === "small" && selection === "checked" && "class-346"
            } ${size === "small" && selection === "selected" && state === "hover" && "class-347"} ${
              !expanded && expandable && !selectable && size === "small" && state === "enabled" && "class-348"
            } ${!expanded && expandable && !selectable && size === "small" && state === "hover" && "class-349"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "enabled" && "class-350"
            } ${size === "extra-small" && selection === "unselected" && state === "enabled" && "class-351"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "hover" && "class-352"
            } ${size === "extra-small" && selection === "unselected" && state === "hover" && "class-353"} ${
              size === "extra-small" && !expandable && selection === "checked" && state === "enabled" && "class-354"
            } ${size === "extra-small" && selection === "selected" && state === "enabled" && "class-355"} ${
              state === "hover" && size === "extra-small" && !expandable && selection === "checked" && "class-356"
            } ${size === "extra-small" && selection === "selected" && state === "hover" && "class-357"} ${
              !expanded && expandable && !selectable && size === "extra-small" && state === "enabled" && "class-358"
            } ${!expanded && expandable && !selectable && size === "extra-small" && state === "hover" && "class-359"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "extra-large" && "class-360"
            } ${state === "enabled" && expanded && selection === "checked" && size === "extra-large" && "class-361"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-362"
            } ${state === "hover" && expanded && selection === "checked" && size === "extra-large" && "class-363"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "large" && "class-364"
            } ${state === "enabled" && expanded && selection === "checked" && size === "large" && "class-365"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "large" && "class-366"
            } ${state === "hover" && expanded && selection === "checked" && size === "large" && "class-367"} ${
              expanded && selection === "unchecked" && size === "medium" && state === "enabled" && "class-368"
            } ${state === "hover" && expanded && selection === "unchecked" && size === "medium" && "class-369"} ${
              state === "enabled" && expanded && size === "medium" && selection === "checked" && "class-370"
            } ${state === "hover" && expanded && size === "medium" && selection === "checked" && "class-371"} ${
              size === "small" && expanded && selection === "unchecked" && state === "enabled" && "class-372"
            } ${size === "small" && expanded && selection === "unchecked" && state === "hover" && "class-373"} ${
              selectable && selection === "none" && state === "enabled" && "class-374"
            } ${selection === "none" && state === "hover" && selectable && "class-375"} ${
              size === "extra-small" && expanded && selection === "unchecked" && state === "enabled" && "class-376"
            } ${size === "extra-small" && expanded && selection === "unchecked" && state === "hover" && "class-377"} ${
              size === "extra-small" && expanded && selection === "checked" && state === "enabled" && "class-378"
            } ${state === "hover" && size === "extra-small" && expanded && selection === "checked" && "class-379"} ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-380"
            } ${!expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-381"} ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-382"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "hover" &&
              "class-383"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-384"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "large" &&
              state === "enabled" &&
              "class-385"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-386"
            } ${
              !expanded && expandable && selection === "checked" && size === "large" && state === "hover" && "class-387"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-388"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "enabled" &&
              "class-389"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-390"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "hover" &&
              "class-391"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "enabled" &&
              "class-392"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "hover" &&
              "class-393"
            } ${size === "small" && expandable && selection === "checked" && state === "enabled" && "class-394"} ${
              state === "hover" && size === "small" && expandable && selection === "checked" && "class-395"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "enabled" &&
              "class-396"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "hover" &&
              "class-397"
            } ${selectable && state === "enabled" && selectType === "none" && "class-398"} ${
              selectable && state === "hover" && selectType === "none" && "class-399"
            }`}
            resizerResizerClassName={`${!expandable && !selectable && "col-2"} ${
              ((expandable && !selectable) || (selectable && !expandable)) && "col"
            } ${expandable && selectable && "data-table-header-instance"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            state="enabled"
          />
          <DataTableRowCell
            cellText={
              expandable || selectable ? "Content" : !expandable && !selectable ? dataTableRowCellCellText4 : undefined
            }
            className={`${
              ((!expandable && !selectable && size === "medium") ||
                size === "extra-large" ||
                size === "extra-small" ||
                size === "large" ||
                size === "small") &&
              "data-table-row-cell-item"
            } ${size === "medium" && (expandable || selectable) && "class-3"}`}
            minHeightClassName={`${
              state === "enabled" && expanded && selection === "unchecked" && size === "extra-large" && "class-400"
            } ${state === "enabled" && expanded && selection === "checked" && size === "extra-large" && "class-401"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-402"
            } ${state === "hover" && expanded && selection === "checked" && size === "extra-large" && "class-403"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "large" && "class-404"
            } ${state === "enabled" && expanded && selection === "checked" && size === "large" && "class-405"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "large" && "class-406"
            } ${state === "hover" && expanded && selection === "checked" && size === "large" && "class-407"} ${
              expanded && selection === "unchecked" && size === "medium" && state === "enabled" && "class-408"
            } ${state === "hover" && expanded && selection === "unchecked" && size === "medium" && "class-409"} ${
              state === "enabled" && expanded && size === "medium" && selection === "checked" && "class-410"
            } ${state === "hover" && expanded && size === "medium" && selection === "checked" && "class-411"} ${
              size === "small" && expanded && selection === "unchecked" && state === "enabled" && "class-412"
            } ${size === "small" && expanded && selection === "unchecked" && state === "hover" && "class-413"} ${
              selectable && selection === "none" && state === "enabled" && "class-414"
            } ${selection === "none" && state === "hover" && selectable && "class-415"} ${
              size === "extra-small" && expanded && selection === "unchecked" && state === "enabled" && "class-416"
            } ${size === "extra-small" && expanded && selection === "unchecked" && state === "hover" && "class-417"} ${
              size === "extra-small" && expanded && selection === "checked" && state === "enabled" && "class-418"
            } ${state === "hover" && size === "extra-small" && expanded && selection === "checked" && "class-419"} ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-420"
            } ${!expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-421"} ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-422"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "hover" &&
              "class-423"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-424"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "large" &&
              state === "enabled" &&
              "class-425"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-426"
            } ${
              !expanded && expandable && selection === "checked" && size === "large" && state === "hover" && "class-427"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-428"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "enabled" &&
              "class-429"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-430"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "hover" &&
              "class-431"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "enabled" &&
              "class-432"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "hover" &&
              "class-433"
            } ${size === "small" && expandable && selection === "checked" && state === "enabled" && "class-434"} ${
              state === "hover" && size === "small" && expandable && selection === "checked" && "class-435"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "enabled" &&
              "class-436"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "hover" &&
              "class-437"
            } ${selectable && state === "enabled" && selectType === "none" && "class-438"} ${
              selectable && state === "hover" && selectType === "none" && "class-439"
            } ${!expandable && !selectable && dataTableRowCellMinHeightClassName1} ${
              state === "enabled" && expanded && !selectable && size === "extra-large" && "class-440"
            } ${state === "hover" && expanded && !selectable && size === "extra-large" && "class-441"} ${
              state === "enabled" && expanded && !selectable && size === "large" && "class-442"
            } ${state === "hover" && expanded && !selectable && size === "large" && "class-443"} ${
              !selectable && expanded && size === "medium" && state === "enabled" && "class-444"
            } ${state === "hover" && !selectable && expanded && size === "medium" && "class-445"} ${
              expanded && size === "small" && !selectable && state === "enabled" && "class-446"
            } ${state === "hover" && expanded && size === "small" && !selectable && "class-447"} ${
              size === "extra-small" && expanded && !selectable && state === "enabled" && "class-448"
            } ${state === "hover" && size === "extra-small" && expanded && !selectable && "class-449"} ${
              !expandable && selection === "unchecked" && size === "extra-large" && "class-450"
            } ${size === "extra-large" && selection === "unselected" && state === "enabled" && "class-451"} ${
              selection === "unselected" && state === "hover" && size === "extra-large" && "class-452"
            } ${
              state === "enabled" && !expandable && selection === "checked" && size === "extra-large" && "class-453"
            } ${size === "extra-large" && selection === "selected" && state === "enabled" && "class-454"} ${
              state === "hover" && !expandable && selectType === "checkbox" && size === "extra-large" && "class-455"
            } ${selection === "selected" && state === "hover" && size === "extra-large" && "class-456"} ${
              !expanded && expandable && !selectable && size === "extra-large" && state === "enabled" && "class-457"
            } ${!expanded && expandable && !selectable && size === "extra-large" && state === "hover" && "class-458"} ${
              state === "enabled" && !expandable && selection === "unchecked" && size === "large" && "class-459"
            } ${!expandable && selection === "unchecked" && state === "hover" && size === "large" && "class-460"} ${
              state === "enabled" && !expandable && selection === "checked" && size === "large" && "class-461"
            } ${state === "hover" && !expandable && selection === "checked" && size === "large" && "class-462"} ${
              size === "large" && selection === "unselected" && state === "enabled" && "class-463"
            } ${selection === "unselected" && state === "hover" && size === "large" && "class-464"} ${
              size === "large" && selection === "selected" && state === "enabled" && "class-465"
            } ${selection === "selected" && state === "hover" && size === "large" && "class-466"} ${
              !expanded && expandable && !selectable && size === "large" && state === "enabled" && "class-467"
            } ${!expanded && expandable && !selectable && size === "large" && state === "hover" && "class-468"} ${
              !expandable && selection === "unchecked" && size === "medium" && state === "enabled" && "class-469"
            } ${selection === "unselected" && size === "medium" && state === "enabled" && "class-470"} ${
              state === "hover" && !expandable && selection === "unchecked" && size === "medium" && "class-471"
            } ${selection === "unselected" && state === "hover" && size === "medium" && "class-472"} ${
              state === "enabled" && !expandable && size === "medium" && selection === "checked" && "class-473"
            } ${selection === "selected" && size === "medium" && state === "enabled" && "class-474"} ${
              state === "hover" && !expandable && size === "medium" && selection === "checked" && "class-475"
            } ${selection === "selected" && state === "hover" && size === "medium" && "class-476"} ${
              !expanded && size === "medium" && expandable && !selectable && state === "enabled" && "class-477"
            } ${!expanded && size === "medium" && expandable && !selectable && state === "hover" && "class-478"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "enabled" && "class-479"
            } ${size === "small" && selection === "unselected" && state === "enabled" && "class-480"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "hover" && "class-481"
            } ${size === "small" && selection === "unselected" && state === "hover" && "class-482"} ${
              !expandable && size === "small" && selection === "checked" && state === "enabled" && "class-483"
            } ${size === "small" && selection === "selected" && state === "enabled" && "class-484"} ${
              state === "hover" && !expandable && size === "small" && selection === "checked" && "class-485"
            } ${size === "small" && selection === "selected" && state === "hover" && "class-486"} ${
              !expanded && expandable && !selectable && size === "small" && state === "enabled" && "class-487"
            } ${!expanded && expandable && !selectable && size === "small" && state === "hover" && "class-488"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "enabled" && "class-489"
            } ${size === "extra-small" && selection === "unselected" && state === "enabled" && "class-490"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "hover" && "class-491"
            } ${size === "extra-small" && selection === "unselected" && state === "hover" && "class-492"} ${
              size === "extra-small" && !expandable && selection === "checked" && state === "enabled" && "class-493"
            } ${size === "extra-small" && selection === "selected" && state === "enabled" && "class-494"} ${
              state === "hover" && size === "extra-small" && !expandable && selection === "checked" && "class-495"
            } ${size === "extra-small" && selection === "selected" && state === "hover" && "class-496"} ${
              !expanded && expandable && !selectable && size === "extra-small" && state === "enabled" && "class-497"
            } ${!expanded && expandable && !selectable && size === "extra-small" && state === "hover" && "class-498"}`}
            resizerResizerClassName={`${expandable && selectable && "data-table-header-instance"} ${
              !expandable && !selectable && "col-2"
            } ${((expandable && !selectable) || (selectable && !expandable)) && "col"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            state="enabled"
          />
          <DataTableRowCell
            cellText={
              expandable || selectable ? "Content" : !expandable && !selectable ? dataTableRowCellCellText5 : undefined
            }
            className={`${
              ((!expandable && !selectable && size === "medium") ||
                size === "extra-large" ||
                size === "extra-small" ||
                size === "large" ||
                size === "small") &&
              "data-table-row-cell-item"
            } ${size === "medium" && (expandable || selectable) && "class-3"}`}
            minHeightClassName={`${
              state === "enabled" && expanded && selection === "unchecked" && size === "extra-large" && "class-499"
            } ${state === "enabled" && expanded && selection === "checked" && size === "extra-large" && "class-500"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-501"
            } ${state === "hover" && expanded && selection === "checked" && size === "extra-large" && "class-502"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "large" && "class-503"
            } ${state === "enabled" && expanded && selection === "checked" && size === "large" && "class-504"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "large" && "class-505"
            } ${state === "hover" && expanded && selection === "checked" && size === "large" && "class-506"} ${
              expanded && selection === "unchecked" && size === "medium" && state === "enabled" && "class-507"
            } ${state === "hover" && expanded && selection === "unchecked" && size === "medium" && "class-508"} ${
              state === "enabled" && expanded && size === "medium" && selection === "checked" && "class-509"
            } ${state === "hover" && expanded && size === "medium" && selection === "checked" && "class-510"} ${
              size === "small" && expanded && selection === "unchecked" && state === "enabled" && "class-511"
            } ${size === "small" && expanded && selection === "unchecked" && state === "hover" && "class-512"} ${
              selectable && selection === "none" && state === "enabled" && "class-513"
            } ${selection === "none" && state === "hover" && selectable && "class-514"} ${
              size === "extra-small" && expanded && selection === "unchecked" && state === "enabled" && "class-515"
            } ${size === "extra-small" && expanded && selection === "unchecked" && state === "hover" && "class-516"} ${
              size === "extra-small" && expanded && selection === "checked" && state === "enabled" && "class-517"
            } ${state === "hover" && size === "extra-small" && expanded && selection === "checked" && "class-518"} ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-519"
            } ${!expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-520"} ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-521"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "hover" &&
              "class-522"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-523"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "large" &&
              state === "enabled" &&
              "class-524"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-525"
            } ${
              !expanded && expandable && selection === "checked" && size === "large" && state === "hover" && "class-526"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-527"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "enabled" &&
              "class-528"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-529"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "hover" &&
              "class-530"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "enabled" &&
              "class-531"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "hover" &&
              "class-532"
            } ${size === "small" && expandable && selection === "checked" && state === "enabled" && "class-533"} ${
              state === "hover" && size === "small" && expandable && selection === "checked" && "class-534"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "enabled" &&
              "class-535"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "hover" &&
              "class-536"
            } ${selectable && state === "enabled" && selectType === "none" && "class-537"} ${
              selectable && state === "hover" && selectType === "none" && "class-538"
            } ${!expandable && !selectable && dataTableRowCellMinHeightClassName2} ${
              state === "enabled" && expanded && !selectable && size === "extra-large" && "class-539"
            } ${state === "hover" && expanded && !selectable && size === "extra-large" && "class-540"} ${
              state === "enabled" && expanded && !selectable && size === "large" && "class-541"
            } ${state === "hover" && expanded && !selectable && size === "large" && "class-542"} ${
              !selectable && expanded && size === "medium" && state === "enabled" && "class-543"
            } ${state === "hover" && !selectable && expanded && size === "medium" && "class-544"} ${
              expanded && size === "small" && !selectable && state === "enabled" && "class-545"
            } ${state === "hover" && expanded && size === "small" && !selectable && "class-546"} ${
              size === "extra-small" && expanded && !selectable && state === "enabled" && "class-547"
            } ${state === "hover" && size === "extra-small" && expanded && !selectable && "class-548"} ${
              !expandable && selection === "unchecked" && size === "extra-large" && "class-549"
            } ${size === "extra-large" && selection === "unselected" && state === "enabled" && "class-550"} ${
              selection === "unselected" && state === "hover" && size === "extra-large" && "class-551"
            } ${
              state === "enabled" && !expandable && selection === "checked" && size === "extra-large" && "class-552"
            } ${size === "extra-large" && selection === "selected" && state === "enabled" && "class-553"} ${
              state === "hover" && !expandable && selectType === "checkbox" && size === "extra-large" && "class-554"
            } ${selection === "selected" && state === "hover" && size === "extra-large" && "class-555"} ${
              !expanded && expandable && !selectable && size === "extra-large" && state === "enabled" && "class-556"
            } ${!expanded && expandable && !selectable && size === "extra-large" && state === "hover" && "class-557"} ${
              state === "enabled" && !expandable && selection === "unchecked" && size === "large" && "class-558"
            } ${!expandable && selection === "unchecked" && state === "hover" && size === "large" && "class-559"} ${
              state === "enabled" && !expandable && selection === "checked" && size === "large" && "class-560"
            } ${state === "hover" && !expandable && selection === "checked" && size === "large" && "class-561"} ${
              size === "large" && selection === "unselected" && state === "enabled" && "class-562"
            } ${selection === "unselected" && state === "hover" && size === "large" && "class-563"} ${
              size === "large" && selection === "selected" && state === "enabled" && "class-564"
            } ${selection === "selected" && state === "hover" && size === "large" && "class-565"} ${
              !expanded && expandable && !selectable && size === "large" && state === "enabled" && "class-566"
            } ${!expanded && expandable && !selectable && size === "large" && state === "hover" && "class-567"} ${
              !expandable && selection === "unchecked" && size === "medium" && state === "enabled" && "class-568"
            } ${selection === "unselected" && size === "medium" && state === "enabled" && "class-569"} ${
              state === "hover" && !expandable && selection === "unchecked" && size === "medium" && "class-570"
            } ${selection === "unselected" && state === "hover" && size === "medium" && "class-571"} ${
              state === "enabled" && !expandable && size === "medium" && selection === "checked" && "class-572"
            } ${selection === "selected" && size === "medium" && state === "enabled" && "class-573"} ${
              state === "hover" && !expandable && size === "medium" && selection === "checked" && "class-574"
            } ${selection === "selected" && state === "hover" && size === "medium" && "class-575"} ${
              !expanded && size === "medium" && expandable && !selectable && state === "enabled" && "class-576"
            } ${!expanded && size === "medium" && expandable && !selectable && state === "hover" && "class-577"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "enabled" && "class-578"
            } ${size === "small" && selection === "unselected" && state === "enabled" && "class-579"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "hover" && "class-580"
            } ${size === "small" && selection === "unselected" && state === "hover" && "class-581"} ${
              !expandable && size === "small" && selection === "checked" && state === "enabled" && "class-582"
            } ${size === "small" && selection === "selected" && state === "enabled" && "class-583"} ${
              state === "hover" && !expandable && size === "small" && selection === "checked" && "class-584"
            } ${size === "small" && selection === "selected" && state === "hover" && "class-585"} ${
              !expanded && expandable && !selectable && size === "small" && state === "enabled" && "class-586"
            } ${!expanded && expandable && !selectable && size === "small" && state === "hover" && "class-587"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "enabled" && "class-588"
            } ${size === "extra-small" && selection === "unselected" && state === "enabled" && "class-589"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "hover" && "class-590"
            } ${size === "extra-small" && selection === "unselected" && state === "hover" && "class-591"} ${
              size === "extra-small" && !expandable && selection === "checked" && state === "enabled" && "class-592"
            } ${size === "extra-small" && selection === "selected" && state === "enabled" && "class-593"} ${
              state === "hover" && size === "extra-small" && !expandable && selection === "checked" && "class-594"
            } ${size === "extra-small" && selection === "selected" && state === "hover" && "class-595"} ${
              !expanded && expandable && !selectable && size === "extra-small" && state === "enabled" && "class-596"
            } ${!expanded && expandable && !selectable && size === "extra-small" && state === "hover" && "class-597"}`}
            resizerResizerClassName={`${expandable && selectable && "data-table-header-instance"} ${
              !expandable && !selectable && "col-2"
            } ${((expandable && !selectable) || (selectable && !expandable)) && "col"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            state="enabled"
          />
          <DataTableRowCell
            cellText={
              expandable || selectable ? "Content" : !expandable && !selectable ? dataTableRowCellCellText6 : undefined
            }
            className={`${
              ((!expandable && !selectable && size === "medium") ||
                size === "extra-large" ||
                size === "extra-small" ||
                size === "large" ||
                size === "small") &&
              "data-table-row-cell-item"
            } ${size === "medium" && (expandable || selectable) && "class-3"}`}
            minHeightClassName={`${
              state === "enabled" && expanded && !selectable && size === "extra-large" && "class-598"
            } ${state === "hover" && expanded && !selectable && size === "extra-large" && "class-599"} ${
              state === "enabled" && expanded && !selectable && size === "large" && "class-600"
            } ${state === "hover" && expanded && !selectable && size === "large" && "class-601"} ${
              !selectable && expanded && size === "medium" && state === "enabled" && "class-602"
            } ${state === "hover" && !selectable && expanded && size === "medium" && "class-603"} ${
              expanded && size === "small" && !selectable && state === "enabled" && "class-604"
            } ${state === "hover" && expanded && size === "small" && !selectable && "class-605"} ${
              size === "extra-small" && expanded && !selectable && state === "enabled" && "class-606"
            } ${state === "hover" && size === "extra-small" && expanded && !selectable && "class-607"} ${
              !expandable && selection === "unchecked" && size === "extra-large" && "class-608"
            } ${size === "extra-large" && selection === "unselected" && state === "enabled" && "class-609"} ${
              selection === "unselected" && state === "hover" && size === "extra-large" && "class-610"
            } ${
              state === "enabled" && !expandable && selection === "checked" && size === "extra-large" && "class-611"
            } ${size === "extra-large" && selection === "selected" && state === "enabled" && "class-612"} ${
              state === "hover" && !expandable && selectType === "checkbox" && size === "extra-large" && "class-613"
            } ${selection === "selected" && state === "hover" && size === "extra-large" && "class-614"} ${
              !expanded && expandable && !selectable && size === "extra-large" && state === "enabled" && "class-615"
            } ${!expanded && expandable && !selectable && size === "extra-large" && state === "hover" && "class-616"} ${
              state === "enabled" && !expandable && selection === "unchecked" && size === "large" && "class-617"
            } ${!expandable && selection === "unchecked" && state === "hover" && size === "large" && "class-618"} ${
              state === "enabled" && !expandable && selection === "checked" && size === "large" && "class-619"
            } ${state === "hover" && !expandable && selection === "checked" && size === "large" && "class-620"} ${
              size === "large" && selection === "unselected" && state === "enabled" && "class-621"
            } ${selection === "unselected" && state === "hover" && size === "large" && "class-622"} ${
              size === "large" && selection === "selected" && state === "enabled" && "class-623"
            } ${selection === "selected" && state === "hover" && size === "large" && "class-624"} ${
              !expanded && expandable && !selectable && size === "large" && state === "enabled" && "class-625"
            } ${!expanded && expandable && !selectable && size === "large" && state === "hover" && "class-626"} ${
              !expandable && selection === "unchecked" && size === "medium" && state === "enabled" && "class-627"
            } ${selection === "unselected" && size === "medium" && state === "enabled" && "class-628"} ${
              state === "hover" && !expandable && selection === "unchecked" && size === "medium" && "class-629"
            } ${selection === "unselected" && state === "hover" && size === "medium" && "class-630"} ${
              state === "enabled" && !expandable && size === "medium" && selection === "checked" && "class-631"
            } ${selection === "selected" && size === "medium" && state === "enabled" && "class-632"} ${
              state === "hover" && !expandable && size === "medium" && selection === "checked" && "class-633"
            } ${selection === "selected" && state === "hover" && size === "medium" && "class-634"} ${
              !expanded && size === "medium" && expandable && !selectable && state === "enabled" && "class-635"
            } ${!expanded && size === "medium" && expandable && !selectable && state === "hover" && "class-636"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "enabled" && "class-637"
            } ${size === "small" && selection === "unselected" && state === "enabled" && "class-638"} ${
              size === "small" && !expandable && selection === "unchecked" && state === "hover" && "class-639"
            } ${size === "small" && selection === "unselected" && state === "hover" && "class-640"} ${
              !expandable && size === "small" && selection === "checked" && state === "enabled" && "class-641"
            } ${size === "small" && selection === "selected" && state === "enabled" && "class-642"} ${
              state === "hover" && !expandable && size === "small" && selection === "checked" && "class-643"
            } ${size === "small" && selection === "selected" && state === "hover" && "class-644"} ${
              !expanded && expandable && !selectable && size === "small" && state === "enabled" && "class-645"
            } ${!expanded && expandable && !selectable && size === "small" && state === "hover" && "class-646"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "enabled" && "class-647"
            } ${size === "extra-small" && selection === "unselected" && state === "enabled" && "class-648"} ${
              size === "extra-small" && !expandable && selection === "unchecked" && state === "hover" && "class-649"
            } ${size === "extra-small" && selection === "unselected" && state === "hover" && "class-650"} ${
              size === "extra-small" && !expandable && selection === "checked" && state === "enabled" && "class-651"
            } ${size === "extra-small" && selection === "selected" && state === "enabled" && "class-652"} ${
              state === "hover" && size === "extra-small" && !expandable && selection === "checked" && "class-653"
            } ${size === "extra-small" && selection === "selected" && state === "hover" && "class-654"} ${
              !expanded && expandable && !selectable && size === "extra-small" && state === "enabled" && "class-655"
            } ${!expanded && expandable && !selectable && size === "extra-small" && state === "hover" && "class-656"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "extra-large" && "class-657"
            } ${state === "enabled" && expanded && selection === "checked" && size === "extra-large" && "class-658"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-659"
            } ${state === "hover" && expanded && selection === "checked" && size === "extra-large" && "class-660"} ${
              state === "enabled" && expanded && selection === "unchecked" && size === "large" && "class-661"
            } ${state === "enabled" && expanded && selection === "checked" && size === "large" && "class-662"} ${
              expanded && selection === "unchecked" && state === "hover" && size === "large" && "class-663"
            } ${state === "hover" && expanded && selection === "checked" && size === "large" && "class-664"} ${
              expanded && selection === "unchecked" && size === "medium" && state === "enabled" && "class-665"
            } ${state === "hover" && expanded && selection === "unchecked" && size === "medium" && "class-666"} ${
              state === "enabled" && expanded && size === "medium" && selection === "checked" && "class-667"
            } ${state === "hover" && expanded && size === "medium" && selection === "checked" && "class-668"} ${
              size === "small" && expanded && selection === "unchecked" && state === "enabled" && "class-669"
            } ${size === "small" && expanded && selection === "unchecked" && state === "hover" && "class-670"} ${
              selectable && selection === "none" && state === "enabled" && "class-671"
            } ${selection === "none" && state === "hover" && selectable && "class-672"} ${
              size === "extra-small" && expanded && selection === "unchecked" && state === "enabled" && "class-673"
            } ${size === "extra-small" && expanded && selection === "unchecked" && state === "hover" && "class-674"} ${
              size === "extra-small" && expanded && selection === "checked" && state === "enabled" && "class-675"
            } ${state === "hover" && size === "extra-small" && expanded && selection === "checked" && "class-676"} ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-677"
            } ${!expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-678"} ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "enabled" &&
              "class-679"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "extra-large" &&
              state === "hover" &&
              "class-680"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-681"
            } ${
              !expanded &&
              expandable &&
              selection === "checked" &&
              size === "large" &&
              state === "enabled" &&
              "class-682"
            } ${
              !expanded &&
              expandable &&
              size === "large" &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-683"
            } ${
              !expanded && expandable && selection === "checked" && size === "large" && state === "hover" && "class-684"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "enabled" &&
              "class-685"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "enabled" &&
              "class-686"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "unchecked" &&
              state === "hover" &&
              "class-687"
            } ${
              !expanded &&
              size === "medium" &&
              expandable &&
              selection === "checked" &&
              state === "hover" &&
              "class-688"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "enabled" &&
              "class-689"
            } ${
              !expanded &&
              expandable &&
              selection === "unchecked" &&
              size === "small" &&
              state === "hover" &&
              "class-690"
            } ${size === "small" && expandable && selection === "checked" && state === "enabled" && "class-691"} ${
              state === "hover" && size === "small" && expandable && selection === "checked" && "class-692"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "enabled" &&
              "class-693"
            } ${
              !expanded &&
              selectType === "checkbox" &&
              expandable &&
              size === "extra-small" &&
              state === "hover" &&
              "class-694"
            } ${selectable && state === "enabled" && selectType === "none" && "class-695"} ${
              selectable && state === "hover" && selectType === "none" && "class-696"
            } ${!expandable && !selectable && dataTableRowCellMinHeightClassName3}`}
            resizerResizerClassName={`${((expandable && !selectable) || (selectable && !expandable)) && "col"} ${
              expandable && selectable && "data-table-header-instance"
            } ${!expandable && !selectable && "col-2"}`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
            state="enabled"
          />
          {(expandable || selectable) && (
            <DataTableRowCell
              cellText="Content"
              className={`${
                ["extra-large", "extra-small", "large", "small"].includes(size) && "data-table-row-cell-item"
              } ${size === "medium" && "class-3"}`}
              minHeightClassName={`${
                state === "enabled" && expanded && !selectable && size === "extra-large" && "class-697"
              } ${state === "hover" && expanded && !selectable && size === "extra-large" && "class-698"} ${
                state === "enabled" && expanded && !selectable && size === "large" && "class-699"
              } ${state === "hover" && expanded && !selectable && size === "large" && "class-700"} ${
                !selectable && expanded && size === "medium" && state === "enabled" && "class-701"
              } ${state === "hover" && !selectable && expanded && size === "medium" && "class-702"} ${
                expanded && size === "small" && !selectable && state === "enabled" && "class-703"
              } ${state === "hover" && expanded && size === "small" && !selectable && "class-704"} ${
                size === "extra-small" && expanded && !selectable && state === "enabled" && "class-705"
              } ${state === "hover" && size === "extra-small" && expanded && !selectable && "class-706"} ${
                !expandable && selection === "unchecked" && size === "extra-large" && "class-707"
              } ${size === "extra-large" && selection === "unselected" && state === "enabled" && "class-708"} ${
                selection === "unselected" && state === "hover" && size === "extra-large" && "class-709"
              } ${
                state === "enabled" && !expandable && selection === "checked" && size === "extra-large" && "class-710"
              } ${size === "extra-large" && selection === "selected" && state === "enabled" && "class-711"} ${
                state === "hover" && !expandable && selectType === "checkbox" && size === "extra-large" && "class-712"
              } ${selection === "selected" && state === "hover" && size === "extra-large" && "class-713"} ${
                !expanded && state === "enabled" && !selectable && size === "extra-large" && "class-714"
              } ${state === "hover" && !expanded && !selectable && size === "extra-large" && "class-715"} ${
                state === "enabled" && !expandable && selection === "unchecked" && size === "large" && "class-716"
              } ${!expandable && selection === "unchecked" && state === "hover" && size === "large" && "class-717"} ${
                state === "enabled" && !expandable && selection === "checked" && size === "large" && "class-718"
              } ${state === "hover" && !expandable && selection === "checked" && size === "large" && "class-719"} ${
                size === "large" && selection === "unselected" && state === "enabled" && "class-720"
              } ${selection === "unselected" && state === "hover" && size === "large" && "class-721"} ${
                size === "large" && selection === "selected" && state === "enabled" && "class-722"
              } ${selection === "selected" && state === "hover" && size === "large" && "class-723"} ${
                !expanded && state === "enabled" && !selectable && size === "large" && "class-724"
              } ${state === "hover" && !expanded && !selectable && size === "large" && "class-725"} ${
                !expandable && selection === "unchecked" && size === "medium" && state === "enabled" && "class-726"
              } ${selection === "unselected" && size === "medium" && state === "enabled" && "class-727"} ${
                state === "hover" && !expandable && selection === "unchecked" && size === "medium" && "class-728"
              } ${selection === "unselected" && state === "hover" && size === "medium" && "class-729"} ${
                state === "enabled" && !expandable && size === "medium" && selection === "checked" && "class-730"
              } ${selection === "selected" && size === "medium" && state === "enabled" && "class-731"} ${
                state === "hover" && !expandable && size === "medium" && selection === "checked" && "class-732"
              } ${selection === "selected" && state === "hover" && size === "medium" && "class-733"} ${
                !expanded && !selectable && size === "medium" && state === "enabled" && "class-734"
              } ${state === "hover" && !expanded && !selectable && size === "medium" && "class-735"} ${
                size === "small" && !expandable && selection === "unchecked" && state === "enabled" && "class-736"
              } ${size === "small" && selection === "unselected" && state === "enabled" && "class-737"} ${
                size === "small" && !expandable && selection === "unchecked" && state === "hover" && "class-738"
              } ${size === "small" && selection === "unselected" && state === "hover" && "class-739"} ${
                !expandable && size === "small" && selection === "checked" && state === "enabled" && "class-740"
              } ${size === "small" && selection === "selected" && state === "enabled" && "class-741"} ${
                state === "hover" && !expandable && size === "small" && selection === "checked" && "class-742"
              } ${size === "small" && selection === "selected" && state === "hover" && "class-743"} ${
                !expanded && size === "small" && !selectable && state === "enabled" && "class-744"
              } ${state === "hover" && !expanded && size === "small" && !selectable && "class-745"} ${
                size === "extra-small" && !expandable && selection === "unchecked" && state === "enabled" && "class-746"
              } ${size === "extra-small" && selection === "unselected" && state === "enabled" && "class-747"} ${
                size === "extra-small" && !expandable && selection === "unchecked" && state === "hover" && "class-748"
              } ${size === "extra-small" && selection === "unselected" && state === "hover" && "class-749"} ${
                size === "extra-small" && !expandable && selection === "checked" && state === "enabled" && "class-750"
              } ${size === "extra-small" && selection === "selected" && state === "enabled" && "class-751"} ${
                state === "hover" && size === "extra-small" && !expandable && selection === "checked" && "class-752"
              } ${size === "extra-small" && selection === "selected" && state === "hover" && "class-753"} ${
                size === "extra-small" && !expanded && !selectable && state === "enabled" && "class-754"
              } ${size === "extra-small" && !expanded && !selectable && state === "hover" && "class-755"} ${
                state === "enabled" && expanded && selection === "unchecked" && size === "extra-large" && "class-756"
              } ${
                state === "enabled" && expanded && selection === "checked" && size === "extra-large" && "class-757"
              } ${
                expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-758"
              } ${state === "hover" && expanded && selection === "checked" && size === "extra-large" && "class-759"} ${
                state === "enabled" && expanded && selection === "unchecked" && size === "large" && "class-760"
              } ${state === "enabled" && expanded && selection === "checked" && size === "large" && "class-761"} ${
                expanded && selection === "unchecked" && state === "hover" && size === "large" && "class-762"
              } ${state === "hover" && expanded && selection === "checked" && size === "large" && "class-763"} ${
                expanded && selection === "unchecked" && size === "medium" && state === "enabled" && "class-764"
              } ${state === "hover" && expanded && selection === "unchecked" && size === "medium" && "class-765"} ${
                state === "enabled" && expanded && size === "medium" && selection === "checked" && "class-766"
              } ${state === "hover" && expanded && size === "medium" && selection === "checked" && "class-767"} ${
                size === "small" && expanded && selection === "unchecked" && state === "enabled" && "class-768"
              } ${size === "small" && expanded && selection === "unchecked" && state === "hover" && "class-769"} ${
                selectable && selection === "none" && state === "enabled" && "class-770"
              } ${selection === "none" && state === "hover" && selectable && "class-771"} ${
                size === "extra-small" && expanded && selection === "unchecked" && state === "enabled" && "class-772"
              } ${
                size === "extra-small" && expanded && selection === "unchecked" && state === "hover" && "class-773"
              } ${
                size === "extra-small" && expanded && selection === "checked" && state === "enabled" && "class-774"
              } ${state === "hover" && size === "extra-small" && expanded && selection === "checked" && "class-775"} ${
                !expanded &&
                expandable &&
                selection === "unchecked" &&
                size === "extra-large" &&
                state === "enabled" &&
                "class-776"
              } ${
                !expanded && selection === "unchecked" && state === "hover" && size === "extra-large" && "class-777"
              } ${
                !expanded &&
                expandable &&
                selection === "checked" &&
                size === "extra-large" &&
                state === "enabled" &&
                "class-778"
              } ${
                !expanded &&
                expandable &&
                selection === "checked" &&
                size === "extra-large" &&
                state === "hover" &&
                "class-779"
              } ${
                !expanded &&
                expandable &&
                size === "large" &&
                selection === "unchecked" &&
                state === "enabled" &&
                "class-780"
              } ${
                !expanded &&
                expandable &&
                selection === "checked" &&
                size === "large" &&
                state === "enabled" &&
                "class-781"
              } ${
                !expanded &&
                expandable &&
                size === "large" &&
                selection === "unchecked" &&
                state === "hover" &&
                "class-782"
              } ${
                !expanded &&
                expandable &&
                selection === "checked" &&
                size === "large" &&
                state === "hover" &&
                "class-783"
              } ${
                !expanded &&
                size === "medium" &&
                expandable &&
                selection === "unchecked" &&
                state === "enabled" &&
                "class-784"
              } ${
                !expanded &&
                size === "medium" &&
                expandable &&
                selection === "checked" &&
                state === "enabled" &&
                "class-785"
              } ${
                !expanded &&
                size === "medium" &&
                expandable &&
                selection === "unchecked" &&
                state === "hover" &&
                "class-786"
              } ${
                !expanded &&
                size === "medium" &&
                expandable &&
                selection === "checked" &&
                state === "hover" &&
                "class-787"
              } ${
                !expanded &&
                expandable &&
                selection === "unchecked" &&
                size === "small" &&
                state === "enabled" &&
                "class-788"
              } ${
                !expanded &&
                expandable &&
                selection === "unchecked" &&
                size === "small" &&
                state === "hover" &&
                "class-789"
              } ${size === "small" && expandable && selection === "checked" && state === "enabled" && "class-790"} ${
                state === "hover" && size === "small" && expandable && selection === "checked" && "class-791"
              } ${
                !expanded &&
                selectType === "checkbox" &&
                expandable &&
                size === "extra-small" &&
                state === "enabled" &&
                "class-792"
              } ${
                !expanded &&
                selectType === "checkbox" &&
                expandable &&
                size === "extra-small" &&
                state === "hover" &&
                "class-793"
              } ${selectable && state === "enabled" && selectType === "none" && "class-794"} ${
                selectable && state === "hover" && selectType === "none" && "class-795"
              }`}
              resizerResizerClassName={`${(!expandable || !selectable) && "col"} ${
                expandable && selectable && "data-table-header-instance"
              }`}
              size={
                size === "extra-large"
                  ? "extra-large"
                  : size === "large"
                  ? "large"
                  : size === "medium"
                  ? "medium"
                  : size === "small"
                  ? "small"
                  : size === "extra-small"
                  ? "extra-small"
                  : undefined
              }
              state="enabled"
            />
          )}

          {!expandable && !selectable && (
            <>
              <>
                {visible && (
                  <DataTableRowCell
                    cellText="Content"
                    className="data-table-row-cell-item"
                    minHeightClassName={`${state === "enabled" && size === "extra-large" && "class-796"} ${
                      state === "hover" && size === "extra-large" && "class-797"
                    } ${state === "enabled" && size === "large" && "class-798"} ${
                      state === "hover" && size === "large" && "class-799"
                    } ${size === "medium" && state === "enabled" && "class-800"} ${
                      state === "hover" && size === "medium" && "class-801"
                    } ${size === "small" && state === "enabled" && "class-802"} ${
                      size === "small" && state === "hover" && "class-803"
                    } ${size === "extra-small" && state === "enabled" && "class-804"} ${
                      size === "extra-small" && state === "hover" && "class-805"
                    }`}
                    resizerResizerClassName="col-2"
                    size={
                      size === "extra-large"
                        ? "extra-large"
                        : size === "large"
                        ? "large"
                        : size === "medium"
                        ? "medium"
                        : size === "small"
                        ? "small"
                        : size === "extra-small"
                        ? "extra-small"
                        : undefined
                    }
                    state="enabled"
                  />
                )}
              </>
            </>
          )}
        </div>
      )}

      {((!expandable && selection === "checked" && size === "extra-large" && state === "hover") ||
        (!expandable && selection === "checked" && size === "large" && state === "hover") ||
        (!expandable && selection === "none" && size === "extra-large" && state === "hover") ||
        (!expandable && selection === "none" && size === "extra-small" && state === "hover") ||
        (!expandable && selection === "none" && size === "large" && state === "hover") ||
        (!expandable && selection === "unchecked" && size === "extra-small" && state === "hover") ||
        (!expandable && selection === "unchecked" && size === "large" && state === "hover") ||
        (!expandable && selection === "unchecked" && state === "enabled" && type === "body") ||
        (!expandable && size === "medium" && state === "hover") ||
        (!expandable && size === "small" && state === "hover") ||
        (expandable && !expanded && selection === "checked" && size === "extra-large" && state === "hover") ||
        (expandable && !expanded && selection === "checked" && size === "large" && state === "hover") ||
        (expandable && !expanded && selection === "checked" && size === "medium" && state === "hover") ||
        (expandable && !expanded && selection === "none" && state === "hover") ||
        (expandable && !expanded && selection === "unchecked" && state === "enabled" && type === "body") ||
        (expandable && !expanded && selection === "unchecked" && state === "hover") ||
        (expandable && selection === "checked" && size === "small" && state === "hover") ||
        (!expanded && selection === "checked" && size === "extra-small" && state === "hover") ||
        (!expanded && selection === "checked" && state === "enabled" && type === "body") ||
        (!expanded && selection === "none" && state === "enabled" && type === "body") ||
        (selection === "selected" && size === "extra-large" && state === "hover") ||
        (selection === "selected" && size === "extra-small" && state === "hover") ||
        (selection === "selected" && size === "large" && state === "hover") ||
        (selection === "selected" && state === "enabled") ||
        (selection === "unselected" && size === "extra-large" && state === "hover") ||
        (selection === "unselected" && size === "extra-small" && state === "hover") ||
        (selection === "unselected" && size === "large" && state === "hover") ||
        (selection === "unselected" && state === "enabled" && type === "body")) && (
        <>
          <>
            {topBorder && (
              <div
                className={`divider-2 ${
                  (!expandable && selectable && size === "extra-small") ||
                  (!selectable && size === "extra-small") ||
                  size === "extra-large" ||
                  size === "large" ||
                  size === "medium" ||
                  size === "small"
                    ? dividerClassName
                    : undefined
                }`}
              />
            )}
          </>
        </>
      )}

      {!expandable && selection === "unchecked" && state === "hover" && size === "extra-large" && (
        <div className="data-table-row-2">
          <div className="checkbox-wrapper">
            <Checkbox3 className="instance-node-4" color="#161616" />
          </div>
          <DataTableRowCell
            cellText="Content"
            className="data-table-row-cell-item"
            minHeightClassName="data-table-row-cell-instance"
            resizerResizerClassName="col"
            size="extra-large"
            state="enabled"
          />
          <DataTableRowCell
            cellText="Content"
            className="data-table-row-cell-item"
            minHeightClassName="data-table-row-cell-item-instance"
            resizerResizerClassName="col"
            size="extra-large"
            state="enabled"
          />
          <DataTableRowCell
            cellText="Content"
            className="data-table-row-cell-item"
            minHeightClassName="col-3"
            resizerResizerClassName="col"
            size="extra-large"
            state="enabled"
          />
          <DataTableRowCell
            cellText="Content"
            className="data-table-row-cell-item"
            minHeightClassName="col-4"
            resizerResizerClassName="col"
            size="extra-large"
            state="enabled"
          />
          <DataTableRowCell
            cellText="Content"
            className="data-table-row-cell-item"
            minHeightClassName="col-5"
            resizerResizerClassName="col"
            size="extra-large"
            state="enabled"
          />
          <DataTableRowCell
            cellText="Content"
            className="data-table-row-cell-item"
            minHeightClassName="col-6"
            resizerResizerClassName="col"
            size="extra-large"
            state="enabled"
          />
          <DataTableRowCell
            cellText="Content"
            className="data-table-row-cell-item"
            minHeightClassName="col-7"
            resizerResizerClassName="col"
            size="extra-large"
            state="enabled"
          />
          <DataTableRowCell
            cellText="Content"
            className="data-table-row-cell-item"
            minHeightClassName="col-8"
            resizerResizerClassName="col"
            size="extra-large"
            state="enabled"
          />
        </div>
      )}

      {expanded && (
        <>
          <DataTableBodyRow
            border={
              state === "enabled" && !selectable && size === "medium"
                ? "/img/border-22.svg"
                : size === "medium" &&
                  ["checked", "unchecked"].includes(selection) &&
                  (selection === "checked" || state === "enabled")
                ? "/img/border-17.svg"
                : !selectable && state === "hover" && size === "medium"
                ? "/img/border-20.svg"
                : selection === "unchecked" && state === "hover" && size === "medium"
                ? "/img/border-19.svg"
                : size === "small" || (selectable && size === "extra-small")
                ? "/img/border.svg"
                : size === "extra-small" && !selectable
                ? "/img/border-8.svg"
                : undefined
            }
            cellText="Expandable table content"
            className="data-table-body-row-expanded-content-base"
            contentClassName={`${size === "extra-large" && selectable && "class-806"} ${
              size === "large" && selectable && "class-807"
            } ${size === "medium" && selectable && "class-808"} ${size === "small" && selectable && "class-809"} ${
              size === "extra-small" && selectable && "class-810"
            }`}
            descriptionClassName={`${
              ((!selectable && state === "enabled") ||
                (selection === "checked" && size === "extra-large" && state === "enabled") ||
                (selection === "checked" && size === "large" && state === "enabled") ||
                (selection === "unchecked" && state === "enabled")) &&
              "class-811"
            }`}
            minHeightClassName={`${size === "extra-large" && !selectable && state === "enabled" && "class-812"} ${
              size === "extra-large" && selection === "unchecked" && state === "enabled" && "class-813"
            } ${size === "extra-large" && selection === "checked" && state === "enabled" && "class-814"} ${
              !selectable && state === "hover" && size === "extra-large" && "class-815"
            } ${selection === "unchecked" && state === "hover" && size === "extra-large" && "class-816"} ${
              size === "extra-large" && state === "hover" && selection === "checked" && "class-817"
            } ${size === "large" && !selectable && state === "enabled" && "class-818"} ${
              size === "large" && selection === "unchecked" && state === "enabled" && "class-819"
            } ${size === "large" && selection === "checked" && state === "enabled" && "class-820"} ${
              !selectable && state === "hover" && size === "large" && "class-821"
            } ${selection === "unchecked" && state === "hover" && size === "large" && "class-822"} ${
              size === "large" && state === "hover" && selection === "checked" && "class-823"
            } ${state === "enabled" && !selectable && size === "medium" && "class-824"} ${
              selection === "unchecked" && size === "medium" && state === "enabled" && "class-825"
            } ${!selectable && state === "hover" && size === "medium" && "class-826"} ${
              selection === "unchecked" && state === "hover" && size === "medium" && "class-827"
            } ${selection === "checked" && size === "medium" && state === "enabled" && "class-828"} ${
              selection === "checked" && state === "hover" && size === "medium" && "class-829"
            } ${size === "small" && !selectable && state === "enabled" && "class-830"} ${
              selection === "unchecked" && size === "small" && state === "enabled" && "class-831"
            } ${!selectable && size === "small" && state === "hover" && "class-832"} ${
              selection === "unchecked" && size === "small" && state === "hover" && "class-833"
            } ${selectable && selection === "none" && state === "enabled" && "class-834"} ${
              selection === "none" && state === "hover" && selectable && "class-835"
            } ${size === "extra-small" && !selectable && state === "enabled" && "class-836"} ${
              size === "extra-small" && selection === "unchecked" && state === "enabled" && "class-837"
            } ${size === "extra-small" && !selectable && state === "hover" && "class-838"} ${
              size === "extra-small" && selection === "unchecked" && state === "hover" && "class-839"
            } ${size === "extra-small" && selection === "checked" && state === "enabled" && "class-840"} ${
              size === "extra-small" && state === "hover" && selection === "checked" && "class-841"
            }`}
            size={
              size === "extra-large"
                ? "extra-large"
                : size === "large"
                ? "large"
                : size === "medium"
                ? "medium"
                : size === "small"
                ? "small"
                : size === "extra-small"
                ? "extra-small"
                : undefined
            }
          />
          <>
            {topBorder && (
              <div
                className={`divider-3 ${
                  (selection === "checked" && size === "large" && state === "enabled") ||
                  (selection === "none" && size === "large" && state === "enabled") ||
                  (size === "extra-large" && state === "enabled") ||
                  (size === "extra-small" && state === "enabled") ||
                  (size === "medium" && state === "enabled") ||
                  (size === "small" && state === "enabled") ||
                  state === "hover"
                    ? dividerClassName
                    : undefined
                }`}
              />
            )}
          </>
        </>
      )}

      {type === "header" && !expandable && !selectable && (
        <>
          <>
            {visible1 && (
              <DataTableHeader
                cellText="Header"
                className="data-table-header-cell-item"
                resizerResizerClassName="col-2"
                size={
                  size === "extra-large"
                    ? "extra-large"
                    : size === "large"
                    ? "large"
                    : size === "medium"
                    ? "medium"
                    : size === "small"
                    ? "small"
                    : size === "extra-small"
                    ? "extra-small"
                    : undefined
                }
                sortable={!sortable ? false : sortable ? true : undefined}
                sorted="none"
                stateProp="enabled"
              />
            )}
          </>
        </>
      )}
    </div>
  );
};

DataTableRowItem.propTypes = {
  topBorder: PropTypes.bool,
  zebraStyle: PropTypes.bool,
  type: PropTypes.oneOf(["body", "header"]),
  size: PropTypes.oneOf(["large", "extra-large", "extra-small", "small", "medium"]),
  state: PropTypes.oneOf(["hover", "enabled"]),
  selectable: PropTypes.bool,
  selectType: PropTypes.oneOf(["none", "checkbox", "radio-button"]),
  selection: PropTypes.oneOf(["none", "indeterminate", "unselected", "selected", "unchecked", "checked"]),
  expandable: PropTypes.bool,
  expanded: PropTypes.bool,
  sortable: PropTypes.bool,
  dataTableRowCellCellText: PropTypes.string,
  dataTableRowCellCellText1: PropTypes.string,
  dataTableRowCellCellText2: PropTypes.string,
  dataTableRowCellCellText3: PropTypes.string,
  dataTableRowCellCellText4: PropTypes.string,
  dataTableRowCellCellText5: PropTypes.string,
  dataTableRowCellCellText6: PropTypes.string,
  visible: PropTypes.bool,
  dataTableHeaderCellText: PropTypes.string,
  dataTableHeaderCellText1: PropTypes.string,
  dataTableHeaderCellText2: PropTypes.string,
  dataTableHeaderCellText3: PropTypes.string,
  dataTableHeaderCellText4: PropTypes.string,
  dataTableHeaderCellText5: PropTypes.string,
  dataTableHeaderCellText6: PropTypes.string,
  visible1: PropTypes.bool,
};
