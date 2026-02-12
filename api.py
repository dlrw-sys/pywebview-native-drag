import webview
import win32gui
import win32con
import win32api
from windows_drag import native_drag

# ------------------------------
# Global
# ------------------------------
MAIN_HWND = None
DRAG_DATA = None
ORIGINAL_WNDPROC = None
WM_APP_DRAG = win32con.WM_APP + 1

# ------------------------------
# subclass for WebView2
# ------------------------------

def install_wndproc(hwnd):
    global ORIGINAL_WNDPROC

    def wndproc(hWnd, msg, wParam, lParam):
        global DRAG_DATA
        if msg == WM_APP_DRAG:
            print("[UI] WM_APP_DRAG received")
            if DRAG_DATA:
                paths, ctrl = DRAG_DATA
                DRAG_DATA = None
                native_drag(paths, ctrl, hWnd)
            return 0
        return win32gui.CallWindowProc(ORIGINAL_WNDPROC, hWnd, msg, wParam, lParam)

    ORIGINAL_WNDPROC = win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, wndproc)
    print("[UI] Subclass installed")

# ------------------------------
# WebView2 HWND
# ------------------------------

def find_webview_hwnd(parent):
    result = []
    def enum_child(hwnd, _):
        cls = win32gui.GetClassName(hwnd)
        if "Chrome_WidgetWin" in cls:
            result.append(hwnd)
        return True
    win32gui.EnumChildWindows(parent, enum_child, None)
    return result[0] if result else parent

def after_start_func(window):
    global MAIN_HWND
    root = window._hWnd  # webview window
    MAIN_HWND = find_webview_hwnd(root)
    print("ROOT:", root)
    print("WEBVIEW HWND:", MAIN_HWND)
    install_wndproc(MAIN_HWND)

# ------------------------------
# API for JS
# ------------------------------

class WebAPI:
    def external_drag(self, data):
        global DRAG_DATA
        paths = data.get("paths", [])
        ctrl = data.get("ctrl", False)
        if not paths:
            return
        DRAG_DATA = (paths, ctrl)
        print("[API] Posting WM_APP_DRAG")
        win32api.PostMessage(MAIN_HWND, WM_APP_DRAG, 0, 0)

# ------------------------------
# WebView
# ------------------------------

api = WebAPI()
window = webview.create_window("Drag & Drop Demo", "https://example.com", js_api=api)
webview.start(after_start=after_start_func, gui='edgechromium', debug=True)