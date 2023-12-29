import { DataTableRowItem } from ".";

export default {
  title: "Components/DataTableRowItem",
  component: DataTableRowItem,
  argTypes: {
    type: {
      options: ["body", "header"],
      control: { type: "select" },
    },
    size: {
      options: ["large", "extra-large", "extra-small", "small", "medium"],
      control: { type: "select" },
    },
    state: {
      options: ["hover", "enabled"],
      control: { type: "select" },
    },
    selectType: {
      options: ["none", "checkbox", "radio-button"],
      control: { type: "select" },
    },
    selection: {
      options: ["none", "indeterminate", "unselected", "selected", "unchecked", "checked"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    topBorder: true,
    zebraStyle: false,
    type: "body",
    size: "large",
    state: "hover",
    selectable: true,
    selectType: "none",
    selection: "none",
    expandable: true,
    expanded: true,
    sortable: true,
    className: {},
    dataTableRowCellMinHeightClassName: {},
    dataTableRowCellCellText: "Content",
    dataTableRowCellMinHeightClassNameOverride: {},
    dataTableRowCellCellText1: "Content",
    dataTableRowCellImgClassName: {},
    dataTableRowCellCellText2: "Content",
    dataTableRowCellImgClassNameOverride: {},
    dataTableRowCellCellText3: "Content",
    dataTableRowCellMinHeightClassName1: {},
    dataTableRowCellCellText4: "Content",
    dataTableRowCellMinHeightClassName2: {},
    dataTableRowCellCellText5: "Content",
    dataTableRowCellMinHeightClassName3: {},
    dataTableRowCellCellText6: "Content",
    visible: true,
    dividerClassName: {},
    dataTableHeaderCellText: "Header",
    dataTableHeaderCellText1: "Header",
    dataTableHeaderCellText2: "Header",
    dataTableHeaderCellText3: "Header",
    dataTableHeaderCellText4: "Header",
    dataTableHeaderCellText5: "Header",
    dataTableHeaderCellText6: "Header",
    visible1: true,
  },
};
