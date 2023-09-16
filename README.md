# Light Capture
A light weight snapshot tool for Linux, just for fun.
![Alt text](example/01.png "Area selection")
![Alt text](example/02.png "Edit functions")

## Why
I am writing this because I need a snapshot tool like QQ embedded one.
Under linux, we have the following tools:
- gnome-screenshot
  - Pro: Installed by gnome interface linux.
  - Con: Terminal based, cannot draw something after capture.
- scrot
  - Pro: Many functions with commands, light-weight.
  - Con: The same as gnome-screenshot.
- [shutter](https://shutter-project.org/)
  - Pro: Rich function for edit, and the editor is not heavy like GIMP but has enough functions, I really like it.
  - Con: Official deb for Ubuntu not provided, apt source is blocked where I work, this tool needs extra dependencies if you want to use its editor.
    ```
    sudo add-apt-repository ppa:shutter/ppa
    sudo apt-get update #for Linux Mint only, this is done automatically on Ubuntu
    sudo apt install shutter
    # Fix eidtor
    curl -o FixShutterEdit.sh https://raw.githubusercontent.com/letsfoss/Fix-Disabled-Edit-Option-In-Shutter/master/FixShutterEdit.sh; chmod +x FixShutterEdit.sh; ./FixShutterEdit.sh
    ```
- [flameshot](https://flameshot.org/)
  - Pro: I think it is ideal tool.
  - Con: Depends on QT while the QT version does not match my development version, I don't want to take the risk to reinstall QT. (AppImage can solve it but the clipboard cannot work)

# Features
So I just need a easy tool with this features:
1. Little dependency
    xclip(for clipboard), Pillow(Python, need install), tkinter(Python installed by default)
2. Portable
    the dependency upon is available on most Linux systems.

# Functions
- [ ] move
- [x] rectangle
- [x] circle
- [x] arrow
- [ ] number
- [x] pencil
  - [ ] optimize the curve
- [x] pen
  - [ ] Fix the curve not connect problem
  - [ ] Support pen size edit
- [ ] text
- [x] blur (pen-mode, rectangle-mode)
  - [ ] Support pen mode
  - [ ] Support customize block size
- [x] eraser (pen-mode, rectangle-mode)
  - [ ] Support erase edit only
  - [ ] Support rectangle
  - [ ] Support pen size edit
- [x] undo
- [x] redo
- [ ] open
- [x] abort
- [x] save
- [x] clipboard
- [ ] edit top image (size change)
- [ ] put window always on top
- [ ] centralized configuration management
- [ ] use gnome-screenshot/scrot for snapshot and edit by this tool(use as merely front end)
- [ ] Optimize font settings(by using font family instead of font file)
- [ ] Sub Menus
  - [ ] Fill Color (RGBA) - rectangle,circle
  - [ ] Fill - rectangle,circle
  - [ ] Border Size - rectangle,circle
  - [ ] Border Color - rectangle,circle
  - [ ] Color - arrow, number, pencil, pen, text
  - [ ] Size - number, pencil, pen, text, blur, eraser
  - [ ] Font - text
- [ ] other functions ...

I am going to finish them with my trivial time out of work.

Welcome to provide good ideas but I will not promise accept and finish them.

Light & Portable is the rule, prefer to abandon some "useful" functions if they do not obey the rule.

# Bugs
1. Keyboard(ESC & Enter) does not work on Ubuntu(but work on Windows)
2. Windows clipboard support(Maybe never fix it because Windows doesn't need this tool)
