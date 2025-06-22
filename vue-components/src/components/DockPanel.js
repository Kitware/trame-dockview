export default {
  props: ["params"],
  setup(props) {
    const templateName = props.params.params.templateName;
    return { templateName };
  },
  template: '<trame-template :templateName="templateName" />',
};
