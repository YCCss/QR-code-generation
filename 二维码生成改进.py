import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qrcode import QRCode, ERROR_CORRECT_H
from PIL import Image,ImageDraw,ImageFont

class Qr_qt(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("二维码生成")
        self.setWindowIcon(QIcon('icon.png'))

        self.lab1 = QLabel('请输入二维码的内容 ')
        self.lab2 = QLabel('请输入6位编号的内容')

        self.text1 = QLineEdit('内容', self)
        self.text1.selectAll()
        self.text2 = QLineEdit('6位编号', self)

        self.bt1 = QPushButton('选择图片', self)
        self.bt1.setToolTip("<b>点击按钮选择要插入的图片</b>")
        self.bt1.clicked.connect(self.chooseImage)

        self.bt2 = QPushButton('生成', self)
        self.bt2.setToolTip("<b>点击按钮生成二维码</b>")
        self.bt2.clicked.connect(self.createQr)


        grid = QGridLayout()
        grid.addWidget(self.lab1, 0, 0)
        grid.addWidget(self.text1, 0, 1)
        grid.addWidget(self.lab2, 1, 0)
        grid.addWidget(self.text2, 1, 1)
        grid.addWidget(self.bt1, 2, 0)
        grid.addWidget(self.bt2, 2, 1)
        self.setLayout(grid)

        self.show()

    def chooseImage(self):
        self.fname, jud = QFileDialog.getOpenFileName(self, '打开文件', './', "Image Files (*.jpg *.png)")

    def createQr(self):
        qr = QRCode(version = 1, error_correction = ERROR_CORRECT_H, border = 4)

        qr.add_data(self.text1.text())
        qr.make(fit = True)

        img = qr.make_image()
        img = img.convert("RGB")

        if self.text2.text():
            try:
                w, h = img.size
                text = self.text2.text()
                dr = ImageDraw.Draw(img)
                font = ImageFont.truetype(os.path.join("C:/Windows/Fonts", "simyou.ttf"), 50)
                dr.text(((w-160)/2,h-45),text,font=font,fill='#000000')
                #上述将字符串写道图片上

            except:
                QMessageBox.about(self, 'Error', 'Error')    
        
        if self.text2.text() == None:
            pass

        try:
            logo = Image.open(self.fname)

            w, h = img.size
            logo_w = int(w/4)
            logo_h = int(h/4)

            rel_w = int((w-logo_w)/2)
            rel_h = int((h-logo_h)/2)
            logo = logo.resize((logo_w, logo_h), Image.ANTIALIAS)
            logo = logo.convert("RGBA")
            img.paste(logo, (rel_w, rel_h), logo)
            finame, jud = QFileDialog.getSaveFileName(self, '保存文件', './', "Image Files (*.jpg *.png)")
            if jud and img:
                img.save(finame)

        except:
            QMessageBox.about(self, 'Error', 'No Such a File')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    qr = Qr_qt()
    sys.exit(app.exec_())