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

from PIL import Image, ImageTk, ImageDraw, ImageFont

_ARROW_LINE_WIDTH = 3
_ARROW_LENGTH = 10  # pixel from arrow root to head
_ARROW_LENGTH_POW2 = _ARROW_LENGTH * _ARROW_LENGTH
_ARROW_RATE = 0.5 # root to point / root to head
"""
                root
                 |
------------------>|
                   |
                    head
"""

def _draw_background(width, height):
    background_color = (0, 0, 0, 0)
    image = Image.new(
        mode='RGBA',
        size=(width, height),
        color=background_color)
    return image


def _calculate_arrow_root(x_1, y_1, x_2, y_2):
    # calculate arrow root
    S = 1.0 * (y_2 - y_1) / (x_2 - x_1)  # Slope
    SS = S * S
    delta = math.sqrt(_ARROW_LENGTH_POW2 / (SS + 1))
    root_1 = x_2 + delta
    root_2 = x_2 - delta
    root_x = root_1
    if root_x < min(x_1, x_2) or root_x > max(x_1, x_2):
        root_x = root_2
    root_y = S * root_x - S * x_2 + y_2
    return root_x, root_y

def _calculate_arrow_foot(head_x, head_y, root_x, root_y):
    # calculate 2 foot points
    A = root_x - head_x
    AA = A * A
    B = root_y - head_y
    BB = B * B
    LL_RATED = _ARROW_RATE * _ARROW_RATE * _ARROW_LENGTH_POW2
    delta = math.sqrt(abs(LL_RATED - 1 - AA / BB))
    res_x_1 = root_x + delta
    res_y_1 = root_y + A / B * (head_x - res_x_1)
    res_x_2 = root_x - delta
    res_y_2 = root_y + A / B * (head_x - res_x_2)
    return res_x_1, res_y_1, res_x_2, res_y_2

def _calculate_arrow(x_1, y_1, x_2, y_2):
    current_length = (x_2 - x_1) * (x_2 - x_1) + (y_2 - y_1) * (y_2 - y_1)
    if current_length < _ARROW_LENGTH_POW2:
        return None, None, None, None

    if x_1 == x_2:
        heading = 1.0 if y_1 < y_2 else -1.0
        res_x_1 = x_2 - _ARROW_LENGTH * _ARROW_RATE
        res_y_1 = y_2 - _ARROW_LENGTH * heading
        res_x_2 = x_2 + _ARROW_LENGTH * _ARROW_RATE
        res_y_2 = y_2 - _ARROW_LENGTH * heading
        return int(res_x_1), int(res_y_1), int(res_x_2), int(res_y_2)
    if y_1 == y_2:
        heading = 1.0 if x_1 < x_2 else -1.0
        res_x_1 = x_2 - _ARROW_LENGTH * heading
        res_y_1 = y_2 - _ARROW_LENGTH * _ARROW_RATE
        res_x_2 = x_2 - _ARROW_LENGTH * heading
        res_y_2 = y_2 + _ARROW_LENGTH * _ARROW_RATE
        return int(res_x_1), int(res_y_1), int(res_x_2), int(res_y_2)

    root_x, root_y = _calculate_arrow_root(x_1, y_1, x_2, y_2)
    res_x_1, res_y_1, res_x_2, res_y_2 = _calculate_arrow_foot(x_2, y_2, root_x, root_y)
    # A = 1.0 * (x_1 - x_2)
    # AA =  A * A
    # B = 1.0 * (y_1 - y_2)
    # BB = B * B
    # C = math.cos(math.pi / 6.0)
    # CC = C * C
    # R = 6.0
    # RR = R * R
    # AA_BB = AA + BB
    # AABB = AA * BB
    # BBBB = BB * BB
    # D = CC * RR * AA_BB
    # DD = D * D
    # E = math.sqrt(abs(AABB * RR + BBBB * RR - BB * DD))
    # res = []
    # for i in [-1, 1]:
    #     for j in [-1, 1]:
    #         for k in [-1, 1]:
    #             t_x = (i * A * D + j * E) / AA_BB
    #             t_y = (k * D - A * t_x) / B
    #             if A * t_x + B * t_y > 0:
    #                 res.append([t_x+ x_2, t_y+ y_2])
    # print(res)
    # t_x_1 = (-1.0 * A * D + E) / AA_BB
    # t_y_1 = (-1.0 * D - A * t_x_1) / B
    # t_x_2 = (-1.0 * A * D + E) / AA_BB
    # t_y_2 = (-1.0 * D - A * t_x_2) / B
    # res_x_1 = t_x_1 + x_2
    # res_y_1 = t_y_1 + y_2
    # res_x_2 = t_x_2 + x_2
    # res_y_2 = t_y_2 + y_2
    # print(int(res_x_1), int(res_y_1), int(res_x_2), int(res_y_2))

    return int(res_x_1), int(res_y_1), int(res_x_2), int(res_y_2)


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
