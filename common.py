import wx
import os
import sys
import wx.grid
import mariadb
import base64
from dotenv import load_dotenv
from urllib.parse import quote, unquote, urlencode, parse_qs
from cryptography.fernet import Fernet


def resource_path(relative_path: str) -> str:
    """ 
    PyInstaller 환경에서 리소스 경로 추적
    :param relative_path: 상대 경로
    :return: 절대 경로
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# .env 파일 로드
load_dotenv(dotenv_path = resource_path(".env"))

# 환경 변수 가져오기
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# 색상 상수 정의
PANEL_BG_COLOR = (230, 230, 230) # 패널 기본 배경색
BUTTON_BG_COLOR = (240, 240, 240) # 버튼 배경색
BUTTON_TEXT_COLOR = (9, 10, 9) # 버튼 글자색





def lighten_color(color: tuple, factor : float =0.2) -> tuple: 
    """
    주어진 RGB 색상을 옅게 만드는 함수
    :param color: (R, G, B) 튜플
    :param factor: 밝기 증가 비율 (0~1)
    :return: 옅어진 색상 (R, G, B)
    """
    r, g, b = color
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return (r, g, b)


def base64_encode(txt: str) -> str:
    """
    Base64 인코딩 함수
    :param txt: 인코딩할 문자열
    :return: Base64 인코딩된 문자열
    """    
    return base64.b64encode(txt.encode('utf-8')).decode('utf-8')


def base64_decode(data: str) -> str:
    """
    Base64 디코딩 함수
    :param data: 디코딩할 Base64 문자열
    :return: 디코딩된 문자열
    """    
    return base64.b64decode(data.encode('utf-8')).decode('utf-8')


def url_encode(text: str) -> str:
    """
    URL 인코딩 함수
    :param text: 인코딩할 문자열
    :return: URL 인코딩된 문자열
    """
    return quote(text, safe='')


def url_decode(encoded_text: str) -> str:
    """
    URL 인코딩된 문자열을 디코딩
    :param encoded_text: URL 인코딩된 문자열
    :return: 디코딩된 문자열
    """
    return unquote(encoded_text)


def generate_key() -> bytes:
    """
    대칭키 생성 함수
    :return: 생성된 대칭키 (bytes)
    """
    return Fernet.generate_key()


class FernetCipher:
    """
    대칭키 암호화 클래스
    """
    def __init__(self, key: bytes = ENCRYPTION_KEY):
        """
        :param key: 대칭키 (bytes)
        """
        self.cipher = Fernet(key)


    def encrypt(self, data: str) -> str:
        """
        문자열 데이터를 암호화하여 문자열로 반환
        :param data: 암호화할 문자열
        :return: 암호화된 문자열
        """
        return self.cipher.encrypt(data.encode()).decode()


    def decrypt(self, encrypted : str) -> str:
        """
        암호화된 문자열을 복호화하여 원래 문자열로 반환
        :param token: 암호화된 문자열
        :return: 복호화된 문자열
        """
        return self.cipher.decrypt(encrypted.encode()).decode()
    

class SplitterWindow(wx.SplitterWindow):
    """
    공통 SplitterWindow 클래스
    :param parent: 부모 윈도우
    :param style: wx.SplitterWindow 스타일
    :param kwargs: 기타 wx.SplitterWindow 옵션
    """
    def __init__(self, parent, style=wx.SP_LIVE_UPDATE | wx.SP_3DSASH, **kwargs):
        super().__init__(parent, style=style, **kwargs)
        self.SetDoubleBuffered(True)  # 더블 버퍼링 활성화


class Button(wx.Button):
    """
    공통버튼 클래스 : 버튼의 기본 스타일 설정    
    """
    def __init__(self, parent, bg_color=BUTTON_BG_COLOR, fg_color=BUTTON_TEXT_COLOR, **kwargs):
        """
        :param parent: 부모 윈도우
        :param bg_color: 버튼 배경색 (wx.Colour)
        :param fg_color: 버튼 글자색 (wx.Colour)
        :param kwargs: 기타 Button 옵션
        """
        super().__init__(parent, **kwargs)
        self.bg_color = bg_color
        self.fg_color = fg_color
                
        self.SetBackgroundColour(self.bg_color)
        self.SetForegroundColour(self.fg_color)        


class Panel(wx.Panel):
    """
    공통 패널 클래스 : 패널의 기본 배경색 설정
    """
    def __init__(self, parent, background_color=PANEL_BG_COLOR, **kwargs):
        """
        :param parent: 부모 윈도우
        :param background_color: 패널 배경색 (wx.Colour)
        :param kwargs: 기타 Panel 옵션
        """
        super().__init__(parent, **kwargs)
        self.SetBackgroundColour(background_color) # 패널의 기본 배경색


class TextCtrl(wx.TextCtrl):
    """
    공통 텍스트 박스 클래스
    """ 
    def __init__(self, parent, default_text="", placeholder="", **kwargs):
        """
        :param parent: 부모 윈도우
        :param default_text: 기본 텍스트
        :param placeholder: 플레이스홀더 텍스트        
        """
        super().__init__(parent, **kwargs)

        # 기본 텍스트 설정
        self.SetValue(default_text)

        # 플레이스홀더 설정 (윈도우, 맥 지원)
        if wx.Platform == "__WXMSW__" or wx.Platform == "__WXMAC__":
            self.SetHint(placeholder)


class Grid(wx.grid.Grid):
    """
    공통 그리드 클래스
    """
    def __init__(self, parent, rows=0, cols=0, readonly=True, **kwargs):
        """        
        :param parent: 부모 윈도우
        :param rows: 초기 행 수
        :param cols: 초기 열 수
        :param readonly: 읽기 전용 여부
        :param kwargs: 기타 grid 옵션
        """
        super().__init__(parent, **kwargs)

        # 그리드 크기 설정
        self.CreateGrid(rows, cols)        

        # 그리드 행 헤더 크기 기본 설정
        self.SetRowLabelSize(50)

        # 그리드 수정가능 여부 설정
        self.EnableEditing(not readonly)
        
        # 셀 크기 자동 조정
        self.AutoSizeColumns()
        self.AutoSizeRows()


    def Clear(self):
        """
        그리드 비우기 : 행열을 모두 삭제
        """
        self.ClearGrid() # 그리드 데이터 초기화
                
        if self.GetNumberRows() > 0: # 행 삭제            
            self.DeleteRows(0, self.GetNumberRows())
        
        if self.GetNumberCols() > 0: # 열 삭제
            self.DeleteCols(0, self.GetNumberCols())


    def ClearData(self):
        """
        그리드 데이터 비우기 : 행만 삭제하고 열은 유지
        """
        self.ClearGrid() # 그리드 데이터 초기화
                
        if self.GetNumberRows() > 0: # 행 삭제            
            self.DeleteRows(0, self.GetNumberRows())


    def SetCols(self, col_headers=[], col_widths=[]):
        """
        그리드 열 수 설정
        :param col_headers: 열 헤더 리스트
        :param col_widths: 열 너비 리스트
        """
        self.AppendCols(len(col_headers))

        if col_headers: # 열 헤더 설정
            for col in range(len(col_headers)):
                self.SetColLabelValue(col, str(col_headers[col]))
        
        if col_widths: # 열 너비 설정
            for col in range(len(col_widths)):
                self.SetColSize(col, col_widths[col])                
    

    def SetGrid(self, data, col_headers=[], col_widths=[]):
        """
        그리드에 데이터 설정 : 행열 정보를 모두 초기화하고, 새로 설정
        :param data: 2D 리스트 형태의 데이터
        :param col_headers: 열 헤더 리스트
        :param col_widths: 열 너비 리스트
        """
        
        rows = len(data)
        cols = len(data[0]) if rows > 0 else 0

        self.Clear() # 그리드 비우기
        self.AppendRows(rows)
        if col_headers == []: # 열 헤더가 없을 경우
            self.AppendCols(cols) # 열 수 설정
        else: # 열 헤더가 있을 경우
            self.SetCols(col_headers, col_widths) # 열 헤더 설정

        if rows == 0: # 데이터가 없을 경우
            return

        for row in range(rows): # 그리드 데이터 설정
            for col in range(cols):
                self.SetCellValue(row, col, str(data[row][col]))        

    
    def SetData(self, data):
        """
        그리드에 데이터 설정 : 기존의 열 정보는 유지하고, 행만 삭제 후 데이터 설정
        """

        rows = len(data)
        cols = len(data[0]) if rows > 0 else 0

        self.ClearData() # 그리드 비우기(행만 삭제)

        if rows == 0: # 데이터가 없을 경우
            return
        
        self.AppendRows(rows) # 그리드에 행 추가

        for row in range(rows): # 그리드 데이터 설정
            for col in range(cols):
                self.SetCellValue(row, col, str(data[row][col]))


    def GetData(self):
        """
        그리드에서 데이터 가져오기
        :return: 2D 리스트 형태의 데이터
        """
        data = []
        for row in range(self.GetNumberRows()):
            row_data = []
            for col in range(self.GetNumberCols()):
                row_data.append(self.GetCellValue(row, col))
            data.append(row_data)
        return data
    

    def GetColHeaders(self):
        """
        그리드의 열 헤더 가져오기
        """
        return [self.GetColLabelValue(col) for col in range(self.GetNumberCols())]
   

    def GetColWidths(self):
        """
        그리드의 열 너비 가져오기
        """
        return [self.GetColSize(col) for col in range(self.GetNumberCols())]


class DB():
    """
    DB 클래스
    """
    HOST = os.getenv('DB_HOST')
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE = os.getenv('DB_NAME')


    def __init__(self):
        pass


    @classmethod
    def connect(cls):
        try:
            return mariadb.connect(
                host=cls.HOST,
                user=cls.USER,
                password=cls.PASSWORD,
                database=cls.DATABASE
            )
        except mariadb.Error as e:
            print(f"Error connecting to the database: {e}")
            return None


    @classmethod
    def get_data(cls, query):
        try:
            with cls.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error fetching data: {e}")
            return None