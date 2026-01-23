import sys
import ctypes
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import winreg
import os
import logging

# --- THEME: ECO-FUTURISM (Warm & Organic) ---
COLOR_BG = "#F9F7F2"          # Limestone
COLOR_PANEL = "#EBE5DE"       # Warm Beige
COLOR_TEXT_MAIN = "#4A4238"   # Deep Mocha
COLOR_TEXT_SEC = "#8C8174"    # Warm Grey

COLOR_ACCENT_DANGER = "#C06C54"  # Terracotta
COLOR_ACCENT_SAFE = "#7D9D75"    # Sage Green
COLOR_ACCENT_WARNING = "#A47864" # Mocha Mousse

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_STATUS = ("Segoe UI", 24, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_BTN = ("Segoe UI", 11, "bold")
FONT_SMALL = ("Segoe UI", 9)

SERVICE_NAME = "i8042prt"
REGISTRY_PATH = r"SYSTEM\CurrentControlSet\Services\i8042prt"

# --- SYSTEM UTILITIES ---

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def apply_theme_title_bar(root):
    """Force Windows Title Bar to Light Mode."""
    try:
        root.update()
        set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ctypes.windll.user32.GetParent
        hwnd = get_parent(root.winfo_id())
        value = ctypes.c_int(0) # 0 = Light Mode
        set_window_attribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
    except:
        pass

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")

def create_tooltip(widget, text):
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(tooltip, text=text, background="#4A4238", foreground="#F9F7F2",
                         relief="flat", borderwidth=0, font=FONT_SMALL, padx=5, pady=3)
        label.pack()
        widget.tooltip = tooltip

    def on_leave(event):
        if hasattr(widget, "tooltip"):
            widget.tooltip.destroy()
            del widget.tooltip

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

# --- MAIN APPLICATION ---

class KeyboardNukeLite:
    def __init__(self, root):
        self.root = root
        self.root.title("Laptop Keyboard Manager")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)
        
        # --- ICON SETUP (SMART PATH) ---
        icon_name = "lock.ico"
        icon_path = resource_path(icon_name)
        
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
                self.root.iconbitmap(default=icon_path) 
            except Exception as e:
                print(f"Icon Load Error: {e}")
        # -------------------------------

        self.root.geometry("520x600")
        center_window(self.root, 520, 600)
        apply_theme_title_bar(self.root)
        
        self.current_state = "UNKNOWN"
        self.setup_ui()
        self.update_status_display()

    def setup_ui(self):
        # HEADER
        header_frame = tk.Frame(self.root, bg=COLOR_BG)
        header_frame.pack(fill="x", padx=40, pady=(40, 10))
        
        tk.Label(header_frame, text="Internal Keyboard Manager", bg=COLOR_BG, fg=COLOR_TEXT_MAIN, 
                 font=FONT_TITLE).pack(anchor="w")
        tk.Frame(header_frame, bg=COLOR_ACCENT_SAFE, height=2, width=100).pack(anchor="w", pady=(5,0))
        
        # STATUS CARD
        self.status_frame = tk.Frame(self.root, bg=COLOR_PANEL, padx=25, pady=25)
        self.status_frame.pack(fill="x", padx=40, pady=20)
        
        tk.Label(self.status_frame, text="CURRENT STATUS:", bg=COLOR_PANEL, fg=COLOR_TEXT_SEC, 
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        
        self.lbl_status = tk.Label(self.status_frame, text="CHECKING...", bg=COLOR_PANEL, fg=COLOR_TEXT_MAIN, 
                                   font=FONT_STATUS)
        self.lbl_status.pack(pady=10)
        
        self.lbl_desc = tk.Label(self.status_frame, text="...", bg=COLOR_PANEL, fg=COLOR_TEXT_MAIN, 
                                 font=FONT_BODY, wraplength=400, justify="center")
        self.lbl_desc.pack()
        
        # ACTION BUTTON
        self.btn_action = tk.Button(self.root, text="ACTION", command=self.toggle_driver,
                                    font=FONT_BTN, relief="flat", cursor="hand2", width=35, pady=12,
                                    fg="#FFFFFF")
        self.btn_action.pack(pady=(0, 20))
        
        # GUIDE SECTION
        info_frame = tk.Frame(self.root, bg=COLOR_BG, padx=40)
        info_frame.pack(fill="both", expand=True)
        
        tk.Label(info_frame, text="GUIDE & WARNINGS", bg=COLOR_BG, fg=COLOR_ACCENT_WARNING, 
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 8))

        guide_text = (
            "• This tool disables the core driver (PS/2) at the Windows kernel level.\n"
            "• A RESTART IS REQUIRED for changes to take effect.\n"
            "• ⚠️ IMPORTANT: Laptop Touchpads often share the same bus as the keyboard. The TOUCHPAD MAY ALSO BE DISABLED.\n"
            "• Ensure you have an External USB/Bluetooth Mouse ready."
        )
        
        tk.Label(info_frame, text=guide_text, bg=COLOR_BG, fg=COLOR_TEXT_MAIN, 
                 font=FONT_BODY, justify="left", wraplength=440).pack(anchor="w")
        
        # FOOTER
        footer_frame = tk.Frame(self.root, bg=COLOR_BG)
        footer_frame.pack(fill="x", pady=20)
        tk.Label(footer_frame, text="Eco-Mode v2.1 • Safe & Organic", bg=COLOR_BG, fg=COLOR_TEXT_SEC, 
                 font=FONT_SMALL).pack(side="bottom")

    def check_driver(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_PATH, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "Start")
            winreg.CloseKey(key)
            return "DISABLED" if value == 4 else "ENABLED"
        except:
            return "UNKNOWN"

    def update_status_display(self):
        state = self.check_driver()
        self.current_state = state
        
        if state == "ENABLED":
            self.lbl_status.config(text="ACTIVE (ON)", fg=COLOR_ACCENT_SAFE)
            self.lbl_desc.config(text="Internal keyboard is functioning normally. Click below to disable it permanently.")
            self.btn_action.config(text="DISABLE & RESTART", bg=COLOR_ACCENT_DANGER, 
                                   activebackground="#A65D48", activeforeground="#FFFFFF")
            create_tooltip(self.btn_action, "Disable internal keyboard & touchpad, then restart.")
            
        elif state == "DISABLED":
            self.lbl_status.config(text="DISABLED (OFF)", fg=COLOR_ACCENT_DANGER)
            self.lbl_desc.config(text="Internal keyboard is killed. Use an external mouse/keyboard.")
            self.btn_action.config(text="ENABLE & RESTART", bg=COLOR_ACCENT_SAFE, 
                                   activebackground="#668260", activeforeground="#FFFFFF")
            create_tooltip(self.btn_action, "Restore internal keyboard function & restart.")
            
        else:
            self.lbl_status.config(text="UNKNOWN STATUS", fg=COLOR_ACCENT_WARNING)
            self.btn_action.config(state="disabled", bg=COLOR_PANEL, fg=COLOR_TEXT_SEC)

    def toggle_driver(self):
        if not is_admin():
            messagebox.showerror("Access Denied", "Administrator privileges required.")
            return

        target_mode = "disabled" if self.current_state == "ENABLED" else "auto"
        verb = "DISABLE" if target_mode == "disabled" else "ENABLE"

        confirm = messagebox.askyesno(
            f"Confirm {verb.capitalize()}",
            f"You are about to {verb} the internal keyboard driver.\n\n"
            "⚠️ WARNING:\n"
            "1. Computer will RESTART IMMEDIATELY.\n"
            "2. Touchpad might be disabled too.\n"
            "3. External Mouse is REQUIRED.\n\n"
            "Proceed?"
        )

        if confirm:
            loading = tk.Toplevel(self.root)
            loading.title("Processing...")
            loading.geometry("300x120")
            center_window(loading, 300, 120)
            loading.configure(bg=COLOR_BG)
            
            try: loading.iconbitmap(resource_path("lock.ico"))
            except: pass

            tk.Label(loading, text="Configuring System...", bg=COLOR_BG, fg=COLOR_TEXT_MAIN, 
                     font=FONT_BTN).pack(pady=20)
            
            pb = ttk.Progressbar(loading, mode="indeterminate")
            pb.pack(fill="x", padx=30)
            pb.start(15)
            self.root.update()

            cmd = f'sc config {SERVICE_NAME} start= {target_mode}'
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.run(cmd, check=True, startupinfo=startupinfo, shell=True)
                
                # Force restart 0 seconds
                subprocess.run("shutdown /r /t 0 /f", shell=True)
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                loading.destroy()

def main():
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        except:
            messagebox.showerror("Error", "Failed to request Admin access.")
    else:
        root = tk.Tk()
        app = KeyboardNukeLite(root)
        root.mainloop()

if __name__ == "__main__":
    main()