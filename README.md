# Laptop Keyboard Manager

A small Windows utility for disabling the built-in laptop keyboard so an external
keyboard can sit on top of it without triggering stray key presses. Useful when a
mechanical keyboard is placed directly over the laptop's own keys.

The internal keyboard is driven by the PS/2 driver `i8042prt`. This tool flips that
driver's start mode in the registry, then reboots so the change takes effect.

## How it works

| Step | Detail |
| :--- | :--- |
| Read state | `HKLM\SYSTEM\CurrentControlSet\Services\i8042prt` → `Start` (`4` means disabled) |
| Disable | `sc config i8042prt start= disabled` |
| Enable | `sc config i8042prt start= auto` |
| Reboot | `shutdown /r /t 0 /f` — runs immediately after the change |

The GUI is Tkinter, so the runtime has no third-party dependency. Administrator
rights are requested automatically through `ShellExecuteW(... "runas" ...)`.

## Requirements

- Windows
- Python 3 with Tkinter (bundled in the standard python.org installer)
- Administrator privileges — the app re-launches itself elevated

`requirements.txt` contains only PyInstaller, used to produce a standalone `.exe`.
It is not needed to run the script.

## Run

```bash
python keyboard_blocker_pro.py
```

## Build an executable (optional)

No build script ships with this repository. PyInstaller is listed in
`requirements.txt` because that is the intended path; a typical invocation is:

```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --icon lock.ico keyboard_blocker_pro.py
```

## Warning — read this before toggling

- **The touchpad is usually on the same PS/2 bus and may be disabled as well.**
 Keep an external USB or Bluetooth mouse connected.
- **The reboot is immediate** (`/t 0 /f`). Unsaved work is lost.
- If the keyboard *and* touchpad are both disabled with no external input attached,
 recovery requires another machine or a Windows recovery environment to set
 `i8042prt` back to `auto`. There is no built-in undo once the machine restarts.
- Registry and service edits require elevation; without it the app refuses to act.

---

## Bahasa Indonesia

**Laptop Keyboard Manager** adalah utilitas Windows kecil untuk menonaktifkan keyboard bawaan laptop, supaya keyboard eksternal bisa diletakkan di atasnya tanpa memicu ketikan liar. Berguna saat keyboard mekanikal dipasang tepat di atas tombol laptop.

---

## License

MIT — see [LICENSE](LICENSE).
