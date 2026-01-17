import { fileURLToPath, URL } from "node:url";
import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";

// https://vite.dev/config/
export default defineConfig(({ mode, command }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const keepConsole = env.VITE_KEEP_CONSOLE === "true" || env.VITE_KEEP_CONSOLE === "1";
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
      drop: keepConsole ? ["debugger"] : ["console", "debugger"],
    }
  };
});
