from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel

class SPIDecodeTool_VerGUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPIDecodeToolについて")
        self.resize(300, 90)
        
        layout = QFormLayout()
        self.lbVer = QLabel("Version   \t：1.4.0\n" + 
                            "Created by \t：GaoHongyu\n" + 
                            "MailAddress\t：hongyu.gao.zs@kyocera.jp\n" + 
                            "Created at \t：京セラ横浜事務所")
        layout.addWidget(self.lbVer)
        
        self.setLayout(layout)
        
