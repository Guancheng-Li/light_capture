# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0 
(GPLv3.0, the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    https://www.gnu.org/licenses/gpl-3.0.en.html
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Copyright 2023.
Authors: guanchenglichina@qq.com (Guancheng Li)

Draw different things.
"""

import math
import sys

from PIL import Image, ImageTk, ImageDraw, ImageFont

sys.path.append('..') 
from state import State


_ARROW_LINE_WIDTH = 3


def _draw_background(width, height):
    background_color = (0, 0, 0, 0)
    image = Image.new(
        mode='RGBA',
        size=(width, height),
        color=background_color)
    return image


def draw_rectangle(width, height, info):
    image = _draw_background(width, height)
    image_draw = ImageDraw.Draw(image)

    border_width = 2
    border_color = 'red'
    x_1, y_1, x_2, y_2 = info['x_1'], info['y_1'], info['x_2'], info['y_2']
    rectangle = (
        min(x_1, x_2),
        min(y_1, y_2),
        max(x_1, x_2),
        max(y_1, y_2),
    )
    image_draw.rectangle(
        xy=rectangle,
        fill=(0, 0, 0, 0),
        outline=border_color,
        width=border_width)
    return image


def draw_circle(width, height, info):
    image = _draw_background(width, height)
    image_draw = ImageDraw.Draw(image)

    border_width = 2
    border_color = 'red'
    x_1, y_1, x_2, y_2 = info['x_1'], info['y_1'], info['x_2'], info['y_2']
    rectangle = (
        min(x_1, x_2),
        min(y_1, y_2),
        max(x_1, x_2),
        max(y_1, y_2),
    )
    image_draw.ellipse(
        rectangle,
        fill=(0, 0, 0, 0),
        outline=border_color,
        width=border_width)
    return image


def draw_arrow(width, height, info):
    image = _draw_background(width, height)
    image_draw = ImageDraw.Draw(image)

    line_width = _ARROW_LINE_WIDTH
    line_color = (255, 0, 0)  # red
    x_1, y_1, x_2, y_2 = info['x_1'], info['y_1'], info['x_2'], info['y_2']
    image_draw.line(
        (x_1, y_1, x_2, y_2),
        width=line_width,
        fill=line_color)

    # Now work out the arrow head
    # = it will be a triangle with one vertex at 2nd point.
    # - it will start at 95% of the length of the line
    # - it will extend 8 pixels either side of the line
    _HEAD_RATIO = 0.05
    _EXTEND_PIXEL = 8
    _HALF_EXTEND_PIXEL = 0.5 * _EXTEND_PIXEL
    # Calculate the x,y coordinates of the bottom of the arrow head triangle
    botton_x = _HEAD_RATIO * (x_1 - x_2) + x_2
    botton_y = _HEAD_RATIO * (y_1 - y_2) + y_2
    # Calculate the other two vertices of the triangle
    # Check if line is vertical
    if x_1 == x_2:
        vtx_1 = (botton_x - _HALF_EXTEND_PIXEL, botton_y)
        vtx_2 = (botton_x + _HALF_EXTEND_PIXEL, botton_y)
    # Check if line is horizontal
    elif y_1 == y_2:
        vtx_1 = (botton_x, botton_y + _HALF_EXTEND_PIXEL)
        vtx_2 = (botton_x, botton_y - _HALF_EXTEND_PIXEL)
    else:
        alpha = math.atan2(y_2 - y_1, x_2 - x_1) - 90 * math.pi / 180
        a = _EXTEND_PIXEL * math.cos(alpha)
        b = _EXTEND_PIXEL * math.sin(alpha)
        vtx_1 = (botton_x + a, botton_y + b)
        vtx_2 = (botton_x - a, botton_y - b)
    # Draw arrow head triangle
    image_draw.polygon([vtx_1, vtx_2, (x_2, y_2)], fill=line_color)

    return image


STATE_DRAW_MAPPING = {
    State.snapshot_edit_rectangle: draw_rectangle,
    State.snapshot_edit_circle: draw_circle,
    State.snapshot_edit_arrow: draw_arrow,
}
