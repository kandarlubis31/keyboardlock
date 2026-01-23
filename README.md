# 🔒 Laptop Keyboard Manager

**Laptop Keyboard Manager** is a lightweight, aesthetic Windows utility designed to easily disable or enable the internal laptop keyboard driver. Ideally used when you want to place an external mechanical keyboard directly on top of your laptop's built-in keyboard without accidental key presses.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## ✨ Features

* **Eco-Futurism UI:** A modern, warm, and organic interface designed for visual comfort (Light Mode).
* **Kernel Level Control:** Disables the core `i8042prt` service (PS/2 Controller) for complete blocking.
* **Smart State Detection:** Automatically detects if the keyboard is currently Active or Disabled.
* **One-Click Action:** Toggles the driver state and initiates a system restart seamlessly.
* **Auto-Elevation:** Automatically requests Administrator privileges if not granted.
* **Portable:** Can be compiled into a single, standalone `.exe` file.

## ⚠️ Important Warnings

Before using this tool, please ensure you understand the following:

1.  **System Restart Required:** Changes to kernel drivers require a full system restart to take effect. The tool will force a restart immediately upon confirmation.
2.  **External Mouse Required:** On many laptops, the **Touchpad/Trackpad** shares the same PS/2 bus as the keyboard. Disabling the keyboard driver **may also disable your touchpad**. Ensure you have an external USB or Bluetooth mouse connected.
3.  **Authentication:** You might need to use an external keyboard or On-Screen Keyboard to type your password/PIN after the restart if the internal keyboard is disabled.

## 🛠️ How It Works

This tool modifies the Windows Registry Start value for the PS/2 service:

* **Registry Path:** `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\i8042prt`
* **Disable Logic:** Sets `Start` value to `4` (Disabled).
* **Enable Logic:** Sets `Start` value to `1` (System).

It utilizes the Windows Service Control (`sc config`) command to apply these changes safely.

## 🚀 Installation & Usage

### Option 1: Run from Source
1.  Ensure you have Python 3.x installed.
2.  Install dependencies (standard library only, but ensure `tkinter` is active).
3.  Run the script:
    ```bash
    python keyboard_manager.py
    ```

### Option 2: Run the Executable
1.  Download the latest `KeyboardManager.exe`.
2.  Right-click and **Run as Administrator** (or let the app ask for permission).
3.  Click the Action button to Toggle status.
4.  Accept the restart prompt.

## 📦 Building from Source (Compile to .exe)

To build a standalone executable that includes the custom icon:

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2.  Ensure `lock.ico` is in the same directory as the script.
3.  Run the build command:
    ```bash
    pyinstaller --noconsole --onefile --icon=lock.ico --add-data "lock.ico;." keyboard_manager.py
    ```
4.  The executable will be located in the `dist/` folder.

## 📝 License

This project is open-source and free to use. Use at your own risk. The developer is not responsible for any system instability caused by driver modification.

---
*Created with ❤️ for the mechanical keyboard community.*