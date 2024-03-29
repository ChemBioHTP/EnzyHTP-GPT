import React from "react";
import Chart from "react-apexcharts";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";

export const AminoAcidTable = ({ mutations }) => {
  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Number</TableCell>
            <TableCell>Pattern</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {mutations.map((mutation, i) => (
            <TableRow key={i + 1}>
              <TableCell>{i + 1}</TableCell>
              <TableCell>{mutation}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export const HeatMapChart = ({ data }) => {
  const options = {
    chart: {
      type: "heatmap",
    },
    dataLabels: {
      enabled: false,
    },
    colors: ["#008FFB"],
    xaxis: {
      categories: data.xCategories,
    },
    yaxis: {
      categories: data.yCategories,
    },
    tooltip: {
      enabled: true,
      style: {
        fontSize: "12px",
      },
    },
  };
  const aminoAcidHydrophobicityMap = {
    A: 0.42,
    R: -1.01,
    N: -0.77,
    D: -0.77,
    C: 0.49,
    Q: -0.73,
    E: -0.64,
    G: 0,
    H: -0.4,
    I: 1.38,
    L: 1.06,
    K: -1.23,
    M: 0.64,
    F: 1.19,
    P: 0.12,
    S: -0.04,
    T: 0.26,
    W: 0.81,
    Y: 0.26,
    V: 1.08,
  };
  // const mappedArray = arrayOfDictionaries.map(dictionary => {
  //   return Object.entries(dictionary).map(([key, value]) => `${key}: ${value}`);
  // });

  const convertedwtData = data.wtData.map((ele) => {
    return { x: ele.x, y: aminoAcidHydrophobicityMap[ele.y] };
  });
  const convertedmutData = data.mutData.map((ele) => {
    return { x: ele.x, y: aminoAcidHydrophobicityMap[ele.y] };
  });

  console.log(convertedmutData);

  const series = [
    {
      name: "WT",
      data: convertedwtData,
    },
    {
      name: "Mut",
      data: convertedmutData,
    },
  ];

  return (
    <div>
      <Chart options={options} series={series} type="heatmap" />
    </div>
  );
};
