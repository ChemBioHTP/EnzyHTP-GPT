<template>
  <div class="main">
    <Header />
    <a-flex class="layout">
      <Side />
      <div class="main-content">
        <router-view />
      </div>
    </a-flex>
  </div>
</template>
<script setup>
import Header from "./header.vue"
import Side from "./side.vue"
</script>
<style scoped lang="scss">
.main {
  height: 100vh;
  width: 100vw;
  overflow: hidden;

  .layout {
    width: 100%;
    height: calc(100% - 48px);
    background: #f4f4f4;

    .main-content {
      width: calc(100% - 262px);
      height: 100%;
    }
  }
}
</style>
