### spring


Simple Pygame launcher for Linux and Windows.

Loads executables from `./games/`, relative to the executable.
i.e.:
```
- spring
  games/
  - game1/
    - game1.sh
  - game2/
    - game2.x86_64
  - game3/
    - game3
```

Looks for `.exe` files on Windows and any executable `.sh`, `.x86`, `.x86_64` file or executable files with no extension on Linux.

Builds with `pyinstaller`, build.sh included.
