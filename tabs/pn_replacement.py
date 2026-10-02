import wx

import common as com  # 공통 모듈

class pnReplacement(com.Panel):
    """
    Replacement 탭
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.initUI()


    def initUI(self):

        # 메인 사이저
        self.szMain = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.szMain)

        # SplitterWindow (상단과 하단 분할)
        self.spltMain = com.SplitterWindow(self)
        self.szMain.Add(self.spltMain, proportion=1, flag=wx.EXPAND)
        
        self.pnTop = com.Panel(self.spltMain)     # 상단 패널
        self.pnBottom = com.Panel(self.spltMain)  # 하단 패널       

        # spltMain 설정
        self.spltMain.SplitHorizontally(self.pnTop, self.pnBottom, sashPosition=150)
        self.spltMain.SetMinimumPaneSize(100) # 상단 최소 크기 설정
        
        # 상단 패널
        self.szTop = wx.BoxSizer(wx.HORIZONTAL)
        self.pnTop.SetSizer(self.szTop)
        self.grdData = com.Grid(self.pnTop)        
        self.btnSetData = com.Button(self.pnTop, label="Set Data", size=(80, 110))
        self.btnSetData.Bind(wx.EVT_BUTTON, self.onBtnSetData)
        self.szTop.Add(self.grdData, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.szTop.Add(self.btnSetData, proportion=0, flag=wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, border=5)

        # 하단 패널 (패턴 패널 + 결과 패널)
        self.szBottom = wx.BoxSizer(wx.VERTICAL)
        self.pnBottom.SetSizer(self.szBottom)

        self.panel_pattern = com.Panel(self.pnBottom)
        self.szBottom.Add(self.panel_pattern, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        self.pnResult = com.Panel(self.pnBottom)
        self.szBottom.Add(self.pnResult, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # 패턴 패널 내부 레이아웃
        self.szPattern = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_pattern.SetSizer(self.szPattern)

        self.txtPattern = com.TextCtrl(self.panel_pattern, placeholder='패턴 입력 $1, $2,...', style=wx.TE_MULTILINE)
        self.btnReplace = com.Button(self.panel_pattern, label="Replace", size=(80, 110))
        self.btnReplace.Bind(wx.EVT_BUTTON, self.onBtnReplace)

        self.szPattern.Add(self.txtPattern, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=5)
        self.szPattern.Add(self.btnReplace, proportion=0, flag=wx.EXPAND)

        # 결과 패널 내부 레이아웃
        self.szResult = wx.BoxSizer(wx.VERTICAL)
        self.pnResult.SetSizer(self.szResult)
        self.txtResult = com.TextCtrl(self.pnResult, placeholder='Replacement 결과값', style=wx.TE_MULTILINE)
        self.szResult.Add(self.txtResult, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)


    def onBtnSetData(self, event):
        """
        Set Data 버튼 클릭 처리 : 클립 보드에서 행열 데이터를 읽어, 그리드에 설정
        """
        if wx.TheClipboard.Open():
            text_data = wx.TextDataObject()
            success = wx.TheClipboard.GetData(text_data)
            wx.TheClipboard.Close()
            if success:                
                try:
                    # 클립보드에서 행열 데이터를 가져와 2차원 리스트로 변환
                    clipboard_text = text_data.GetText()
                    data = [row.split("\t") for row in clipboard_text.strip().split("\n")]
                    
                    self.grdData.SetGrid(data)  # 그리드에 설정
                    
                    # 열 헤더명 설정($1, $2, ...)
                    for col in range(self.grdData.GetNumberCols()):
                        self.grdData.SetColLabelValue(col, f"${col+1}")

                except Exception as e:
                    wx.MessageBox(f"데이터 로드에 실패했습니다.", "오류", wx.OK | wx.ICON_ERROR)
                    

    def onBtnReplace(self, event):
        """
        Replace 버튼 클릭 처리 : 그리드의 데이터를 패턴에 맞게 변환하여 결과 텍스트 박스에 표시
        """        
        # 결과 텍스트 박스 초기화
        self.txtResult.SetValue('')

        # 패턴 입력 확인
        pattern = self.txtPattern.GetValue()
        if not pattern:
            wx.MessageBox("패턴을 입력하세요.", "오류", wx.OK | wx.ICON_ERROR)
            return

        # 그리드에서 데이터 가져오기
        if self.grdData.GetNumberRows() == 0:
            wx.MessageBox("데이터가 없습니다.", "오류", wx.OK | wx.ICON_ERROR)
            return
        
        data = self.grdData.GetData()

        # 데이터의 행과 열 수 확인
        rows = len(data)
        cols = len(data[0])

        result = "" # 결과 문자열 초기화

        # 패턴에 맞게 데이터 변환
        # 패턴에서 $1, $2, ...를 데이터로 대체
        for row_index, row in enumerate(data):
            row_replaced = pattern
            for col_index, col in enumerate(row):
                row_replaced = row_replaced.replace(f'${col_index+1}', col)
            result += row_replaced + "\n"
                    
        # 결과를 텍스트 박스에 표시
        self.txtResult.SetValue(result)
        
