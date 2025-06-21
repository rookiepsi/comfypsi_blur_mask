import torch
import torch.nn.functional as F


class comfypsi_blur_mask:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "blur": (
                    "FLOAT",
                    {"default": 5.0, "min": 0.0, "max": 100.0, "step": 0.1},
                ),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "main"
    CATEGORY = "comfypsi/mask"

    def main(self, mask: torch.Tensor, blur: float):
        if blur <= 0:
            return (mask,)

        _, height, width = mask.shape
        mask_clone = mask.clone()

        kernel_size = int(6 * blur)
        if kernel_size % 2 == 0:
            kernel_size += 1

        kernel_size = min(kernel_size, width - 1, height - 1)
        if kernel_size % 2 == 0:
            kernel_size += 1

        kernel_size = max(1, kernel_size)

        ax = torch.arange(-kernel_size // 2 + 1.0, kernel_size // 2 + 1.0)
        xx = torch.exp(-(ax**2) / (2.0 * blur**2))
        kernel_1d = (xx / torch.sum(xx)).to(mask_clone.device, dtype=mask_clone.dtype)

        mask_for_conv = mask_clone.unsqueeze(1)

        kernel_h = kernel_1d.view(1, 1, 1, kernel_size)
        padding_h = (0, kernel_size // 2)
        blurred_mask = F.conv2d(mask_for_conv, kernel_h, padding=padding_h, stride=1)

        kernel_v = kernel_1d.view(1, 1, kernel_size, 1)
        padding_v = (kernel_size // 2, 0)
        blurred_mask = F.conv2d(blurred_mask, kernel_v, padding=padding_v, stride=1)

        blurred_mask = blurred_mask.squeeze(1)

        return (blurred_mask,)


NODE_CLASS_MAPPINGS = {"comfypsi_blur_mask": comfypsi_blur_mask}
NODE_DISPLAY_NAME_MAPPINGS = {"comfypsi_blur_mask": "Blur Mask"}
