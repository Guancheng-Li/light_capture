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
# from scipy import interpolate

sys.path.append('..') 
from state import State


_ARROW_LINE_WIDTH = 3
_BORDER_WIDTH = 2
_PENCIL_WIDTH = 2
_PEN_WIDTH = 50
_BLUR_TILE_SIZE = 10

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

    border_width = _BORDER_WIDTH
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

    border_width = _BORDER_WIDTH
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


def draw_pencil(width, height, info):
    image = _draw_background(width, height)
    image_draw = ImageDraw.Draw(image)

    border_width = _PENCIL_WIDTH
    line_color = (255, 0, 0)  # red
    points = info['points']
    for i in range(len(points) - 1):
        x_1, y_1 = points[i][0], points[i][1]
        x_2, y_2 = points[i + 1][0], points[i + 1][1]
        image_draw.line(
            (x_1, y_1, x_2, y_2),
            width=border_width,
            fill=line_color)

    return image


# def draw_pencil_interpolate(width, height, info):
#     # TODO: Fix it utill work well
#     image = _draw_background(width, height)
#     image_draw = ImageDraw.Draw(image)
#     border_width = _PENCIL_WIDTH
#     line_color = (255, 0, 0)  # red
#     points = info['points']
#     interpolate_method = 'linear'
#     for i in range(len(points) - 1):
#         x_1, y_1 = points[i][0], points[i][1]
#         x_2, y_2 = points[i + 1][0], points[i + 1][1]
#         if abs(x_2 - x_1) > 10:
#             x, y = [x_1, x_2], [y_1, y_2]
#             line_function = interpolate.interp1d(
#                 x, y, kind=interpolate_method)
#             for i in range(x[0], x[-1]):
#                 image_draw.line(
#                     (i, line_function(i), i + 1, line_function(i + 1)),
#                     width=border_width,
#                     fill=line_color)
#         else:
#             x_1, y_1 = points[i][0], points[i][1]
#             x_2, y_2 = points[i + 1][0], points[i + 1][1]
#             image_draw.line(
#                 (x_1, y_1, x_2, y_2),
#                 width=border_width,
#                 fill=line_color)
#     return image


def _draw_bold_lines(width, height, info, color):
    # TODO: Fix the curve not connect problem.
    image = _draw_background(width, height)
    image_draw = ImageDraw.Draw(image)

    border_width = _PEN_WIDTH
    color  # transparent red
    points = info['points']

    def _draw_pen_start_and_end(x, y):
        radius = int(border_width * 0.5)
        rectangle = (
            x - radius, y - radius,
            x + radius, y + radius,
        )
        image_draw.ellipse(
            rectangle,
            fill=color)

    _draw_pen_start_and_end(
        points[0][0], points[0][1])
    for i in range(len(points) - 1):
        x_1, y_1 = points[i][0], points[i][1]
        x_2, y_2 = points[i + 1][0], points[i + 1][1]
        image_draw.line(
            (x_1, y_1, x_2, y_2),
            width=border_width,
            fill=color)
    _draw_pen_start_and_end(
        points[-1][0], points[-1][1])

    return image

def draw_pen(width, height, info):
    color = (255, 0, 0, 128)  # transparent red
    return _draw_bold_lines(width, height, info, color)

def draw_eraser(width, height, info):
    color = (255, 255, 255)  # white
    return _draw_bold_lines(width, height, info, color)


def draw_blur(width, height, info):
    image = _draw_background(width, height)
    image_draw = ImageDraw.Draw(image)

    x_1, y_1, x_2, y_2 = info['x_1'], info['y_1'], info['x_2'], info['y_2']
    x_1, y_1, x_2, y_2 = \
        min(x_1, x_2), min(y_1, y_2), max(x_1, x_2), max(y_1, y_2),
    origin_image = info['snapshot']
    tile_size = _BLUR_TILE_SIZE
    for x_3 in range(x_1, x_2, tile_size):
        for y_3 in range(y_1, y_2, tile_size):
            x_4 = x_3 + tile_size
            if x_4 > x_2:
                x_4 = x_2
            y_4 = y_3 + tile_size
            if y_4 > y_2:
                y_4 = y_2
            box = (x_3, y_3, x_4, y_4)
            tile = origin_image.crop(box)
            r, g, b = tile.resize((1, 1)).getpixel((0, 0))
            color = (r, g, b)
            image_draw.rectangle(box, fill=color)

    return image


STATE_DRAW_MAPPING = {
    State.snapshot_edit_rectangle: draw_rectangle,
    State.snapshot_edit_circle: draw_circle,
    State.snapshot_edit_arrow: draw_arrow,
    State.snapshot_edit_pencil: draw_pencil,
    State.snapshot_edit_pen: draw_pen,
    State.snapshot_edit_eraser: draw_eraser,
    State.snapshot_edit_blur: draw_blur,
}
