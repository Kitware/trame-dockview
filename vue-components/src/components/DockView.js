import "dockview-vue/dist/styles/dockview.css";
import { computed, onBeforeUnmount } from "vue";
import { DockviewVue } from "dockview-vue";
import DockPanel from "./DockPanel";

const THEMES = {
  dark: {
    name: "dark",
    className: "dockview-theme-dark",
  },
  light: {
    name: "light",
    className: "dockview-theme-light",
  },
  visualstudio: {
    name: "visualStudio",
    className: "dockview-theme-vs",
  },
  abyss: {
    name: "abyss",
    className: "dockview-theme-abyss",
  },
  dracula: {
    name: "dracula",
    className: "dockview-theme-dracula",
  },
  replit: {
    name: "replit",
    className: "dockview-theme-replit",
    gap: 10,
  },
  abyssspaced: {
    name: "abyssSpaced",
    className: "dockview-theme-abyss-spaced",
    gap: 10,
    dndOverlayMounting: "absolute",
    dndPanelOverlay: "group",
  },
  lightspaced: {
    name: "lightSpaced",
    className: "dockview-theme-light-spaced",
    gap: 10,
    dndOverlayMounting: "absolute",
    dndPanelOverlay: "group",
  },
};

function templateToComponent(name) {
  const safeName = name
    .toLowerCase()
    .replaceAll("_", "-")
    .replaceAll("--", "-");
  return `trame-template-${safeName}`;
}

const PROP_NAMES = [
  "defaultRenderer",
  "disableAutoResizing",
  "disableDnd",
  "disableFloatingGroups",
  "disableTabsOverflowList",
  "dndEdges",
  "floatingGroupBounds",
  "hideBorders",
  "locked",
  "noPanelsOverlay",
  "popoutUrl",
  "scrollbars",
  "singleTabMode",
];

export default {
  emits: ["ready", "activePanel", "removePanel"],
  props: {
    theme: {
      default: "Dracula",
    },
    defaultRenderer: {
      default: "always",
      type: String,
    },
    disableAutoResizing: {
      default: false,
      type: Boolean,
    },
    disableDnd: {
      default: false,
      type: Boolean,
    },
    disableFloatingGroups: {
      default: false,
      type: Boolean,
    },
    disableTabsOverflowList: {
      default: false,
      type: Boolean,
    },
    dndEdges: {
      default: false,
      type: Boolean,
    },
    floatingGroupBounds: {}, // {minimumHeightWithinViewport, minimumWidthWithinViewport} | boundedWithinViewport
    hideBorders: {
      default: false,
      type: Boolean,
    },
    locked: {
      default: false,
      type: Boolean,
    },
    noPanelsOverlay: {
      default: "watermark", // watermark | emptyGroup
      type: String,
    },
    popoutUrl: {
      type: String,
    },
    scrollbars: {
      // custom | native
      type: String,
    },
    singleTabMode: {
      default: "default", // default | fullwidth
      type: String,
    },
    components: {
      default: () => ({
        defaultTabComponent: null,
        leftHeaderActionsComponent: null,
        prefixHeaderActionsComponent: null,
        rightHeaderActionsComponent: null,
        watermarkComponent: null,
      }),
    },
  },
  components: {
    DockviewVue,
    DockPanel,
  },
  setup(props, { emit }) {
    let api = null;
    const disposables = [];
    const theme = computed(() => THEMES[props.theme.toLowerCase()]);

    onBeforeUnmount(() => {
      while (disposables.length) {
        disposables.pop().dispose();
      }
    });

    function onReady(event) {
      api = event.api;

      // Listen to active panel to emit event
      disposables.push(
        api.onDidActivePanelChange((e) => {
          emit("activePanel", e?.id);
        }),
      );
      disposables.push(
        api.onDidRemovePanel((e) => {
          console.log("onDidRemovePanel", e);
          emit("removePanel", e?.id);
        }),
      );

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
    // v-bind
    const bind = computed(() => {
      const dockViewProps = {};
      Object.entries(props.components).forEach(([k, v]) => {
        if (v) {
          dockViewProps[k] = templateToComponent(v);
        }
      });

      PROP_NAMES.forEach((key) => {
        if (props[key]) {
          dockViewProps[key] = props[key];
        }
      });

      return dockViewProps;
    });

    function removePanel(panelId) {
      api.getPanel(panelId)?.api?.close();
    }

    function activePanel(panelId) {
      api.getPanel(panelId)?.api?.setActive();
    }

    return {
      theme,
      onReady,
      addPanel,
      bind,
      removePanel,
      activePanel,
    };
  },
  template:
    '<div style="position:relative;width:100%;height:100%;"><dockview-vue style="position:absolute;width:100%;height:100%" :theme="theme" @ready="onReady" /></div>',
};
