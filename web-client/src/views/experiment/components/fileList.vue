<template>
	<a-flex justify="space-between">
		<div class="file-title">Downloadable files</div>
		<DownloadOutlined class="download-icon" :class="{ disabled: downloading }" @click="handleDownload" v-if="showDownload" />
	</a-flex>
	<a-row class="file-header">
		<a-col :span="16" class="file-name">Name</a-col>
		<a-col :span="8" class="file-format">Format</a-col>
	</a-row>
	<div class="file-list" v-if="list">
		<a-row v-for="(value, key) in list" class="item">
			<a-col :span="16" class="file-name">{{ key }}</a-col>
			<a-col :span="8" class="file-format">{{ value }}</a-col>
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
const downloading = ref(false);

const handleDownload = () => {
	if (downloading.value) {
		return;
	}
	const key = `download-${Date.now()}`;
	let lastPercent = -1;
	const updateMessage = content => {
		message.loading({ content, key, duration: 0 });
	};
	downloading.value = true;
	updateMessage("Downloading...");
	downloadable(route.query.id, {}, {
		onDownloadProgress: event => {
			if (!event.total) {
				return;
			}
			const percent = Math.round((event.loaded / event.total) * 100);
			if (percent !== lastPercent) {
				lastPercent = percent;
				updateMessage(`Downloading... ${percent}%`);
			}
		},
	})
		.then((res) => {
			downloadFile(res, "Downloadable-files.zip");
		})
		.finally(() => {
			message.destroy(key);
			downloading.value = false;
		});
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
.download-icon.disabled {
	cursor: not-allowed;
	opacity: 0.6;
	pointer-events: none;
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

.file-header .file-name {
	padding-right: 12px;
}

.file-header .file-format {
	padding-left: 12px;
}

.file-list {
	.item {
		background: #fff;
		border-top: 1px solid #dbdbdb;
		padding: 10px 16px;
		line-height: 20px;
	}

	.item > div {
		min-width: 0;
	}

	.file-name {
		padding-right: 12px;
		white-space: normal;
		word-break: break-word;
		overflow-wrap: anywhere;
	}

	.file-format {
		padding-left: 12px;
		white-space: normal;
		word-break: break-word;
	}
}
</style>
