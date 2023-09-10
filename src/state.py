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

State machine for this window.
"""

from enum import Enum


class State(Enum):
    area_not_selected = 1
    area_selecting = 2
    snapshot_edit = 3
    snapshot_edit_rectangle = 11
    snapshot_edit_arrow = 12

FUNCTIONAL_STATE = (
    State.snapshot_edit_rectangle,
    State.snapshot_edit_arrow,
)

EDIT_READY_STATE = (
    State.snapshot_edit,
    State.snapshot_edit_rectangle,
    State.snapshot_edit_arrow,
)

def next_state(current_state):
    return None

def try_jump_state(from_state, to_state):
    if to_state in FUNCTIONAL_STATE:
        if from_state in EDIT_READY_STATE:
            if from_state == to_state:
                return State.snapshot_edit
            else:
                return to_state
    return from_state
