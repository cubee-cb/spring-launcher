### spring launcher

A simple Pygame-based app launcher for Linux and Windows. Mostly intended to be used with Heroic Games Launcher for bundling multiple similar games into one entry. (for example, multiple versions, or executable mods)
Supports mouse and keyboard arrows + enter.

Loads executables from `./games/`, relative to the executable.
For example:
```
- spring
  games/
  - game1/
    - game1.sh or game1.exe
      icon.png
      name.txt
  - game2/
    - game2.x86_64 or game2.exe
      icon.png
      name.txt
  - game3/
    - game3 or game3.exe
      icon.png
      name.txt
```

Looks for `.exe` files on Windows, and any executable `.sh`, `.x86`, `.x86_64` file or executable files with no extension on Linux.

## Building

Build with `pyinstaller`, see [`build.sh`](build.sh) and [`build.bat`](build.bat).
