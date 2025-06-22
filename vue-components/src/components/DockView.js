import "dockview-vue/dist/styles/dockview.css";
import { computed } from "vue";
import { DockviewVue } from "dockview-vue";
import DockPanel from "./DockPanel";

const THEMES_CLASSES = {
  Abyss: "dockview-theme-abyss",
  AbyssSpaced: "dockview-theme-abyss-spaced",
  Dark: "dockview-theme-dark",
  Dracula: "dockview-theme-dracula",
  Light: "dockview-theme-light",
  LightSpaced: "dockview-theme-light-spaced",
  Replit: "dockview-theme-replit",
  VisualStudio: "dockview-theme-vs",
};

export default {
  emits: ["ready"],
  props: {
    theme: {
      default: "Dracula",
    },
  },
  components: {
    DockviewVue,
    DockPanel,
  },
  setup(props, { emit }) {
    let api = null;
    const theme = computed(() => THEMES_CLASSES[props.theme]);

    function onReady(event) {
      api = event.api;
      emit("ready");
    }

    function addPanel(id, title, templateName, addOn = {}) {
      api.addPanel({
        id,
        title,
        component: "DockPanel",
        params: { templateName },
        ...addOn,
      });
    }

    return { theme, onReady, addPanel };
  },
  template:
    '<div style="position:relative;width:100%;height:100%;"><dockview-vue style="position:absolute;width:100%;height:100%" :className="theme" :class="theme" @ready="onReady" /></div>',
};
