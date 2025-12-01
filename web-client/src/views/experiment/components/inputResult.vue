<template>
	<a-flex justify="start" class="row">
		<div @click="tableClick('Input')" :class="{ 'active': selected === 'Input' }">Input</div>
		<div @click="tableClick('Results')" :class="{ 'active': selected === 'Results' }">Results</div>
	</a-flex>
</template>
<script setup>
import { ref, reactive } from "vue"

const selected = defineModel({type: String, default: 'Input'})

const tableClick = (name) => {
	selected.value = name;
	console.log(selected.value);
}



</script>
<style lang="scss" scoped>
.row {
	margin: 15px 0 30px 30px;

	>div {
		position: relative;
		width: 160px;
		height: 60px;
		font-size: 14px;
		color: #525252;
		font-weight: 400;
		padding: 10px 15px;
		cursor: pointer;
		margin-left: 5px;
		border-bottom: 2px solid #C6C6C6;

		&.active {
			color: #161616;
			font-weight: 600;
			border-bottom: 2px solid #0F62FE;
		}
	}

}
</style>
