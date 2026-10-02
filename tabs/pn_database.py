import wx

import common as com  # 공통 모듈

class pnDatabase(com.Panel):
    """
    Database 탭
    """
    _tables = []  # 테이블 목록
    _cols = []  # 컬럼 목록
    

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.initUI()
    

    def initUI(self):

        # 메인 사이저
        self.szMain = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.szMain)

        # SplitterWindow (좌우측으로 분할)
        self.spltMain = com.SplitterWindow(self)
        self.szMain.Add(self.spltMain, proportion=1, flag=wx.EXPAND)
        
        self.pnLeft = com.Panel(self.spltMain)  # 좌측 패널
        self.pnRight = com.Panel(self.spltMain)  # 우측 패널

        # spltMain 설정
        self.spltMain.SplitVertically(self.pnLeft, self.pnRight, sashPosition=350)
        self.spltMain.SetMinimumPaneSize(200) # 좌측 최소 크기 설정

        # 좌측 패널 설정
        self.szLeft = wx.BoxSizer(wx.VERTICAL)
        self.pnLeft.SetSizer(self.szLeft)

        self.btnLoading = com.Button(self.pnLeft, label="Loading", size=(0, 30)) # Loading 버튼
        self.szLeft.Add(self.btnLoading, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        self.btnLoading.Bind(wx.EVT_BUTTON, self.onButtonLoading)

        self.txtTableSearchTerm = com.TextCtrl(self.pnLeft, placeholder='Table search term(name or desc)') # 테이블 검색어 텍스트 박스
        self.txtTableSearchTerm.Bind(wx.EVT_TEXT, self.onTxtTableSearchTermChange)
        self.szLeft.Add(self.txtTableSearchTerm, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=5)
        
        self.grdTables = com.Grid(self.pnLeft) # 테이블 목록 그리드
        self.grdTables.SetCols(col_headers=["Table Name", "Table Desc"], col_widths=[140, 150])
        self.grdTables.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.onGrdTablesClick)
        self.szLeft.Add(self.grdTables, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=5)

        # 우측 패널 설정
        self.szRight = wx.BoxSizer(wx.VERTICAL)
        self.pnRight.SetSizer(self.szRight)
        
        self.szRight.AddSpacer(9) # 여백 추가

        self.stTableName = wx.StaticText(self.pnRight, label="Table Name : ") # 테이블명 텍스트
        self.szRight.Add(self.stTableName, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        self.txtColSearchTerm = com.TextCtrl(self.pnRight, placeholder='Column search term(name or desc)') # 컬럼명 텍스트 박스
        self.txtColSearchTerm.Bind(wx.EVT_TEXT, self.onTxtColSearchTermChange)
        self.szRight.Add(self.txtColSearchTerm, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        self.grdCols = com.Grid(self.pnRight) # 컬럼 목록 그리드
        self.grdCols.SetCols(col_headers=["Col Name", "Col Desc", "PK", "Type", "Nullable"], col_widths=[100, 100, 30, 70, 60])
        self.szRight.Add(self.grdCols, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=5)
      

    def onButtonLoading(self, event):
        """
        Loading 버튼 클릭 처리
        """

        self._tables = com.DB.get_data(f"""
            SELECT 
                table_name,
                table_comment
            FROM 
                information_schema.tables
            WHERE 
                table_schema = '{com.DB.DATABASE}'
            ORDER BY 
                table_name
            ;
        """)  # 데이터베이스에서 테이블 목록 가져오기

        self.grdTables.SetData(self._tables)
    

    def onTxtTableSearchTermChange(self, event):
        """
        테이블 검색어 텍스트 박스 변경 처리
        """

        search_term = event.GetString()

        # 검색어가 포함된 행만 조회
        filtered = [row for row in self._tables if any(search_term in cell for cell in row)]
        
        self.grdTables.SetData(filtered)


    def onTxtColSearchTermChange(self, event):
        """
        컬럼 검색어 텍스트 박스 변경 처리
        """

        search_term = event.GetString()

        # 검색어가 포함된 행만 조회
        filtered = [row for row in self._cols if any(search_term in cell for cell in row)]
        
        self.grdCols.SetData(filtered)


    def onGrdTablesClick(self, event):
        """
        테이블 목록 그리드 더블 클릭 처리
        """

        row = event.GetRow()
        table_name = self.grdTables.GetCellValue(row, 0)

        self._cols = com.DB.get_data(f"""            
            SELECT 
                c.column_name,
                c.column_comment,
                ifnull(s.seq_in_index, '') as pk,
                c.column_type,
                c.is_nullable
            FROM 
                information_schema.columns c
            LEFT JOIN 
                information_schema.statistics s
            ON 
                c.table_schema = s.table_schema
                AND c.table_name = s.table_name
                AND c.column_name = s.column_name
                AND s.index_name = 'primary'
            WHERE 
                c.table_schema = '{com.DB.DATABASE}' 
                AND c.table_name = '{table_name}'
            ORDER BY 
                c.ordinal_position;
            ;
        """)  # 데이터베이스에서 컬럼 정보 가져오기

        self.stTableName.SetLabel(f"Table Name : {table_name}")  # 테이블명 텍스트 설정

        self.grdCols.SetData(self._cols)  # 컬럼 정보 그리드에 설정

        