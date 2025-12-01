<script setup>
import { RouterView } from 'vue-router'
import { theme } from 'ant-design-vue';

</script>

<template>
  <a-config-provider :theme="{
    token: {
      borderRadius: 0,
      colorPrimary: '#0F62FE',
      controlHeightLG: 48
    },
  }">
    <RouterView :key="$route.fullPath" />
  </a-config-provider>
</template>

<style></style>
