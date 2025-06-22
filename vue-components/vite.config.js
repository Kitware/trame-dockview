export default {
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "trame_dockview",
      formats: ["umd"],
      fileName: "trame_dockview",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../src/trame_dockview/module/serve",
    assetsDir: ".",
  },
};
