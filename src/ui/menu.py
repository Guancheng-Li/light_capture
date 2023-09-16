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

Menu for the window.
"""

import sys

from PIL import Image, ImageTk
import tkinter as tk

sys.path.append('..') 
from image.loader import load_all_icon
import shape
from state import State, EDIT_READY_STATE, FUNCTIONAL_STATE

_FUNCTIONS = [
    # 'move',
    'rectangle',
    'circle',
    'arrow',
    # 'number',
    'pencil',
    'pen',
    # 'text',
    'blur',
    'eraser',
    'undo',
    'redo',
    # 'open',
    'abort',
    'save',
    'clipboard',
]

_FUNCTION_PROPERTY_MAPPING = {
    'move': {},
    'rectangle': {
        'icon': 'rectangle',
        'clicked': True,
    },
    'circle': {
        'icon': 'circle',
        'clicked': True,
    },
    'arrow': {
        'icon': 'arrow',
        'clicked': True,
    },
    'number': {},
    'pencil': {
        'icon': 'pencil',
        'clicked': True,
    },
    'pen': {
        'icon': 'pen',
        'clicked': True,
    },
    'text': {},
    'blur': {
        'icon': 'blur',
        'clicked': True,
    },
    'eraser': {
        'icon': 'eraser',
        'clicked': True,
    },
    'undo': {
        'icon': 'undo',
        'clicked': False,
    },
    'redo': {
        'icon': 'redo',
        'clicked': False,
    },
    'open': {},
    'abort': {
        'icon': 'close',
        'clicked': False,
    },
    'save': {
        'icon': 'save',
        'clicked': False,
    },
    'clipboard': {
        'icon': 'check',
        'clicked': False,
    },
}

_BUTTON_SPAN = 2
_MENU_SPAN = 2

class Menu:
    def __init__(self, root):
        # constant
        self._screen_width = root._screen_width
        self._screen_height = root._screen_height
        self._selected_area = root._selected_area.rectangle()
        self._icon_size = int(self._screen_width / 100)
        # placeholder
        self._menu_buttons = []
        # menu area
        self._area_width = len(_FUNCTIONS) * \
            (self._icon_size + _BUTTON_SPAN) - _BUTTON_SPAN
        self._area_height = self._icon_size
        # area pos
        self._init_area_pos()
        # button pos
        self._init_buttons_pos()
        # load icons
        self._init_icons()
        # intialize callbacks
        self._init_callbacks(root)

    def _init_area_pos(self):
        self._pos_method_x = 'e'
        self._pos_method_y = 'n'
        x_1, y_1, x_2, y_2 = self._selected_area
        if y_2 + self._area_height < self._screen_height:
            self._pos_method_y = 'n'
        elif y_1 - self._area_height > 0:
            self._pos_method_y = 's'
        if x_2 - self._area_width > 0:
            self._pos_method_x = 'e'
        elif x_1 + self._area_width < self._screen_width:
            self._pos_method_x = 'w'

    def _init_buttons_pos(self):
        """Calculate button nw pos."""
        x_1, y_1, x_2, y_2 = self._selected_area
        first_nw_pos_x = x_2 - self._area_width
        if self._pos_method_x == 'w':
            first_nw_pos_x = x_1
        nw_pos_y = y_2 + 4
        if self._pos_method_y == 's':
            nw_pos_y = y_1 - self._area_height - 4
        self._button_info = []

        last_x_ratio = 1.0 * first_nw_pos_x / self._screen_width
        span_ratio = 1.0 * _BUTTON_SPAN / self._screen_width
        step = 1.0 * self._icon_size / self._screen_width + span_ratio
        pos_y_ratio = 1.0 * nw_pos_y / self._screen_height
        for name in _FUNCTIONS:
            self._button_info.append({
                'name': name,
                'pos_x': last_x_ratio,
                'pos_y': pos_y_ratio,
                'property': _FUNCTION_PROPERTY_MAPPING[name],
            })
            last_x_ratio += step
        self.menu_nw_x = first_nw_pos_x
        self.menu_nw_y = nw_pos_y

    def _init_icons(self):
        all_icon = load_all_icon()
        self._all_icon = {}
        for name, raw_image in all_icon.items():
            self._all_icon[name] = ImageTk.PhotoImage(
                raw_image.resize((self._icon_size, self._icon_size)))

    def _init_callbacks(self, root):
        self._menu_callbacks = {
            # 'move',
            'rectangle': lambda:self._onclick_rectangle(root),
            'circle': lambda:self._onclick_circle(root),
            'arrow': lambda:self._onclick_arrow(root),
            # 'number',
            'pencil': lambda:self._onclick_pencil(root),
            'pen': lambda:self._onclick_pen(root),
            # 'text',
            'blur': lambda:self._onclick_blur(root),
            'eraser': lambda:self._onclick_eraser(root),
            'undo': lambda:root._undo(None),
            'redo': lambda:root._redo(None),
            # 'open',
            'abort': lambda:root._exit(None),
            'save': lambda:root._exit_and_save_to_file(None),
            'clipboard': lambda:root._exit_and_save_to_clipboard(None),
        }

    def _onclick_rectangle(self, root):
        root._update_state(State.snapshot_edit_rectangle)
        self._update_icons(root)
        # Show sub panel

    def _onclick_circle(self, root):
        root._update_state(State.snapshot_edit_circle)
        self._update_icons(root)
        # Show sub panel

    def _onclick_arrow(self, root):
        root._update_state(State.snapshot_edit_arrow)
        self._update_icons(root)
        # Show sub panel

    def _onclick_pencil(self, root):
        root._update_state(State.snapshot_edit_pencil)
        self._update_icons(root)
        # Show sub panel

    def _onclick_pen(self, root):
        root._update_state(State.snapshot_edit_pen)
        self._update_icons(root)
        # Show sub panel

    def _onclick_eraser(self, root):
        root._update_state(State.snapshot_edit_eraser)
        self._update_icons(root)
        # Show sub panel

    def _onclick_blur(self, root):
        root._update_state(State.snapshot_edit_blur)
        self._update_icons(root)
        # Show sub panel

    def _update_icons(self, root):
        if root._state not in EDIT_READY_STATE:
            return
        for i, info in enumerate(self._button_info):
            if info['name'] == root._state.name.split('_')[-1]:
                self._menu_buttons[i]['image'] = self._all_icon[f'{info["property"]["icon"]}_clicked']
            else:
                self._menu_buttons[i]['image'] = self._all_icon[info['property']['icon']]

    def inside(self, x, y, menu_span=_MENU_SPAN):
        return shape.Rectangle(
            self.menu_nw_x - menu_span,
            self.menu_nw_y - menu_span,
            self.menu_nw_x + self._area_width + menu_span,
            self.menu_nw_y + self._icon_size + menu_span,
        ).inside(x, y)

    def show(self, root):
        # create
        if not self._menu_buttons:
            for i, info in enumerate(self._button_info):
                self._menu_buttons.append(tk.Button(
                    root._root,
                    image=self._all_icon[info['property']['icon']],
                    bd=0,
                    command=self._menu_callbacks[info['name']],
                ))
        # update
        for i, button in enumerate(self._menu_buttons):
            button.place(
                relx=self._button_info[i]['pos_x'],
                rely=self._button_info[i]['pos_y'],
                anchor='nw')
            # disable undo/redo on demand.
            if self._button_info[i]['name'] == 'undo':
                state = tk.DISABLED if root._history.is_none() else tk.NORMAL
                button.config(state=state)
            if self._button_info[i]['name'] == 'redo':
                state = tk.DISABLED if root._history.is_top() else tk.NORMAL
                button.config(state=state)
