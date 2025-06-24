"""Top-level package for comfypsi_blur_mask."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """psi"""
__email__ = "rookiepsi@gmail.com"
__version__ = "1.0.1"

from .src.node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"
