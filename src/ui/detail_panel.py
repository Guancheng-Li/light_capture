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

Image utils.
"""
import os
import sys 

from PIL import Image, ImageTk, ImageDraw, ImageFont

sys.path.append('..') 
import shape
from state import State


DETAIL_PANEL_SIZE_RATIO = 0.2
DETAIL_RESIZE_RATIO = 0.5
# TODO: Move to other place.
OS_NAME = os.name
if OS_NAME == 'nt':
    FONT = 'arial.ttf'
elif OS_NAME == 'posix':
    FONT = '/usr/share/fonts/truetype/freefont/FreeMono.ttf'
FONT_SIZE = 20
# MAGIC NUMBER
MAGIC_BORDER_SIZE = 2  # To display full rectangle border.
MAGIC_RADIUS = 10  # For the cross circle.


class DetailPanel():
    """Detail panel to help selection"""
    def __init__(self, context):
        # constant
        self._full_snapshot = context.get('full_snapshot')
        # width
        self._screen_width = self._full_snapshot.width
        self._detail_width = int(DETAIL_PANEL_SIZE_RATIO * self._screen_width)
        self._detail_half_width = int(0.5 * self._detail_width)
        self._detail_crop_half_width = int(
            DETAIL_RESIZE_RATIO * self._detail_half_width)
        # height
        self._screen_height = self._full_snapshot.height
        self._detail_height = int(
            DETAIL_PANEL_SIZE_RATIO * self._screen_height)
        self._detail_half_height = int(0.5 * self._detail_height)
        self._detail_crop_half_height = int(
            DETAIL_RESIZE_RATIO * self._detail_half_height)
        self._state = None
        self._selected_area = None
        # mutable
        self._cursor_pos_x = context.get('cursor_pos_x')
        self._cursor_pos_y = context.get('cursor_pos_y')

    def _crop_and_resize_detail(self):
        """To get the cropped and resized image."""
        x_1 = self._cursor_pos_x - self._detail_crop_half_width
        y_1 = self._cursor_pos_y - self._detail_crop_half_height
        x_2 = self._cursor_pos_x + self._detail_crop_half_width
        y_2 = self._cursor_pos_y + self._detail_crop_half_height
        detail_image = Image.new(
            mode='RGBA',
            size=(self._detail_width, self._detail_height),
            color='white')
        pos_x, pos_y = 0, 0

        if x_1 < 0:
            pos_x = -2 * x_1
            x_1 = 0
        if y_1 < 0:
            pos_y = -2 * y_1
            y_1 = 0
        if x_2 > self._screen_width - 1:
            x_2 = self._screen_width - 1
        if y_2 > self._screen_height - 1:
            y_2 = self._screen_height - 1
        crop_image = None
        try:
            crop_image = self._full_snapshot.resize(
                (int((x_2 - x_1) / DETAIL_RESIZE_RATIO),
                    int((y_2 - y_1) / DETAIL_RESIZE_RATIO)),
                resample=Image.NEAREST,
                box=(x_1, y_1, x_2, y_2))
            detail_image.paste(crop_image, (pos_x, pos_y))
        except:
            print(f'x_1={x_1}, y_1={y_1}, x_2={x_2}, y_2={y_2}')
        return detail_image

    def _append_pos_text(self, image_draw):
        """Append pos text to the detail image."""
        font = ImageFont.truetype(font=FONT, size=FONT_SIZE)
        text = f'({self._cursor_pos_x}, {self._cursor_pos_y})'
        pos_x = self._detail_width - FONT_SIZE * len(text) / 2
        image_draw.text(
            xy=(pos_x, 5),
            text=text,
            fill=(255, 0, 0),
            font=font)

    def _append_rectangle(self, image_draw):
        """Append rectangle border to the detail image."""
        image_draw.rectangle(
            xy=(0, 0, self._detail_width - 1, self._detail_height - 1),
            fill=None,
            outline="red",
            width=1)

    def _append_cross(self, image_draw):
        """Append cross to the detail image."""
        image_draw.line(
            (
                self._detail_half_width,
                0,
                self._detail_half_width,
                self._detail_height,
            ),
            width=1,
            fill=(255, 0, 0))
        image_draw.line(
            (
                0,
                self._detail_half_height,
                self._detail_width,
                self._detail_half_height,
            ),
            width=1,
            fill=(255, 0, 0))
        image_draw.ellipse(
            (
                self._detail_half_width - MAGIC_RADIUS,
                self._detail_half_height - MAGIC_RADIUS,
                self._detail_half_width + MAGIC_RADIUS,
                self._detail_half_height + MAGIC_RADIUS,
            ),
            fill=None,
            outline=(255, 0, 0),
            width=1)

    def _get_display_pos(self):
        """Position to pasted detail."""
        pos_x, pos_y = MAGIC_BORDER_SIZE, MAGIC_BORDER_SIZE
        selected_start_x, selected_start_y = None, None
        if self._selected_area:
            selected_start_x, selected_start_y = self._selected_area.start_point()
        if self._cursor_pos_x < self._detail_width or (
            selected_start_x and selected_start_x < self._detail_width):
            pos_x = self._screen_width - MAGIC_BORDER_SIZE \
                - self._detail_width
        if self._cursor_pos_y < self._detail_height or (
            selected_start_y and selected_start_y < self._detail_height):
            pos_y = self._screen_height - MAGIC_BORDER_SIZE \
                - self._detail_height
        return pos_x, pos_y

    def _update_cursor(self, cursor_pos_x, cursor_pos_y):
        """To update the class variable"""
        self._cursor_pos_x = cursor_pos_x
        self._cursor_pos_y = cursor_pos_y

    def _create_background(self):
        """Half transparent background for unselected area."""
        background_color = (0, 0, 255, 25)
        self._selected_area_ready = self._selected_area and \
            not self._selected_area.is_none()
        self._need_to_append_selected_area = False
        if self._state == State.area_selecting or self._selected_area_ready:
            background_color = (0, 0, 255, 50)
            self._need_to_append_selected_area = True
        elif self._state == State.area_not_selected:
            background_color = (0, 0, 0, 0)
            self._need_to_append_selected_area = False
        else:
            print('Wrong state and area not ready')
            exit(1)
        image = Image.new(
            mode='RGBA',
            size=(self._screen_width, self._screen_height),
            color=background_color)
        return image

    def _refresh_detail_image(self):
        """Refresh the detail image."""
        display_pos_x, display_pos_y = self._get_display_pos()
        image = self._crop_and_resize_detail()
        image_draw = ImageDraw.Draw(image)
        self._append_pos_text(image_draw)
        self._append_rectangle(image_draw)
        self._append_cross(image_draw)
        return image, display_pos_x, display_pos_y

    def _append_cursor_cross(self, image_draw):
        """Append cursor cross to the full screen image."""
        image_draw.line(
            (
                self._cursor_pos_x,
                0,
                self._cursor_pos_x,
                self._screen_height,
            ),
            width=1,
            fill=(255, 0, 0))
        image_draw.line(
            (
                0,
                self._cursor_pos_y,
                self._screen_width,
                self._cursor_pos_y,
            ),
            width=1,
            fill=(255, 0, 0))

    def _append_selected_area(self, image_draw):
        """Append cursor cross to the full screen image."""
        if not self._need_to_append_selected_area:
            return
        x_1, y_1, x_2, y_2 = None, None, None, None
        rectangle = None
        width = 1
        if self._state == State.area_selecting:
            x_1, y_1 = self._selected_area.start_point()
            x_2, y_2 = self._cursor_pos_x, self._cursor_pos_y
            rectangle = (
                min(x_1, x_2),
                min(y_1, y_2),
                max(x_1, x_2),
                max(y_1, y_2),
            )
        else:
            rectangle = self._selected_area.rectangle()
            width = 2
        image_draw.rectangle(
            xy=rectangle,
            fill=(0, 0, 0, 0),
            outline="red",
            width=width)

    def _refresh_full_screen_image(self):
        """Refresh the full screen image."""
        image = self._create_background()
        image_draw = ImageDraw.Draw(image)
        if not self._selected_area_ready:
            detail_image, display_pos_x, display_pos_y = \
                self._refresh_detail_image()
            image.paste(detail_image, (display_pos_x, display_pos_y))
            self._append_cursor_cross(image_draw)
        self._append_selected_area(image_draw)
        return image

    def refresh(self, cursor_pos_x, cursor_pos_y, state, selected_area):
        """Refresh picture when cursor moved."""
        self._update_cursor(cursor_pos_x, cursor_pos_y)
        self._state = state
        self._selected_area = selected_area
        image = self._refresh_full_screen_image()
        return image
