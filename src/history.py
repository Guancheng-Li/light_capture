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

history stack for redo and undo.
"""

from PIL import ImageTk

class History:
    def __init__(self):
        self._stack = []
        self._current = self.top()
        self._image_tk = []

    def top(self):
        return len(self._stack) - 1

    def is_none(self):
        return self._current < 0

    def append(self, image):
        self._stack = self._stack[:self._current + 1]
        self._stack.append(image)
        self._current += 1

    def image(self):
        return self._stack[:self._current + 1]

    def image_tk(self):
        self._image_tk = []
        for i in range(self._current + 1):
            self._image_tk.append(ImageTk.PhotoImage(self._stack[i]))
        return self._image_tk
