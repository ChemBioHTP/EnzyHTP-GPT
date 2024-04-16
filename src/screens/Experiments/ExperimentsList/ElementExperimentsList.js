import React from "react";
import { useState, useEffect } from "react";
import { DataTableRowItem } from "../components/DataTableRowItem";
import { DataTableToolbar } from "../components/DataTableToolbar";
import { NavigationHeader } from "../components/NavigationHeader";
import { NavigationSideNav } from "../components/NavigationSideNav";
import { NewExperimentModal } from "../components/NewExperimentModal";
import chemistImage from "../../../assets/images/Experiments/group-11.png";
import { Search } from "../icons/Search";
import { IconSliders } from "../icons/IconSliders";
import { IconTrash2 } from "../icons/IconTrash2";
import "./style.css";

export const ElementExperimentsList = ({ sideVisible = true, experiments=[], createNewExp=()=>{}}) => {

  useEffect(() => {
    console.log(sideVisible.type);
    if (sideVisible == true) {
      console.log('1');
      document.body.style.setProperty('--list-left-distance', '214px');
    } else {
      console.log('2');
      document.body.style.setProperty('--list-left-distance', '0px');
    }

  }, [sideVisible]);

  const processExperimentResponse = (data) => {
    // Process the data here
    console.log(data);
  }

  const createNewExperiment=()=>{
    console.log("12345");
    createNewExp();
  }
  // Conditionally render loading page or datatable
  const renderContent = () => {
    if (experiments.length === 0) {
      return (
        <>
          <div className="frame-9">
            <div className="text-wrapper-5">No experiments yet</div>
            <p className="p">Once you create experiments, they will show up here</p>
          </div>
          <NewExperimentModal blank={true} className="new-experiment-modal-instance" onSaveClick={createNewExperiment}/>
          <img className="group" alt="Group" src={chemistImage} />
        </>
      );
    } else {
      return (
        <>
          <DataTableToolbar
            buttonButtonText="New experiment"
            buttonIcon={<IconTrash2 className="icon-instance-node-3" />}
            buttonIconClassName="data-table-toolbar-item"
            className="data-table-toolbar-instance"
            override={<IconSliders className="icon-instance-node-3" />}
            searchDefaultIcon={<Search className="icon-instance-node-3" />}
            size="XL-LG-MD"
            visible={false}
            onSaveClick={createNewExp}
          />
          <div className="overlap-group">  
          <DataTableRowItem
            className="data-table-row-item-instance"
            dataTableRowCellCellText="Name"
            dataTableRowCellCellText1="Type"
            dataTableRowCellCellText2="Status"
            dataTableRowCellCellText3="Description"
            dataTableRowCellCellText4="Metrics"
            dataTableRowCellCellText5="Date Created"
            dataTableRowCellCellText6="Date Updated"
            dataTableRowCellImg="min-height-30.svg"
            dataTableRowCellImgClassName="data-table-row-item-4"
            dataTableRowCellImgClassNameOverride="data-table-row-item-5"
            dataTableRowCellMinHeight="min-height-29.svg"
            dataTableRowCellMinHeight1="min-height-31.svg"
            dataTableRowCellMinHeight2="min-height-32.svg"
            dataTableRowCellMinHeight3="min-height-33.svg"
            dataTableRowCellMinHeight4="min-height-34.svg"
            dataTableRowCellMinHeight5="min-height-35.svg"
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
          {experiments.map((experiment, index) => (
            <DataTableRowItem
            key={index}
            className="data-table-row-item-9"
            dataTableHeaderCellText={experiment.name}
            dataTableHeaderCellText1={experiment.type}
            dataTableHeaderCellText2={experiment.status}
            dataTableHeaderCellText3={experiment.description}
            dataTableHeaderCellText4={experiment.metrics}
            dataTableHeaderCellText5={experiment.created_time}
            dataTableHeaderCellText6={experiment.updated_time}
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
          ))}
        </div>
      </>
      );
    }
  };


  return (
    <div className="element-experiments-list">
      <div className="div-wrapper">
        <div className="text-wrapper-4">All experiments</div>
      </div>
      {renderContent()}

    </div>
  );
};

export default ElementExperimentsList;
