/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";
import "../../content/general.css"

export const DataTable = ({
  headerData=["header1, header2"],
  cellData = [["cell1", "cell2"],["cell1", "cell2"]],
  className,
}) => {

  return (
    <table class={`data-table ${className}`}>
      <thead>
        <tr>
        {headerData.map(head => (
          <th>{head}</th>
        ))}
        </tr>
      </thead>
      <tbody>
        {cellData.map((item, index) => (
          <tr key={index}>
            {item.map(cell => (
              <td>{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};


DataTable.propTypes = {
  headerData: PropTypes.array,
  cellData: PropTypes.array,
};
