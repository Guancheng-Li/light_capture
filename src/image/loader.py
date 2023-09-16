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

Image loader.
"""

from PIL import Image

_CLICKED_COLOR = 'red'

_ICON_MAPPING = {
    'arrow': 'arrow',
    'arrow_clicked': f'arrow_{_CLICKED_COLOR}',
    'check': 'check',
    'circle': 'circle',
    'circle_clicked':  f'circle_{_CLICKED_COLOR}',
    'cross': 'cross',
    'move': 'move',
    'move_clicked': f'move_{_CLICKED_COLOR}',
    'rectangle': 'rectangle',
    'rectangle_clicked': f'rectangle_{_CLICKED_COLOR}',
    'undo': 'undo',
    'redo': 'redo',
    'save': 'save',
}


def _generate_icon_path(id):
    return f'image/{id}.png'


def load_all_icon():
    result = {}
    for name, id in _ICON_MAPPING.items():
        filename = _generate_icon_path(id)
        result[name] = Image.open(filename)
    return result
