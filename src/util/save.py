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

Save related functions.
"""

import os

IMAGE_PRE_FIX = 'LightCapture'
IMAGE_FORMAT = 'png'
IMAGE_QUALITY = 100
SAVE_PATH = './saved'


def get_image_file_name(time_str, format=IMAGE_FORMAT):
    return f'{IMAGE_PRE_FIX}_{time_str}.{format}'


def save_to_local(image, image_file_name, path=SAVE_PATH):
    os.makedirs(path, exist_ok=True)
    file_full_name = os.path.join(path, image_file_name)
    image.save(file_full_name, quality=IMAGE_QUALITY)
    return file_full_name
