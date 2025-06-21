import { app } from "../../../scripts/app.js";

app.registerExtension({
  name: "comfypsi.blur.mask",

  async beforeRegisterNodeDef(nodeType) {
    const onNodeCreated = nodeType.prototype.onNodeCreated;

    nodeType.prototype.onNodeCreated = function () {
      onNodeCreated?.apply(this, arguments);

      if (nodeType.comfyClass == "comfypsi_blur_mask") {
        this.size[0] = 225;
      }
    };
  },
});
