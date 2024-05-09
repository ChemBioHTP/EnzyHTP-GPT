import { DataTable } from ".";

export default {
  title: "Components/DataTable",
  component: DataTable,
};

export const Default = {
  args: {
    headerData:["header1, header2"],
    cellData:[["cell1", "cell2"],["cell1", "cell2"]],
    className: {},
  },
};
