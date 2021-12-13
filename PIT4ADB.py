from UI_MAIN import Ui_MainWindow
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import qdarkstyle, os

from client import RunTranslate


languageList = ['한국어', '영어', '중국어(간체)', '일본어', '베트남어', '태국어', '중국어(번체)', '스페인어', '프랑스어', '인도네시아어', '러시아어', '독일어', '이탈리아어']


class PIT4ADB(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setFont(QFont('나눔고딕OTF', 10))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

        QObject.connect(self.select_file_dir_btn, SIGNAL('clicked()'), self.selectFiles)
        QObject.connect(self.open_file_dir_btn, SIGNAL('clicked()'), self.openFolder)
        QObject.connect(self.run_translate_btn, SIGNAL('clicked()'), self.runTrans)

        self.rt = RunTranslate(self)
        self.rt.changeValue.connect(self.progressBar.setValue)

        self.fromLang.addItems(['언어감지']+languageList)
        self.toLang.addItems(languageList)

        self.setWindowIcon(QIcon('./utils/sayo.ico'))

        self.show()




    def runTrans(self):
        if self.run_translate_btn.text() == '번역하기':
            self.f_log_browser.clear()
            self.rt.start()
            self.run_translate_btn.setText('번역중지')
        else:
            self.rt.stop()
            self.run_translate_btn.setText('번역하기')


    def selectFiles(self):
        dir_loc = QFileDialog.getExistingDirectory(self, 'Find Folder')
        if len(dir_loc) == 0:
            return
        self.transed_file_dir.setText(dir_loc)


    def openFolder(self):
        os.system('explorer \"{}\"'.format((self.transed_file_dir.text()).replace('/', '\\')))



if __name__ == '__main__':
    import sys
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    app = QApplication(sys.argv)
    pit4adb = PIT4ADB()
    app.exec_()