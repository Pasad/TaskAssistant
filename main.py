import wx

import common as com  # 공통 모듈
from tabs import *  # 탭 모듈

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Task Assistant", size=(800, 600))

        # 아이콘 설정
        self.SetIcon(wx.Icon(com.resource_path('icon.ico'), wx.BITMAP_TYPE_ICO))
        # ico 파일 포함 배포시 pyinstaller --onefile --noconsole --icon=icon.ico --add-data "icon.ico;." main.py
        # env 파일 포함 배포시 pyinstaller --onefile --noconsole --icon=icon.ico --add-data "icon.ico;." --add-data ".env;." main.py

        notebook = wx.Notebook(self)

        # Replacement 탭
        notebook.AddPage(pnReplacement(notebook), "Replacement")

        # Database 탭
        notebook.AddPage(pnDatabase(notebook), "Database")

        # Encryption 탭
        notebook.AddPage(pnEncryption(notebook), "Encryption")

        # 탭 기본 선택
        notebook.SetSelection(0)

        self.Show()

if __name__ == "__main__":
    app = wx.App()
    MainFrame()
    app.MainLoop()