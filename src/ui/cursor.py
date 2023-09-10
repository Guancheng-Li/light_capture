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

Cursor related util.
"""

import sys

sys.path.append('..') 
from state import State


_DEFAULT_CURSOR = 'arrow'
_CURSOR_STATE_MAPPING = {
    State.area_not_selected: 'cross',
    State.area_selecting: 'cross',
    State.snapshot_edit: 'arrow',
}


def cursor_icon(state):
    return _CURSOR_STATE_MAPPING.get(state, _DEFAULT_CURSOR)
