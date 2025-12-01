<template>
	<a-flex justify="space-between">
		<div class="file-title">Downloadable files</div>
		<DownloadOutlined class="download-icon" @click="handleDownload" v-if="showDownload" />
	</a-flex>
	<a-row class="file-header">
		<a-col :span="16">Name</a-col>
		<a-col :span="8">Format</a-col>
	</a-row>
	<div class="file-list" v-if="list">
		<a-row v-for="(value, key) in list" class="item">
			<a-col :span="16">{{ key }}</a-col>
			<a-col :span="8">{{ value }}</a-col>
		</a-row>
	</div>
</template>
<script setup>
import { ref, reactive } from "vue";
import { DownloadOutlined } from "@ant-design/icons-vue";
import { downloadFile } from "@/utils/common";
import { downloadable } from "@/api/experiment"
import { useRoute } from "vue-router";
import { message } from "ant-design-vue";
const props = defineProps({
	list: {
		type: Object,
		default: () => { },
	},
	showDownload: {
		type: Boolean,
		default: true,
	},
});

const route = useRoute();

const handleDownload = () => {
	message.success("Downloading");
	downloadable(route.query.id).then((res) => {
		downloadFile(res, "Downloadable-files.zip")
	})
};

</script>
<style lang="scss" scoped>
.file-title {
	color: #161616;
	font-size: 14px;
	font-weight: 600;
}

.download-icon {
	cursor: pointer;
	font-size: 16px;
}

.file-header {
	background: #e0e0e0;
	padding: 0 16px;
	margin-top: 20px;

	>div {
		color: #161616;
		font-size: 14px;
		font-weight: 600;
		line-height: 25px;
	}
}

.file-list {
	.item {
		background: #fff;
		border-top: 1px solid #dbdbdb;
		padding: 10px 16px;
		height: 50px;
		line-height: 30px;
	}
}
</style>