WebView Native Drag (Windows)

Native file drag-and-drop from pywebview (WebView2) to Windows Explorer.

Requirements

• Windows
• Python 3.10+
• WebView2 Runtime
• pywebview
• pywin32

Install
pip install -r requirements.txt

Usage from JS
window.pywebview.api.external_drag({
    paths: ["D:\\example.png"],
    ctrl: false
});

Parameters
Field	Type	Description
paths	array	Full Windows file paths
ctrl	bool	If true → copy, else move

Notes

• Works only on Windows
• Uses native OLE DoDragDrop
• Designed for WebView2 backend
