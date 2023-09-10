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

Test file.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


root = tk.Tk()


bt = tk.Button(root)
bt['text'] = '点我'
bt.pack()

def click_bt(e):
    messagebox.showinfo('message', 'helloworld')

def print1(e):
    print(1)

def print2(e):
    print(2)

def print3(e):
    print(3)

bt.bind('<ButtonRelease-1>', click_bt)

root.bind('<KeyPress-Escape>', print1)
root.bind('<Leave>', print2)
root.bind('<KeyPress-Return>', print3)

root.mainloop()

