#!/usr/bin/env python

"""Tests for the comfypsi_blur_mask node."""

import pytest
import torch
from src.node import comfypsi_blur_mask


@pytest.fixture
def blur_mask_node():
    """Fixture to create a comfypsi_blur_mask node instance."""
    return comfypsi_blur_mask()


def test_node_metadata(blur_mask_node):
    """Test the node's declared metadata."""
    assert blur_mask_node.RETURN_TYPES == ("MASK",)
    assert blur_mask_node.FUNCTION == "main"
    assert blur_mask_node.CATEGORY == "comfypsi/mask"

    required_inputs = blur_mask_node.INPUT_TYPES()["required"]
    assert "mask" in required_inputs
    assert required_inputs["mask"][0] == "MASK"
    assert "blur" in required_inputs
    assert required_inputs["blur"][0] == "FLOAT"
    assert required_inputs["blur"][1]["default"] == 5.0


def test_blur_main_logic(blur_mask_node):
    """Test the core blurring functionality."""
    # Create a simple mask: a 5x5 image with a 3x3 white square in the middle
    input_mask = torch.zeros((1, 5, 5), dtype=torch.float32)
    input_mask[:, 1:4, 1:4] = 1.0

    # Run the main function with a blur value
    output_tuple = blur_mask_node.main(mask=input_mask.clone(), blur=1.5)
    output_mask = output_tuple[0]

    # Assert basic properties of the output
    assert isinstance(output_tuple, tuple)
    assert output_mask.shape == input_mask.shape

    # The mask should have changed
    assert not torch.equal(output_mask, input_mask)

    # A key test: the corners (were 0) should now be > 0 due to the blur.
    # The exact center (was 1) should now be < 1.
    assert output_mask[0, 0, 0] > 0.0
    assert output_mask[0, 2, 2] < 1.0


def test_zero_blur_returns_original_mask(blur_mask_node):
    """Test the edge case where blur is 0. It should return the original mask."""
    input_mask = torch.rand((1, 10, 10), dtype=torch.float32)

    # Run the main function with blur=0
    output_tuple = blur_mask_node.main(mask=input_mask.clone(), blur=0.0)
    output_mask = output_tuple[0]

    # The output should be identical to the input
    assert torch.equal(output_mask, input_mask)


def test_negative_blur_returns_original_mask(blur_mask_node):
    """Test the edge case where blur is negative. It should also return the original mask."""
    input_mask = torch.rand((1, 10, 10), dtype=torch.float32)

    # Run the main function with a negative blur value
    output_tuple = blur_mask_node.main(mask=input_mask.clone(), blur=-5.0)
    output_mask = output_tuple[0]

    # The output should be identical to the input
    assert torch.equal(output_mask, input_mask)
