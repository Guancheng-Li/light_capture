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

Utils for Microsoft Windows.
"""

def get_screen_size():
    # import ctypes
    # ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # #调用api获得当前的缩放因子
    # ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # #设置缩放因子
    # self._root.tk.call('tk', 'scaling', ScaleFactor/1000)
    # user32 = ctypes.windll.user32
    # #单显示器屏幕宽度和高度:
    # screen_size0 = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    # print(screen_size0)
    return None, None


def save_image_to_clipboard():
    # if OS_NAME == 'nt':
    #     win32clipboard.OpenClipboard()
    #     win32clipboard.EmptyClipboard()
    #     with open(file_full_name, 'rb') as fp:
    #         win32clipboard.SetClipboardData(
    #             win32clipboard.RegisterClipboardFormat('image/png'),
    #             fp.read())
    #     win32clipboard.CloseClipboard()
    return None
