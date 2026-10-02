import wx

import common as com  # 공통 모듈

class pnEncryption(com.Panel):
    """
    Encryption 탭
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.fernetCipher = com.FernetCipher()  # 암호화 객체 생성
        self.initUI()


    def initUI(self):

        # 메인 사이저
        self.szMain = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.szMain)

        # Base64 그룹
        self.sbBase64 = wx.StaticBox(self, label="Base64")
        self.sbszBase64 = wx.StaticBoxSizer(self.sbBase64, wx.VERTICAL)

        self.grdszBase64 = wx.GridSizer(rows=2, cols=2, hgap=10, vgap=10)
        
        self.txtBase64EncodeIn = com.TextCtrl(self, placeholder='Base64 Encode Input') # Base64 인코딩 입력값
        self.txtBase64EncodeIn.Bind(wx.EVT_TEXT, self.onTxtBase64EncodeInChange)
        self.grdszBase64.Add(self.txtBase64EncodeIn, flag=wx.EXPAND)
        self.txtBase64EncodeOut = com.TextCtrl(self, placeholder='Base64 Encode Output') # Base64 인코딩 출력값
        self.grdszBase64.Add(self.txtBase64EncodeOut, flag=wx.EXPAND)
        
        self.txtBase64DecodeIn = com.TextCtrl(self, placeholder='Base64 Decode Input') # Base64 디코딩 입력값
        self.txtBase64DecodeIn.Bind(wx.EVT_TEXT, self.onTxtBase64DecodeInChange)
        self.grdszBase64.Add(self.txtBase64DecodeIn, flag=wx.EXPAND)
        self.txtBase64DecodeOut = com.TextCtrl(self, placeholder='Base64 Decode Output') # Base64 디코딩 출력값 
        self.grdszBase64.Add(self.txtBase64DecodeOut, flag=wx.EXPAND)

        self.sbszBase64.Add(self.grdszBase64, flag=wx.ALL | wx.EXPAND, border=10)

        # URL 그룹
        self.sbURL = wx.StaticBox(self, label="URL")
        self.sbszURL = wx.StaticBoxSizer(self.sbURL, wx.VERTICAL)

        self.grdszURL = wx.GridSizer(rows=2, cols=2, hgap=10, vgap=10)

        self.txtURLEncodeIn = com.TextCtrl(self, placeholder='URL Encode Input') # URL 인코딩 입력값
        self.txtURLEncodeIn.Bind(wx.EVT_TEXT, self.onTxtURLEncodeInChange)
        self.grdszURL.Add(self.txtURLEncodeIn, flag=wx.EXPAND)
        self.txtURLEncodeOut = com.TextCtrl(self, placeholder='URL Encode Output') # URL 인코딩 출력값
        self.grdszURL.Add(self.txtURLEncodeOut, flag=wx.EXPAND)

        self.txtURLDecodeIn = com.TextCtrl(self, placeholder='URL Decode Input') # URL 디코딩 입력값
        self.txtURLDecodeIn.Bind(wx.EVT_TEXT, self.onTxtURLDecodeInChange)
        self.grdszURL.Add(self.txtURLDecodeIn, flag=wx.EXPAND)
        self.txtURLDecodeOut = com.TextCtrl(self, placeholder='URL Decode Output') # URL 디코딩 출력값 
        self.grdszURL.Add(self.txtURLDecodeOut, flag=wx.EXPAND)

        self.sbszURL.Add(self.grdszURL, flag=wx.ALL | wx.EXPAND, border=10)
        
        # Encryption 그룹
        self.sbEncryption = wx.StaticBox(self, label="Encryption")
        self.sbszEncryption = wx.StaticBoxSizer(self.sbEncryption, wx.VERTICAL)

        self.grdszEncryption = wx.GridSizer(rows=2, cols=2, hgap=10, vgap=10)

        self.txtEncryptIn = com.TextCtrl(self, placeholder='Encrypt Input') # 암호화 입력값
        self.txtEncryptIn.Bind(wx.EVT_TEXT, self.onTxtEncryptInChange)
        self.grdszEncryption.Add(self.txtEncryptIn, flag=wx.EXPAND)
        self.txtEncryptOut = com.TextCtrl(self, placeholder='Encrypt Output') # 암호화 출력값
        self.grdszEncryption.Add(self.txtEncryptOut, flag=wx.EXPAND)

        self.txtDecryptIn = com.TextCtrl(self, placeholder='Decrypt Input') # 복호화 입력값
        self.txtDecryptIn.Bind(wx.EVT_TEXT, self.onTxtDecryptInChange)
        self.grdszEncryption.Add(self.txtDecryptIn, flag=wx.EXPAND)
        self.txtDecryptOut = com.TextCtrl(self, placeholder='Decrypt Output') # 복호화 출력값 
        self.grdszEncryption.Add(self.txtDecryptOut, flag=wx.EXPAND)

        self.sbszEncryption.Add(self.grdszEncryption, flag=wx.ALL | wx.EXPAND, border=10)

        # 그룹들을 메인 레이아웃에 추가
        self.szMain.Add(self.sbszBase64, flag=wx.ALL | wx.EXPAND, border=10)
        self.szMain.Add(self.sbszURL, flag=wx.ALL | wx.EXPAND, border=10)
        self.szMain.Add(self.sbszEncryption, flag=wx.ALL | wx.EXPAND, border=10)


    def onTxtBase64EncodeInChange(self, event):
        """
        Base64 인코딩 입력값 변경 처리
        """
        input_value = self.txtBase64EncodeIn.GetValue()
        if input_value:
            # Base64 인코딩
            encoded_value = com.base64_encode(input_value)
            self.txtBase64EncodeOut.SetValue(encoded_value)
        else:
            self.txtBase64EncodeOut.SetValue("")
        
    
    def onTxtBase64DecodeInChange(self, event):
        """
        Base64 디코딩 입력값 변경 처리
        """
        input_value = self.txtBase64DecodeIn.GetValue()
        if input_value:
            # Base64 디코딩
            decoded_value = com.base64_decode(input_value)
            self.txtBase64DecodeOut.SetValue(decoded_value)
        else:
            self.txtBase64DecodeOut.SetValue("")

    
    def onTxtURLEncodeInChange(self, event):
        """
        URL 인코딩 입력값 변경 처리
        """
        input_value = self.txtURLEncodeIn.GetValue()
        if input_value:
            # URL 인코딩
            encoded_value = com.url_encode(input_value)
            self.txtURLEncodeOut.SetValue(encoded_value)
        else:
            self.txtURLEncodeOut.SetValue("")


    def onTxtURLDecodeInChange(self, event):
        """
        URL 디코딩 입력값 변경 처리
        """
        input_value = self.txtURLDecodeIn.GetValue()
        if input_value:
            # URL 디코딩
            decoded_value = com.url_decode(input_value)
            self.txtURLDecodeOut.SetValue(decoded_value)
        else:
            self.txtURLDecodeOut.SetValue("")


    def onTxtEncryptInChange(self, event):
        """
        암호화 입력값 변경 처리
        """
        input_value = self.txtEncryptIn.GetValue()
        if input_value:
            # 암호화
            encrypted_value = self.fernetCipher.encrypt(input_value)
            self.txtEncryptOut.SetValue(encrypted_value)
        else:
            self.txtEncryptOut.SetValue("")


    def onTxtDecryptInChange(self, event):
        """
        복호화 입력값 변경 처리
        """
        input_value = self.txtDecryptIn.GetValue()
        if input_value:
            # 복호화
            decrypted_value = self.fernetCipher.decrypt(input_value)
            self.txtDecryptOut.SetValue(decrypted_value)
        else:
            self.txtDecryptOut.SetValue("")