import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";

// https://vite.dev/config/
export default defineConfig(({ mode, command }) => {
  return {
    plugins: [vue(), vueJsx()],
    css: {
      preprocessorOptions: {
        scss: {
          api: "modern",
          silenceDeprecations: ["import"],
        },
      },
    },
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    server: {
      port: 3000,
      open: false,
      host: true,
      proxy: {
        "/api": {
          target: "https://enzyhtp.app.vanderbilt.edu",
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, "/api"),
        },
      },
    },
    esbuild: {
      drop: ["console", "debugger"],
    }
  };
});
