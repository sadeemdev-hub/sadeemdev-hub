import pygetwindow as gw
import win32gui
import win32process
import psutil

def get_active_window_title():
    """Fetches the exact text title of the user's front-most open window with a fallback system hook."""
    try:
        # Get the literal handle of the foreground window
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        
        # If the window title is completely empty, look up the background process name instead
        if not title or title.strip() == "":
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            proc = psutil.Process(pid)
            title = proc.name()
            
        return title if title else "Desktop"
    except Exception:
        # Fallback to general pygetwindow method if the hook fails
        try:
            active_window = gw.getActiveWindow()
            if active_window is not None and active_window.title:
                return active_window.title
        except Exception:
            pass
        return "Unknown Context"
