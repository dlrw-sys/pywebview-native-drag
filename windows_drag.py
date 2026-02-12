import pythoncom
import win32con
import win32api
import win32gui
import win32com.server.util
from win32com.shell import shell, shellcon
import ctypes
import time
import threading


DEBUG_DRAG = False   # ← включить / выключить лог

def log(*args):
    if DEBUG_DRAG:
        print("[DRAG]", *args, flush=True)


# ============================
# DropSource
# ============================

class DropSource:
    _com_interfaces_ = [pythoncom.IID_IDropSource]
    _public_methods_ = ['QueryContinueDrag', 'GiveFeedback']

    DRAGDROP_S_DROP = 0x00040100
    DRAGDROP_S_CANCEL = 0x00040101
    DRAGDROP_S_USEDEFAULTCURSORS = 0x00040102

    def QueryContinueDrag(self, esc, key_state):

        if esc:
            log("[DRAG] ESC → CANCEL")
            return self.DRAGDROP_S_CANCEL

        if not (win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000):
            log("[DRAG] MOUSE RELEASE → DROP")
            return self.DRAGDROP_S_DROP

        return 0  # S_OK

    def GiveFeedback(self, effect):
        return self.DRAGDROP_S_USEDEFAULTCURSORS


# ============================
# Мини message pump
# ============================

def pump_messages():
    msg = ctypes.wintypes.MSG()
    while ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), 0, 0, 0, 1):
        ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
        ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))


# ============================
# Основной drag
# ============================

def native_drag(paths, ctrl, hwnd):
    log("[DRAG] UI THREAD execution")

    win32gui.ReleaseCapture()

    pidls = []
    for p in paths:
        pidl, _ = shell.SHParseDisplayName(p, 0)
        pidls.append(pidl)

    desktop = shell.SHGetDesktopFolder()

    data_object = desktop.GetUIObjectOf(
        hwnd,
        pidls,
        pythoncom.IID_IDataObject,
        0
    )[1]

    drop_source = win32com.server.util.wrap(
        DropSource(),
        pythoncom.IID_IDropSource
    )

    effects = shellcon.DROPEFFECT_COPY | shellcon.DROPEFFECT_MOVE

    log("[DRAG] ENTER DoDragDrop")

    result = pythoncom.DoDragDrop(
        data_object,
        drop_source,
        effects
    )

    log("[DRAG] RESULT:", result)
