#需要输入文件路径和生成图片路径
#来自：https://blog.csdn.net/pp5354chun/article/details/88408289
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLineEdit, QGridLayout, QLabel
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from qrcode import QRCode, ERROR_CORRECT_H
from PIL import Image,ImageDraw,ImageFont


class Qr_qt(QWidget): #自定义的类继承QWidget
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QR Code Maker") #设置标题
        self.setWindowIcon(QIcon('icon.png')) #设置窗口的图标（左上角那个），可有可无
        

		#设置三个标签，这里为了对齐方便加了一些空格
        self.lab1 = QLabel('Please Enter The Content Here')
        self.lab2 = QLabel('    Choose a Picture Here    ')
        self.lab3 = QLabel('      Save The QR Code       ')
        
		#设置三个文本框，使用行文本框形式
        self.text1 = QLineEdit('Content', self)
        self.text1.selectAll() #设置该文本框的内容初始被选中
        self.text2 = QLineEdit('Picture', self)
        self.text3 = QLineEdit('Path', self)

		#创建两个按钮
        self.bt1 = QPushButton('Create', self)
        self.bt1.setToolTip("<b>Push Here To Create QR Code</b>") 
        #按钮提示信息，将鼠标悬停在该按钮上会显示信息，使用html字符串
        self.bt1.clicked.connect(self.create_qr) 
        #关联bt1和自定义的create_qr函数，按下按钮会执行该函数

        self.bt2 = QPushButton('Quit', self)
        self.bt2.setToolTip("<b>Push Here To Quit</b>")
        self.bt2.clicked.connect(QCoreApplication.instance().quit)
        #将bt2关联退出窗口事件

        grid = QGridLayout() #采用网格布局
        grid.addWidget(self.lab1, 0, 0) #第一个参数是被排布的元素，后两个参数是元素的位置
        grid.addWidget(self.text1, 0, 1)
        grid.addWidget(self.lab2, 1, 0)
        grid.addWidget(self.text2, 1, 1)
        grid.addWidget(self.lab3, 2, 0)
        grid.addWidget(self.text3, 2, 1)
        grid.addWidget(self.bt1, 3, 0)
        grid.addWidget(self.bt2, 3, 1)
        self.setLayout(grid)

        self.show()

    def create_qr(self):
        qr = QRCode(version = 1, error_correction = ERROR_CORRECT_H, border = 4)
		#实例化一个QRcode类；version表示容错率，1为最高；error_correction表示纠错程度；
		#border表示二维码四周留白的格子数
		
        qr.add_data(self.text1.text()) #想要二维码s扫出来的内容
        qr.make(fit = True) #生成

        img = qr.make_image() #产生一个可处理的图像对象
        img = img.convert("RGB") #设置色彩格式为RGB
        '''
        if self.text2.text():
            try:
                logo = Image.open('{}'.format(self.text2.text()))

                w, h = img.size
                logo_w = int(w/4)
                logo_h = int(h/4)

                rel_w = int((w-logo_w)/2)
                rel_h = int((h-logo_h)/2)
                logo = logo.resize((logo_w, logo_h), Image.ANTIALIAS)
                #上面的代码全都是用来调整在二维码中间插入的图片的大小和位置

                logo = logo.convert("RGBA") #这里如果不是RGBA似乎会出错
                img.paste(logo, (rel_w, rel_h), logo) #将二维码和自己想添加的图片合成
            except:
                QMessageBox.about(self, 'Error', 'No Such a File')
        '''
        if self.text2.text():
            try:
                w, h = img.size
                text = self.text2.text()
                dr = ImageDraw.Draw(img)
                font = ImageFont.truetype(os.path.join("C:/Windows/Fonts", "simyou.ttf"), 50)
                dr.text(((w-180)/2,h-45),text,font=font,fill='#000000')
                #上述将字符串写道图片上

            except:
                QMessageBox.about(self, 'Error', 'No Such a File')    
        
        if self.text2.text() == None:
            pass

        try:
            img.save('{}'.format(self.text3.text())) #保存图片
            QMessageBox.about(self, 'Message', 'Successfully Created')
        except:
            QMessageBox.about(self, 'Error', 'Please Enter The Right Path')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qr = Qr_qt()
    sys.exit(app.exec_()) #主循环




