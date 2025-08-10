<script setup>
import { onMounted, ref, h, reactive, computed } from "vue";
import { PlusOutlined } from "@ant-design/icons-vue";
import ExperimentModal from "@/components/ExperimentModal.vue";
import { useExperimentStore } from "@/stores/experiment";
import { getExperimentList } from "@/api/experiment";
import { useRouter } from "vue-router";
import { CaretLeftOutlined, CaretRightOutlined } from "@ant-design/icons-vue";
// import Foot from "@/components/Foot.vue";

const experimentStore = useExperimentStore();
const router = useRouter();

const getExperiment = () => {
  spinning.value = true;
  getExperimentList()
    .then(res => {
      spinning.value = false;
      if (res.experiments) {
        params.total = res.experiments.length;
        experimentStore.setExperiments(res.experiments);
      }
    })
    .finally(() => {
      spinning.value = false;
    });
};

const params = reactive({
  page: 1,
  items: 7,
  total: 0,
});
const spinning = ref(false);

const open = ref(false);

const columns = ref([
  {
    title: "Name",
    dataIndex: "name",
    width: 250,
    sorter: {
      compare: (a, b) => a.name - b.name,
    },
  },
  // {
  //   title: "Type",
  //   dataIndex: "type",
  //   width: 80,
  // },
  {
    title: "Status",
    dataIndex: "status_text",
    minWidth: 100,
  },
  {
    title: "Description",
    dataIndex: "description",
    minWidth: 200,
  },
  {
    title: "Metrics",
    dataIndex: "metrics",
    customRender: ({ record }) => {
      return record.metrics?.map(item => item.name).join(", ");
    },
  },
  {
    title: "Date Created",
    dataIndex: "created_time",
    width: 250,
    sorter: {
      compare: (a, b) => {
        const timeA = new Date(a.created_time).getTime();
        const timeB = new Date(b.created_time).getTime();
        return timeB - timeA; // 降序排列,最新的在前
      },
    },
  },
  {
    title: "Date Updated",
    dataIndex: "updated_time",
    width: 250,
    sorter: {
      compare: (a, b) => {
        const timeA = new Date(a.updated_time).getTime();
        const timeB = new Date(b.updated_time).getTime();
        return timeB - timeA; // 降序排列,最新的在前
      },
    },
  },
]);

const sort = key => { };

onMounted(() => {
  getExperiment(params);
});

const handleCreate = () => {
  open.value = true;
};
// 自定义分页按钮渲染
const customItemRender = ({ page, type, originalElement }) => {
  if (type === "prev") {
    return h(CaretLeftOutlined, { class: "prev" });
  } else if (type === "next") {
    return h(CaretRightOutlined, { class: "next" });
  } else if (type === "page") {
    return h("a", {}, page);
  }
  return originalElement;
};

const handleTableChange = (pag, filters, sorter) => {
  // console.log(pag, filters, sorter, "-----------");
};

const handleRowClick = record => {
  return {
    onClick: () => {
      if (record._status == 0) {
        router.push({ path: "/result", query: { id: record.id, type: "Results", status: record._status } });
        return;
      }
      if (record._status <= -1 && record._status >= -8) {
        router.push({ path: "/result", query: { id: record.id, type: "Results", status: record._status } });
        return;
      }
      if (record._status == -9 || record._status > 0) {
        router.push({ path: "/setup", query: { id: record.id } });
      }
    },
  };
};

const tableData = computed(() => {
  let index = experimentStore.experimentType;
  switch (index) {
    case 0:
      return experimentStore.experiments;
    case 1:
      return experimentStore.experiments.filter(item => [-9, -8, -7, -6, -5, -4, -3, -2, -1].includes(item._status));
    case 2:
      return experimentStore.experiments.filter(item => [1, 2, 3].includes(item._status));
    case 3:
      return experimentStore.experiments.filter(item => item._status === 0);
    default:
      return experimentStore.experiments;
  }
});
</script>

<template>
  <a-spin :spinning="spinning">
    <!-- empty state -->
    <div class="empty-state" v-if="experimentStore.experiments.length === 0 && spinning === false">
      <div class="title">All experiments</div>
      <div class="content">
        <img src="@/assets/img/no-experiments.png" class="no-experiments" />
        <div class="subtitle">No experiments yet</div>
        <div class="description">
          Once you create experiments, they will show up here
        </div>

        <a-button type="primary" size="large" style="width: 186px; margin-top: 60px" @click="handleCreate">
          <a-flex class="button-content" justify="space-between" align="center">
            <span>New experiment</span>
            <PlusOutlined />
          </a-flex>
        </a-button>
      </div>
    </div>

    <a-flex class="container" v-else>
      <div class="box">
        <div class="title">All experiments</div>
        <a-flex class="toolbar" justify="end" align="center">
          <a-tooltip placement="bottom" title="Under Construction">
            <img src="@/assets/img/search.svg" class="icon" srcset="" />
          </a-tooltip>
          <a-tooltip placement="bottom" title="Under Construction">
            <img src="@/assets/img/del.svg" class="icon" srcset="" style="margin: 0 32px" />
          </a-tooltip>

          <a-dropdown placement="bottomRight" overlayClassName="more-dropdown" v-if="0">
            <img src="@/assets/img/more.svg" class="icon" srcset="" style="margin-right: 16px" />
            <template #overlay>
              <a-menu>
                <a-menu-item>
                  <a href="javascript:;" class="disabled">Sorted by</a>
                </a-menu-item>
                <a-menu-item>
                  <a href="javascript:;" @click="sort('name')">Name</a>
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item>
                  <a href="javascript:;" @click="sort('created_time')">Date created</a>
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item>
                  <a href="javascript:;" @click="sort('updated_time')">Date updated</a>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
          <a-button type="primary" size="large" style="width: 186px" @click="handleCreate">
            <a-flex class="button-content" justify="space-between" align="center">
              <span>New experiment</span>
              <PlusOutlined />
            </a-flex>
          </a-button>
        </a-flex>
        <a-table :loading="loading" :pagination="{
          position: ['bottomCenter'],
          itemRender: customItemRender,
          defaultPageSize: params.items,
          showSizeChanger: false,
          total: tableData.length,
        }" :customRow="handleRowClick" @change="handleTableChange" :dataSource="tableData" :columns="columns"
          class="table" />
        <!-- <Foot/> -->
      </div>
    </a-flex>
  </a-spin>

  <ExperimentModal v-model:open="open" />
</template>
<style lang="scss" scoped>
.container {
  width: 100%;
  height: 100%;

  .box {
    flex: 1;
    padding: 24px 32px;
    height: calc(100vh - 48px);
    position: relative;

    .title {
      font-size: 36px;
      font-weight: 300;
    }

    .toolbar {
      margin-top: 80px;
    }

    .table {
      width: 100%;
    }
  }
}

.empty-state {
  padding: 24px 32px;
  margin: 0 auto;
  text-align: center;

  .title {
    font-size: 36px;
    text-align: left;
  }

  .content {
    margin-top: 150px;

    .subtitle {
      font-size: 28px;
      margin-top: 30px;
    }

    .description {
      margin-top: 10px;
      font-size: 16px;
    }

    .no-experiments {
      width: 217px;
      height: 217px;
    }
  }
}
</style>
