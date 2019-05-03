import sys
from PyQt5.QtCore import QSize, QUrl,Qt
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5 import QtWidgets
from PyPDF2 import PdfFileReader, PdfFileMerger
import os


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi()
        self.pushButton.clicked.connect(self.addPdfFile)
        self.pushButton_2.clicked.connect(self.outputFile)
        self.pushButton_3.clicked.connect(self.deleteFile)
        self.gridState = False
        self.filesList = []
        self.fileroot  = ""

        icon = QIcon("Icon.ico")
        self.setWindowIcon(icon)

        box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "提示", "本软件使用GPL及Anti996协议！",
                                    QtWidgets.QMessageBox.NoButton, self)
        box.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
        self.pushButton_4 = QtWidgets.QPushButton()
        self.pushButton_4.clicked.connect(self.openurl)
        self.pushButton_4.setText("查看996icu")
        box.addButton(self.pushButton_4,QtWidgets.QMessageBox.AcceptRole)
        box.exec_()

    def setupUi(self):
        self.setObjectName("self")
        self.resize(600, 272)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("添加PDF")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("输出文件")
        self.verticalLayout.addWidget(self.pushButton_2)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.combox = QtWidgets.QComboBox(self)
        self.combox.setMinimumWidth(150)
        self.verticalLayout.addWidget(self.combox)
        self.pushButton_3 = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("删除文件")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.temLabel = QtWidgets.QLabel(self)
        self.temLabel.setText("点击左侧按钮添加PDF文件，请按顺序选取，可一次添加多个")
        self.temLabel.setMinimumWidth(350)
        self.temLabel.setAlignment(Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.temLabel)


    def addPdfFile(self):
        values, ok = QtWidgets.QFileDialog.getOpenFileNames(self, "读取pdf文件", self.fileroot, "PDF Files(*.pdf)")
        if ok and values:
            for value in values:
                pdfR2 = PdfFileReader(value)
                num = pdfR2.getNumPages()
                if not self.gridState:
                    self.initGridLayout()
                    self.gridState = True
                self.addGridItem(len(self.filesList)+1,value,0,num)


    def initGridLayout(self):
        self.horizontalLayout.removeWidget(self.temLabel)
        self.temLabel.clear()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        horLayout = QtWidgets.QHBoxLayout()
        label1 = QtWidgets.QLabel(self)
        label1.setText("文件名")
        label1.setMinimumWidth(350)
        horLayout.addWidget(label1)
        label2 = QtWidgets.QLabel(self)
        label2.setText("起始页")
        horLayout.addWidget(label2)
        label3 = QtWidgets.QLabel(self)
        label3.setText("终止页")
        horLayout.addWidget(label3)
        self.verticalLayout_2.addLayout(horLayout)
        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(self.spacerItem)

    def addGridItem(self, index, name, startpage, endpage):
        self.verticalLayout_2.removeItem(self.spacerItem)
        horLayout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
        label.setSizePolicy(sizePolicy)
        label.setMinimumSize(QSize(250, 0))
        filename = os.path.split(name)
        label.setText(filename[1])
        label.setMinimumWidth(350)
        self.combox.addItem(filename[1])
        self.fileroot = filename[0]
        horLayout.addWidget(label)

        spinBox = QtWidgets.QSpinBox(self)
        spinBox.setValue(startpage)
        horLayout.addWidget(spinBox)

        spinBox_2 = QtWidgets.QSpinBox(self)
        spinBox_2.setValue(endpage)
        horLayout.addWidget(spinBox_2)

        self.verticalLayout_2.addLayout(horLayout)
        self.verticalLayout_2.addItem(self.spacerItem)
        self.filesList.append({
            "spin1":spinBox,
            "spin2":spinBox_2,
            "label": label,
            "index": index,
            "name": name
        })


    def outputFile(self):
        if(len(self.filesList)):
            merge = PdfFileMerger()
            try:
                for item in self.filesList:
                    startnum = item["spin1"].value()
                    endnum = item["spin2"].value()
                    merge.append(item["name"],pages=(startnum,endnum))
                value, ok = QtWidgets.QFileDialog.getSaveFileName(self, "合成文件保存", self.fileroot,
                                                                  "PDF Files(*.pdf)")
                if value and ok:
                    with open(value,'wb') as wf:
                        merge.write(wf)
                    merge.close()
                    box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "提示", "成功输出文件！",
                                                QtWidgets.QMessageBox.NoButton, self)
                    box.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
                    box.exec_()
            except Exception as e:
                box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "出错了！", str(e),
                                            QtWidgets.QMessageBox.NoButton, self)
                box.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
                box.exec_()
        else:
            box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "提示", "请先选择要操作的文件！",
                                        QtWidgets.QMessageBox.NoButton, self)
            box.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
            box.exec_()

    def deleteFile(self):
        if(len(self.filesList)):
            index = self.combox.currentIndex()
            self.combox.removeItem(index)
            item = self.filesList.pop(index)
            item["label"].close()
            item["spin1"].close()
            item["spin2"].close()
            d = self.verticalLayout_2.takeAt(index+1)
            del d

    def openurl(self):
        QDesktopServices.openUrl(QUrl('https://github.com/996icu/996.ICU/'))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("PDF合并")
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
