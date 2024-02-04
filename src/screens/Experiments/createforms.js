import React from "react";
import { Close } from "./Close";
import { CreateForms } from "./components/CreateForms";
import { DataTableRowItem } from "./DataTableRowItem";
import { DataTableToolbar } from "./DataTableToolbar";
import { ModalFooterItem } from "./ModalFooterItem";
import { NavigationHeader } from "./NavigationHeader";
import { NavigationSideNav } from "./NavigationSideNav";
import { Search } from "./Search";
import { Sliders } from "./Sliders";
import { Trash2 } from "./Trash2";
import "./style.css";

export const ElementExperiments = () => {
  return (
    <div className="element-experiments">
      <div className="overlap-group-wrapper" data-breakpoints-mode="max-max-plus-1584px-1784px">
        <div className="overlap-group-2">
          <NavigationHeader className="navigation-header-instance" />
          <NavigationSideNav className="navigation-side-nav-instance" version="version-4" />
          <NavigationSideNav className="navigation-side-nav-2" version="version-5" />
          <div className="frame-7">
            <div className="text-wrapper-4">All experiments</div>
          </div>
          <DataTableToolbar
            buttonButtonText="New experiment"
            buttonIcon={<Trash2 className="icon-instance-node-3" />}
            buttonIconClassName="data-table-toolbar-instance"
            className="data-table-toolbar-item"
            override={<Sliders className="icon-instance-node-3" />}
            searchDefaultIcon={<Search className="icon-instance-node-3" />}
            size="XL-LG-MD"
            visible={false}
          />
          <DataTableRowItem
            className="data-table-row-item-instance"
            dataTableRowCellCellText="Name"
            dataTableRowCellCellText1="Type"
            dataTableRowCellCellText2="Status"
            dataTableRowCellCellText3="Description"
            dataTableRowCellCellText4="Metrics"
            dataTableRowCellCellText5="Date Created"
            dataTableRowCellCellText6="Date Updated"
            dataTableRowCellImg="min-height-2.svg"
            dataTableRowCellImgClassName="data-table-row-item-4"
            dataTableRowCellImgClassNameOverride="data-table-row-item-5"
            dataTableRowCellMinHeight="image.svg"
            dataTableRowCellMinHeight1="min-height-3.svg"
            dataTableRowCellMinHeight2="min-height-4.svg"
            dataTableRowCellMinHeight3="min-height-5.svg"
            dataTableRowCellMinHeight4="min-height-6.svg"
            dataTableRowCellMinHeight5="min-height-7.svg"
            dataTableRowCellMinHeightClassName="data-table-row-item-2"
            dataTableRowCellMinHeightClassName1="data-table-row-item-6"
            dataTableRowCellMinHeightClassName2="data-table-row-item-7"
            dataTableRowCellMinHeightClassName3="data-table-row-item-8"
            dataTableRowCellMinHeightClassNameOverride="data-table-row-item-3"
            dividerClassName="data-table-row-item-9"
            expandable={false}
            expanded={false}
            selectType="none"
            selectable={false}
            selection="none"
            size="large"
            sortable={false}
            state="enabled"
            type="body"
            visible={false}
          />
          <div className="frame-8">
            <DataTableRowItem
              className="data-table-row-item-9"
              dataTableHeaderCellText="Name"
              dataTableHeaderCellText1="Type"
              dataTableHeaderCellText2="Status"
              dataTableHeaderCellText3="Description"
              dataTableHeaderCellText4="Metrics"
              dataTableHeaderCellText5="Date Created"
              dataTableHeaderCellText6="Date Updated"
              expandable={false}
              expanded={false}
              selectType="none"
              selectable={false}
              selection="none"
              size="large"
              sortable={false}
              state="enabled"
              type="header"
              visible1={false}
            />
            <DataTableRowItem
              className="data-table-row-item-10"
              dataTableRowCellCellText="Name"
              dataTableRowCellCellText1="Type"
              dataTableRowCellCellText2="Status"
              dataTableRowCellCellText3="Description"
              dataTableRowCellCellText4="Metrics"
              dataTableRowCellCellText5="Date Created"
              dataTableRowCellCellText6="Date Updated"
              dataTableRowCellImg="min-height-9.svg"
              dataTableRowCellImgClassName="data-table-row-item-13"
              dataTableRowCellImgClassNameOverride="data-table-row-item-14"
              dataTableRowCellMinHeight="min-height-8.svg"
              dataTableRowCellMinHeight1="min-height-10.svg"
              dataTableRowCellMinHeight2="min-height-11.svg"
              dataTableRowCellMinHeight3="min-height-12.svg"
              dataTableRowCellMinHeight4="min-height-13.svg"
              dataTableRowCellMinHeight5="min-height-14.svg"
              dataTableRowCellMinHeightClassName="data-table-row-item-11"
              dataTableRowCellMinHeightClassName1="data-table-row-item-15"
              dataTableRowCellMinHeightClassName2="data-table-row-item-16"
              dataTableRowCellMinHeightClassName3="data-table-row-item-17"
              dataTableRowCellMinHeightClassNameOverride="data-table-row-item-12"
              dividerClassName="data-table-row-item-9"
              expandable={false}
              expanded={false}
              selectType="none"
              selectable={false}
              selection="none"
              size="large"
              sortable={false}
              state="enabled"
              type="body"
              visible={false}
            />
            <DataTableRowItem
              className="data-table-row-item-10"
              dataTableRowCellCellText="Name"
              dataTableRowCellCellText1="Type"
              dataTableRowCellCellText2="Status"
              dataTableRowCellCellText3="Description"
              dataTableRowCellCellText4="Metrics"
              dataTableRowCellCellText5="Date Created"
              dataTableRowCellCellText6="Date Updated"
              dataTableRowCellImg="min-height-16.svg"
              dataTableRowCellImgClassName="data-table-row-item-20"
              dataTableRowCellImgClassNameOverride="data-table-row-item-21"
              dataTableRowCellMinHeight="min-height-15.svg"
              dataTableRowCellMinHeight1="min-height-17.svg"
              dataTableRowCellMinHeight2="min-height-18.svg"
              dataTableRowCellMinHeight3="min-height-19.svg"
              dataTableRowCellMinHeight4="min-height-20.svg"
              dataTableRowCellMinHeight5="min-height-21.svg"
              dataTableRowCellMinHeightClassName="data-table-row-item-18"
              dataTableRowCellMinHeightClassName1="data-table-row-item-22"
              dataTableRowCellMinHeightClassName2="data-table-row-item-23"
              dataTableRowCellMinHeightClassName3="data-table-row-item-24"
              dataTableRowCellMinHeightClassNameOverride="data-table-row-item-19"
              dividerClassName="data-table-row-item-9"
              expandable={false}
              expanded={false}
              selectType="none"
              selectable={false}
              selection="none"
              size="large"
              sortable={false}
              state="enabled"
              type="body"
              visible={false}
            />
            <DataTableRowItem
              className="data-table-row-item-10"
              dataTableRowCellCellText="Name"
              dataTableRowCellCellText1="Type"
              dataTableRowCellCellText2="Status"
              dataTableRowCellCellText3="Description"
              dataTableRowCellCellText4="Metrics"
              dataTableRowCellCellText5="Date Created"
              dataTableRowCellCellText6="Date Updated"
              dataTableRowCellImg="min-height-23.svg"
              dataTableRowCellImgClassName="data-table-row-item-27"
              dataTableRowCellImgClassNameOverride="data-table-row-item-28"
              dataTableRowCellMinHeight="min-height-22.svg"
              dataTableRowCellMinHeight1="min-height-24.svg"
              dataTableRowCellMinHeight2="min-height-25.svg"
              dataTableRowCellMinHeight3="min-height-26.svg"
              dataTableRowCellMinHeight4="min-height-27.svg"
              dataTableRowCellMinHeight5="min-height-28.svg"
              dataTableRowCellMinHeightClassName="data-table-row-item-25"
              dataTableRowCellMinHeightClassName1="data-table-row-item-29"
              dataTableRowCellMinHeightClassName2="data-table-row-item-30"
              dataTableRowCellMinHeightClassName3="data-table-row-item-31"
              dataTableRowCellMinHeightClassNameOverride="data-table-row-item-26"
              dividerClassName="data-table-row-item-9"
              expandable={false}
              expanded={false}
              selectType="none"
              selectable={false}
              selection="none"
              size="large"
              sortable={false}
              state="enabled"
              type="body"
              visible={false}
            />
            <DataTableRowItem
              className="data-table-row-item-10"
              dataTableRowCellCellText="Name"
              dataTableRowCellCellText1="Type"
              dataTableRowCellCellText2="Status"
              dataTableRowCellCellText3="Description"
              dataTableRowCellCellText4="Metrics"
              dataTableRowCellCellText5="Date Created"
              dataTableRowCellCellText6="Date Updated"
              dataTableRowCellImg="min-height-30.svg"
              dataTableRowCellImgClassName="data-table-row-item-34"
              dataTableRowCellImgClassNameOverride="data-table-row-item-35"
              dataTableRowCellMinHeight="min-height-29.svg"
              dataTableRowCellMinHeight1="min-height-31.svg"
              dataTableRowCellMinHeight2="min-height-32.svg"
              dataTableRowCellMinHeight3="min-height-33.svg"
              dataTableRowCellMinHeight4="min-height-34.svg"
              dataTableRowCellMinHeight5="min-height-35.svg"
              dataTableRowCellMinHeightClassName="data-table-row-item-32"
              dataTableRowCellMinHeightClassName1="data-table-row-item-36"
              dataTableRowCellMinHeightClassName2="data-table-row-item-37"
              dataTableRowCellMinHeightClassName3="data-table-row-item-38"
              dataTableRowCellMinHeightClassNameOverride="data-table-row-item-33"
              dividerClassName="data-table-row-item-9"
              expandable={false}
              expanded={false}
              selectType="none"
              selectable={false}
              selection="none"
              size="large"
              sortable={false}
              state="enabled"
              type="body"
              visible={false}
            />
          </div>
          <div className="rectangle" />
          <div className="form-modal-default">
            <header className="header-2">
              <div className="label-title">
                <div className="text-wrapper-5">New experiment</div>
              </div>
              <Close className="close-instance" />
            </header>
            <div className="slot-wrapper">
              <div className="slot">
                <CreateForms
                  className="design-component-instance-node-3"
                  sizeMediumStateWrapperDeprecatedTextBackgroundClassName="create-forms-instance"
                  state="empty"
                />
              </div>
            </div>
            <ModalFooterItem
              actions="two"
              buttonButtonText="Cancel"
              buttonButtonText1="Create"
              buttonStateProp="disabled"
              cancel={false}
              className="design-component-instance-node-3"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
