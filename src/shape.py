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

Shapes for the editor.
Only provide the geometry description for the shape.
Not provide the drawing API.
"""

import math


class Rectangle():
    """For selection, rectangle, and oval."""
    def __init__(self, x_1=None, y_1=None, x_2=None, y_2=None):
        self._start_x = x_1
        self._start_y = y_1
        self._end_x = x_2
        self._end_y = y_2

    def is_none(self):
        return self._start_x is None or self._end_x is None

    def set_start(self, x, y):
        self._start_x = x
        self._start_y = y

    def set_end(self, x, y):
        self._end_x = x
        self._end_y = y

    def rectangle(self):
        min_x = min(self._start_x, self._end_x)
        min_y = min(self._start_y, self._end_y)
        max_x = max(self._start_x, self._end_x)
        max_y = max(self._start_y, self._end_y)
        return min_x, min_y, max_x, max_y

    def start_point(self):
        return self._start_x, self._start_y

    def end_point(self):
        return self._end_x, self._end_y

    def center(self):
        center_x = 0.5 * (self._start_x + self._end_x) 
        center_y = 0.5 * (self._start_y + self._end_y)
        return int(center_x), int(center_y)

    def inside(self, x, y, include_boarder=True):
        min_x, min_y, max_x, max_y = self.rectangle()
        if not include_boarder:
            return x > min_x and x < max_x and y > min_y and y < max_y
        return x >= min_x and x <= max_x and y >= min_y and y <= max_y


class Square():
    """For square, circle, and related types."""
    def __init__(self):
        self._start_x = None
        self._start_y = None
        self._end_x = None
        self._end_y = None

    def is_none(self):
        return self._start_x is None or self._end_x is None

    def set_start(self, x, y):
        self._start_x = x
        self._start_y = y

    def set_end(self, x, y):
        self._end_x = x
        self._end_y = y

    def square(self):
        delta_x = self._start_x - self._end_x
        delta_y = self._start_y - self._end_y
        radius = math.sqrt(delta_x * delta_x + delta_y * delta_y)
        min_x = self._start_x - radius
        min_y = self._start_y - radius
        max_x = self._start_x + radius
        max_y = self._start_y + radius
        return int(min_x), int(min_y), int(max_x), int(max_y)

    def center(self):
        return self._start_x, self._start_y


class Arrow():
    """For arrow shape."""
    pass
