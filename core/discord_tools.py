"""
Location: C:/Users/Inicio/Proyectos/windows-scripts/core/discord_tools.py
Function: Win32 desktop automation utilities for Discord interaction, window activation, and clipboard pasting.
All Rights Reserved Arodi Emmanuel
"""

import sys
import os
import time
from pathlib import Path
from typing import Optional, List, Tuple

def set_clipboard_text(text: str) -> bool:
    """Sets Unicode text into Windows clipboard using Win32 API."""
    if sys.platform != "win32":
        return False
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    kernel32.GlobalAlloc.restype = ctypes.c_void_p
    kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    user32.SetClipboardData.restype = ctypes.c_void_p
    user32.SetClipboardData.argtypes = [wintypes.UINT, ctypes.c_void_p]
    user32.OpenClipboard.argtypes = [wintypes.HWND]

    CF_UNICODETEXT = 13
    GMEM_MOVEABLE = 0x0002

    if not user32.OpenClipboard(None):
        return False
    try:
        user32.EmptyClipboard()
        encoded = (text + "\0").encode("utf-16-le")
        h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(encoded))
        if not h_mem:
            return False
        ptr = kernel32.GlobalLock(h_mem)
        if not ptr:
            return False
        ctypes.memmove(ptr, encoded, len(encoded))
        kernel32.GlobalUnlock(h_mem)
        user32.SetClipboardData(CF_UNICODETEXT, h_mem)
        return True
    finally:
        user32.CloseClipboard()

def find_discord_windows(channel_keyword: str = "issues") -> List[Tuple[int, str]]:
    """Connects to interactive desktop station and returns list of Discord HWNDs."""
    if sys.platform != "win32":
        return []
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    hwinsta = user32.OpenWindowStationW("winsta0", False, 0x37F)
    if hwinsta:
        user32.SetProcessWindowStation(hwinsta)
        hdesk = user32.OpenDesktopW("default", 0, False, 0x1FF)
        if hdesk:
            user32.SetThreadDesktop(hdesk)

    results = []
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, wintypes.LPARAM)

    def enum_cb(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                title = buff.value
                if "Discord" in title and "Overlay" not in title:
                    results.append((hwnd, title))
        return 1

    user32.EnumWindows(WNDENUMPROC(enum_cb), 0)

    # Sort matching channel_keyword first (accent-insensitive)
    if channel_keyword:
        def strip_accents(s: str) -> str:
            s = s.lower()
            for a, b in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")]:
                s = s.replace(a, b)
            return s
        kw = strip_accents(channel_keyword)
        results.sort(key=lambda item: 0 if kw in strip_accents(item[1]) else 1)

    return results

def paste_to_discord(text: Optional[str] = None, channel_keyword: str = "issues", send_enter: bool = True) -> bool:
    """
    Brings Discord to foreground, clears existing message box, pastes Ctrl+V,
    and optionally presses Enter to send the message automatically.
    """
    if sys.platform != "win32":
        return False
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    if text:
        # Normalize text and line endings
        cleaned = "\r\n".join([line.rstrip() for line in text.strip().splitlines()])
        set_clipboard_text(cleaned)

    windows = find_discord_windows(channel_keyword=channel_keyword)
    if not windows:
        # Try launching discord: and re-enumerating
        import subprocess
        subprocess.Popen(["cmd", "/c", "start", "discord:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.5)
        windows = find_discord_windows(channel_keyword=channel_keyword)
        if not windows:
            return False

    target_hwnd, target_title = windows[0]

    # Bring target window to foreground
    SW_RESTORE = 9
    current_thread = kernel32.GetCurrentThreadId()
    target_thread = user32.GetWindowThreadProcessId(target_hwnd, None)

    user32.AttachThreadInput(current_thread, target_thread, True)
    user32.ShowWindow(target_hwnd, SW_RESTORE)
    user32.SetForegroundWindow(target_hwnd)
    user32.SetFocus(target_hwnd)
    user32.AttachThreadInput(current_thread, target_thread, False)

    # Bypass Windows foreground lock with Alt tap
    VK_MENU = 0x12
    KEYEVENTF_KEYUP = 0x0002
    user32.keybd_event(VK_MENU, 0, 0, 0)
    user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
    user32.SetForegroundWindow(target_hwnd)

    time.sleep(0.4)

    VK_CONTROL = 0x11
    VK_A = 0x41
    VK_BACK = 0x08
    VK_V = 0x56
    VK_RETURN = 0x0D

    # 1. Clear any existing text in the Discord message box (Ctrl+A -> Backspace)
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.03)
    user32.keybd_event(VK_A, 0, 0, 0)
    time.sleep(0.03)
    user32.keybd_event(VK_A, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.03)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)

    user32.keybd_event(VK_BACK, 0, 0, 0)
    time.sleep(0.03)
    user32.keybd_event(VK_BACK, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.08)

    # 2. Paste single copy of formatted text (Ctrl+V)
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.03)
    user32.keybd_event(VK_V, 0, 0, 0)
    time.sleep(0.03)
    user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.03)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

    # 3. Automatically send by simulating Enter if requested
    if send_enter:
        time.sleep(0.25)
        user32.keybd_event(VK_RETURN, 0, 0, 0)
        time.sleep(0.04)
        user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)

    return True

def set_clipboard_files(paths: List[str]) -> bool:
    """Sets a list of file paths onto Windows clipboard as CF_HDROP."""
    if sys.platform != "win32":
        return False
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    kernel32.GlobalAlloc.restype = ctypes.c_void_p
    kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    user32.SetClipboardData.restype = ctypes.c_void_p
    user32.SetClipboardData.argtypes = [wintypes.UINT, ctypes.c_void_p]
    user32.OpenClipboard.argtypes = [wintypes.HWND]

    abs_paths = [os.path.abspath(p) for p in paths if os.path.exists(p)]
    if not abs_paths:
        return False

    CF_HDROP = 15
    GMEM_MOVEABLE = 0x0002
    GMEM_ZEROINIT = 0x0040

    class DROPFILES(ctypes.Structure):
        _fields_ = [
            ("pFiles", wintypes.DWORD),
            ("pt", wintypes.POINT),
            ("fNC", wintypes.BOOL),
            ("fWide", wintypes.BOOL),
        ]

    buf = "".join(p + "\0" for p in abs_paths) + "\0"
    encoded_paths = buf.encode("utf-16le")

    dropfiles = DROPFILES()
    dropfiles.pFiles = ctypes.sizeof(DROPFILES)
    dropfiles.pt.x = 0
    dropfiles.pt.y = 0
    dropfiles.fNC = False
    dropfiles.fWide = True

    total_size = ctypes.sizeof(DROPFILES) + len(encoded_paths)
    h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, total_size)
    if not h_mem:
        return False
    ptr = kernel32.GlobalLock(h_mem)
    if not ptr:
        return False

    ctypes.memmove(ptr, ctypes.byref(dropfiles), ctypes.sizeof(DROPFILES))
    ctypes.memmove(ptr + ctypes.sizeof(DROPFILES), encoded_paths, len(encoded_paths))
    kernel32.GlobalUnlock(h_mem)

    hwinsta = user32.OpenWindowStationW("winsta0", False, 0x37F)
    if hwinsta:
        user32.SetProcessWindowStation(hwinsta)
        hdesk = user32.OpenDesktopW("default", 0, False, 0x1FF)
        if hdesk:
            user32.SetThreadDesktop(hdesk)

    if not user32.OpenClipboard(None):
        return False
    try:
        user32.EmptyClipboard()
        res = user32.SetClipboardData(CF_HDROP, h_mem)
        return bool(res)
    finally:
        user32.CloseClipboard()

def upload_files_to_discord(file_paths: List[str], channel_keyword: str = "bitacora") -> bool:
    """Attaches files via CF_HDROP and uploads them directly to the Discord channel."""
    if not set_clipboard_files(file_paths):
        return False

    import ctypes
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    windows = find_discord_windows(channel_keyword=channel_keyword)
    if not windows:
        return False

    target_hwnd, target_title = windows[0]

    current_thread = kernel32.GetCurrentThreadId()
    target_thread = user32.GetWindowThreadProcessId(target_hwnd, None)

    user32.AttachThreadInput(current_thread, target_thread, True)
    user32.ShowWindow(target_hwnd, 9)
    user32.SetForegroundWindow(target_hwnd)
    user32.SetFocus(target_hwnd)
    user32.AttachThreadInput(current_thread, target_thread, False)

    VK_MENU = 0x12
    KEYEVENTF_KEYUP = 0x0002
    user32.keybd_event(VK_MENU, 0, 0, 0)
    user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
    user32.SetForegroundWindow(target_hwnd)

    time.sleep(0.4)

    # Paste file into Discord
    VK_CONTROL = 0x11
    VK_V = 0x56
    VK_RETURN = 0x0D

    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.04)
    user32.keybd_event(VK_V, 0, 0, 0)
    time.sleep(0.04)
    user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.04)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

    time.sleep(0.8)

    # Press Enter to upload
    user32.keybd_event(VK_RETURN, 0, 0, 0)
    time.sleep(0.04)
    user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)

    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        target_path = Path(arg)
        if target_path.exists() and target_path.is_file():
            content = target_path.read_text(encoding="utf-8", errors="replace")
        else:
            content = " ".join(sys.argv[1:])
        ok = paste_to_discord(content, send_enter=True)
    else:
        ok = paste_to_discord(send_enter=True)
    print("SENT" if ok else "FAILED")
