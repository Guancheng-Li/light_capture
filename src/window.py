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

Window for this tool.
"""

import os
# import queue
# import threading
# import time
# import keyboard

from PIL import Image, ImageTk
import tkinter as tk

# Move to install.
OS_NAME = os.name
if OS_NAME == 'nt':
    import win32clipboard
elif OS_NAME == 'posix':
    print('Please install xclip')  # Test xclip
else:
    print(f'Not supported: {OS_NAME}')

import history
import posix_util
import shape
from state import State, try_jump_state
from ui.cursor import cursor_icon
from ui.detail_panel import DetailPanel
from ui.menu import Menu
from util import draw
from util import save
from util.snapshot import snapshot
from util.time import get_now_time_str


_GOLDEN_RATIO = 0.618


class Window():
    """Main window displaying the full-screen snapshot."""
    def __init__(self):
        """Constructor for the capture window."""
        # State initialize
        self._state = State.area_not_selected
        # Window initialize
        self._root = tk.Tk()
        self._menu = None
        self._init_basic()
        self._snapshot_time = get_now_time_str()
        self._full_snapshot = snapshot(self._screen_width, self._screen_height)
        self._full_snapshot_tk = ImageTk.PhotoImage(self._full_snapshot)
        self._init_root_key_bind()
        self._init_snapshot_on_canvas()
        self._init_canvas_key_bind()
        # Cursor initialization
        self._init_cursor()
        # Detail panel initialization
        self._detail_panel = None
        self._detail_image_tk = None
        # Selected area
        self._selected_area = shape.Rectangle()
        self._image_to_save = None
        # Edit history
        self._history = history.History()
        self._canvas_need_update = False
        self._editing_area = None
        self._editing_image = None
        self._editing_image_tk = None
        self._editing = False

        # Test initialize
        self._test_init()
        self._menu = None

    def _init_basic(self):
        """Basic property initialization."""
        self._screen_height = self._root.winfo_screenheight()
        self._screen_width = self._root.winfo_screenwidth()
        self._root.title('LightCapture')
        # Full screen: f'{width}x{height}+{pos_x}+{pos_y}'
        self._root.geometry(
            f'{self._screen_width}x{self._screen_height}+0+0')
        self._root.overrideredirect(True)  # Remove the window header
        # self._root.iconbitmap('image/icon.ico')
        # self._root.attributes('-alpha', 0.25)  # Half-transparent background

    def _init_root_key_bind(self):
        """Root key bind initialization."""
        # Keyboard
        self._root.bind('<KeyPress-Escape>', self._exit)
        self._root.bind(
            '<KeyPress-Return>', self._exit_and_save_to_clipboard)
        self._root.focus_set()
        print('binded key')
        # Mouse
        self._root.bind('<Motion>', self._cursor_move)
        self._root.bind('<Button-1>', self._left_key_down)
        self._root.bind(
            '<Double-Button-1>', self._double_left_key)
        self._root.bind('<ButtonRelease-1>', self._left_key_up)
        self._root.bind('<ButtonRelease-3>', self._right_key_up)

    def _init_snapshot_on_canvas(self):
        self._canvas = tk.Canvas(self._root)
        self._canvas.config(
            height=self._screen_height, width=self._screen_width)
        self._canvas.create_image(
            0, 0, anchor=tk.NW, image=self._full_snapshot_tk)
        self._canvas.pack()

    def _init_canvas_key_bind(self):
        """Canvas key bind initialization."""
        # # Keyboard
        # self._canvas.bind('<KeyPress-Escape>', lambda:self._exit(None))
        # self._canvas.bind(
        #     '<KeyPress-Return>', lambda:self._exit_and_save_to_clipboard(None))
        # self._canvas.focus_set()
        print('binded key')

    def _update_cursor(self, x, y):
        self._root.config(cursor=cursor_icon(self._state))
        self._cursor_pos_x = x
        self._cursor_pos_y = y

    def _init_cursor(self):
        self._update_cursor(
            self._root.winfo_pointerx() - self._root.winfo_rootx(),
            self._root.winfo_pointery() - self._root.winfo_rooty(),
        )

    def _create_detail_panel_on_demand(self):
        """Detail panel initialization."""
        if self._detail_panel is None:
            self._detail_panel = DetailPanel({
                'full_snapshot': self._full_snapshot,
                'cursor_pos_x': self._cursor_pos_x,
                'cursor_pos_y': self._cursor_pos_y,
            })

    def _test_init(self):
        print('test initialize')
        # self._root.wm_attributes('-topmost', 1)  # Top window
        #tk.wm_attributes('-alpha', 0.1)
        #tk.attributes('-alpha', 0)

    def _exit(self, event=None):
        """Do nothing and exit."""
        print('Exit and do nothing.')
        self._root.destroy()

    def _exit_and_save_to_clipboard(self, event):
        """Copy image to the clipboard, then exit."""
        self._image_to_save = self._render_image_to_save()
        filename = save.get_image_file_name(self._snapshot_time)
        file_full_name = None
        if OS_NAME == 'nt':
            file_full_name = save.save_to_local(self._image_to_save, filename)
        elif OS_NAME == 'posix':
            file_full_name = save.save_to_local(self._image_to_save, filename, '/tmp')
            posix_util.copy_to_clipboard(file_full_name)
        # load image from file_full_name and pass to clipboard.
        print('Saved to clipboard')
        self._root.destroy()

    def _exit_and_save_to_file(self, event):
        """Save image to local file, then exit."""
        self._image_to_save = self._render_image_to_save()
        filename = save.get_image_file_name(self._snapshot_time)
        file_full_name = save.save_to_local(self._image_to_save, filename)
        print(f'Saved at: {file_full_name}')
        self._root.destroy()

    def _cursor_move(self, event):
        self._update_cursor(event.x_root, event.y_root)
        if (
            self._state == State.area_not_selected
            or self._state == State.area_selecting
            or self._state == State.snapshot_edit # FIXIT: not efficient
        ):
            self._create_detail_panel_on_demand()
            detail_image = self._detail_panel.refresh(
                self._cursor_pos_x,
                self._cursor_pos_y,
                self._state,
                self._selected_area)
            self._detail_image_tk = ImageTk.PhotoImage(detail_image)
            self._canvas.create_image(
                (0, 0),
                anchor='nw',
                image=self._detail_image_tk,
                tag='selection_panel')
        if self._state == State.snapshot_edit_rectangle and self._editing:
            x_1, y_1 = self._editing_area.start_point()
            self._editing_image = draw.draw_rectangle(
                self._screen_width, self._screen_height,
                {
                    'x_1': x_1,
                    'y_1': y_1,
                    'x_2': self._cursor_pos_x,
                    'y_2': self._cursor_pos_y,
                })
            self._editing_image_tk = ImageTk.PhotoImage(self._editing_image)
            self._canvas.create_image(
                (0, 0),
                anchor='nw',
                image=self._editing_image_tk,
                tag='selection_panel')
        elif self._state == State.snapshot_edit_arrow and self._editing:
            x_1, y_1 = self._editing_area.start_point()
            self._editing_image = draw.draw_arrow(
                self._screen_width, self._screen_height,
                {
                    'x_1': x_1,
                    'y_1': y_1,
                    'x_2': self._cursor_pos_x,
                    'y_2': self._cursor_pos_y,
                })
            self._editing_image_tk = ImageTk.PhotoImage(self._editing_image)
            self._canvas.create_image(
                (0, 0),
                anchor='nw',
                image=self._editing_image_tk,
                tag='selection_panel')

    def _update_menu(self):
        if self._state == State.snapshot_edit:
            if self._menu is None:
                self._menu = Menu(self)
            else:
                self._menu.show(self)

    def _left_key_down(self, event):
        x, y = event.x_root, event.y_root
        if self._menu is not None:
            if self._menu.inside(x, y):
                return
        if self._state == State.area_not_selected:
            self._selected_area.set_start(x, y)
            self._state = State.area_selecting
        if self._state == State.snapshot_edit_rectangle and not self._editing:
            self._editing_area = shape.Rectangle()
            self._editing_area.set_start(x, y)
            self._editing = True
        if self._state == State.snapshot_edit_arrow and not self._editing:
            self._editing_area = shape.Rectangle()
            self._editing_area.set_start(x, y)
            self._editing = True

    def _left_key_up(self, event):
        x, y = event.x_root, event.y_root
        if self._state == State.area_selecting:
            self._selected_area.set_end(x, y)
            self._state = State.snapshot_edit
        if self._state == State.snapshot_edit_rectangle and self._editing:
            self._editing_area.set_end(x, y)
            x_1, y_1, x_2, y_2 = self._editing_area.rectangle()
            if abs(x_1 - x_2) < 5 or abs(y_1 - y_2) < 5:
                # print('Avoid double-click mis-match.')
                return
            image = draw.draw_rectangle(
                self._screen_width, self._screen_height,
                {
                    'x_1': x_1,
                    'y_1': y_1,
                    'x_2': x_2,
                    'y_2': y_2,
                })
            self._history.append(image)
            self._editing_image = None
            self._editing_image_tk = None
            self._editing = False
            self._canvas_need_update = True
        if self._state == State.snapshot_edit_arrow and self._editing:
            self._editing_area.set_end(x, y)
            x_1, y_1 = self._editing_area.start_point()
            x_2, y_2 = self._editing_area.end_point()
            if abs(x_1 - x_2) < 5 or abs(y_1 - y_2) < 5:
                # print('Avoid double-click mis-match.')
                return
            image = draw.draw_arrow(
                self._screen_width, self._screen_height,
                {
                    'x_1': x_1,
                    'y_1': y_1,
                    'x_2': x_2,
                    'y_2': y_2,
                })
            self._history.append(image)
            self._editing_image = None
            self._editing_image_tk = None
            self._editing = False
            self._canvas_need_update = True

    def _right_key_down(self, event):
        # move the menu
        pass

    def _right_key_up(self, event):
        x, y = event.x_root, event.y_root
        if self._menu is not None:
            if self._menu.inside(x, y):
                return
        self._exit(event)

    def _double_left_key(self, event):
        x, y = event.x_root, event.y_root
        if self._menu is not None:
            if self._menu.inside(x, y):
                return
        self._exit_and_save_to_clipboard(event)

    def _render_image_to_save(self):
        image = Image.new(
            mode='RGBA',
            size=(self._screen_width, self._screen_height),
            color='white')
        image.paste(self._full_snapshot, (0, 0))
        if not self._history.is_none():
            for item in self._history.image():
                image.paste(item, (0, 0), item)
        if not self._selected_area.is_none():
            image = image.crop(self._selected_area.rectangle())
        return image

    def _update_state(self, state):
        self._state = try_jump_state(self._state, state)

    def _update_canvas(self):
        if not self._canvas_need_update:
            return
        self._canvas.create_image(
            0, 0, anchor=tk.NW, image=self._full_snapshot_tk)
        if self._detail_image_tk:
            self._canvas.create_image(
                (0, 0),
                anchor='nw',
                image=self._detail_image_tk)
        if not self._history.is_none():
            self._history_image = self._history.image_tk()
            for item in self._history_image:
                self._canvas.create_image(
                    (0, 0),
                    anchor='nw',
                    image=item)
        self._canvas_need_update = False

    # def _check_esc_pressed(input_queue):
    #     while True:
    #         if keyboard.is_pressed('esc'):
    #             input_queue.put('esc')
    #         time.sleep(0.1) # seconds

    # def _keyboard_listen(self):
    #     # Create another thread that monitors the keyboard
    #     input_queue = queue.Queue()
    #     kb_input_thread = threading.Thread(target=self._check_esc_pressed, args=(input_queue,))
    #     kb_input_thread.daemon = True
    #     kb_input_thread.start()

    #     # Main logic loop
    #     run_active = True
    #     while True:
    #         if not input_queue.empty():
    #             if (run_active) and (input_queue.get() == 'esc'):
    #                 run_active = False
    #                 self._exit()
    #             if (run_active) and (input_queue.get() == 'enter'):
    #                 run_active = False
    #                 self._exit_and_save_to_clipboard()
    #         time.sleep(0.1)  # seconds

    def _update(self):
        # print(get_now_time_str())
        self._root.after(100, self._update)
        self._update_menu()
        self._update_canvas()
        self._root.focus_set()


    # Public
    def display(self):
        self._update()
        # main_loop_thread = threading.Thread(target=self._keyboard_listen)
        # main_loop_thread.daemon = True
        # main_loop_thread.start()
        self._root.mainloop()
