#! python3
# -*- coding: utf-8 -*-
"""
@File   : image_service.py
@Created: 2025/04/15 22:38
@Author : Zhong, Yinjie
@Email  : yinjie.zhong@vanderbilt.edu
"""

from io import BytesIO
from PIL import Image
import base64

def read_image(path: str) -> Image.Image:
    """Read an image file from path.
    
    Args:
        path (str): Image filepath.

    Return:
        image (Image.Image): An PIL.Image.Image instance.
    """
    image = Image.open(path)
    return image

def encode_src_str(image: Image.Image) -> str:
    """Encode the Image instance to base64 encoded web image src content.
    
    Args:
        image (Image.Image): An PIL.Image.Image instance.

    Return:
        src_str (str): Encoded web image src content.
    """
    img_data = BytesIO()
    image.save(img_data, format="png")
    encoded_image = base64.b64encode(img_data.getvalue()).decode("utf-8")
    src_str = f"data:image/png;base64,{encoded_image}"
    return src_str

def image_path_to_src(path: str) -> str:
    """Convert an image filepath to web image src content.
    
    Args:
        path (str): Image filepath.

    Return:
        src_str (str): Encoded web image src content.
    """
    image = read_image(path=path)
    src_str = encode_src_str(image=image)
    return src_str
