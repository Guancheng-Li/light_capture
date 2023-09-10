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

Snapshot utils for this tool.
Support customize the snapshot tool, by default use ImageGrab.
Also support third party such as gnome-snapshot and scrot.
"""

from PIL import ImageGrab


# TODO: If use third party snapshot, do not import PIL.
def _image_grab_capture(x, y):
    """Full screen capture."""
    return ImageGrab.grab([0, 0, x, y])


def snapshot(x, y):
    return _image_grab_capture(x, y)
