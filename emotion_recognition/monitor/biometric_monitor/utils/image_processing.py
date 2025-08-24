"""Image processing utilities for emotion recognition."""

import math
import numpy as np
from typing import Tuple


def normalize_coordinates(normalized_x: float, normalized_y: float, 
                         image_width: int, image_height: int) -> Tuple[int, int]:
    """Convert normalized coordinates to pixel coordinates."""
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px


def get_face_box(face_landmarks, width: int, height: int) -> Tuple[int, int, int, int]:
    """Extract bounding box coordinates from MediaPipe face landmarks."""
    idx_to_coords = {}
    
    for idx, landmark in enumerate(face_landmarks.landmark):
        landmark_px = normalize_coordinates(landmark.x, landmark.y, width, height)
        if landmark_px:
            idx_to_coords[idx] = landmark_px

    if not idx_to_coords:
        return 0, 0, width, height

    coords_array = np.array(list(idx_to_coords.values()))
    x_min = np.min(coords_array[:, 0])
    y_min = np.min(coords_array[:, 1])
    x_max = np.max(coords_array[:, 0])
    y_max = np.max(coords_array[:, 1])

    # Ensure coordinates are within image bounds
    start_x = max(0, x_min)
    start_y = max(0, y_min)
    end_x = min(width - 1, x_max)
    end_y = min(height - 1, y_max)
    
    return start_x, start_y, end_x, end_y


def expand_bbox(bbox: Tuple[int, int, int, int], 
                expansion_factor: float = 0.2,
                image_width: int = None, image_height: int = None) -> Tuple[int, int, int, int]:
    """Expand bounding box by a factor while keeping within image bounds."""
    start_x, start_y, end_x, end_y = bbox
    
    width = end_x - start_x
    height = end_y - start_y
    
    expand_x = int(width * expansion_factor / 2)
    expand_y = int(height * expansion_factor / 2)
    
    new_start_x = max(0, start_x - expand_x)
    new_start_y = max(0, start_y - expand_y)
    new_end_x = min(image_width - 1 if image_width else end_x + expand_x, end_x + expand_x)
    new_end_y = min(image_height - 1 if image_height else end_y + expand_y, end_y + expand_y)
    
    return new_start_x, new_start_y, new_end_x, new_end_y


def crop_face_region(image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Crop face region from image using bounding box."""
    start_x, start_y, end_x, end_y = bbox
    return image[start_y:end_y, start_x:end_x]


def pad_to_square(image: np.ndarray, target_size: int = 224) -> np.ndarray:
    """Pad image to square and resize to target size."""
    height, width = image.shape[:2]
    
    if height == width:
        return image
    
    # Determine padding
    if height > width:
        pad_width = (height - width) // 2
        padding = ((0, 0), (pad_width, height - width - pad_width))
    else:
        pad_height = (width - height) // 2
        padding = ((pad_height, width - height - pad_height), (0, 0))
    
    # Add channel dimension if needed
    if len(image.shape) == 3:
        padding = padding + ((0, 0),)
    
    padded_image = np.pad(image, padding, mode='constant', constant_values=0)
    
    return padded_image