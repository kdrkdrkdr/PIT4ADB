
from typing import Text
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import uiautomator2 as ui
from time import sleep
import subprocess
import re, os, glob



d = ui.connect()

ext_storage = re.sub('[\t\n\r]', '', str(subprocess.check_output("utils\\adb.exe shell echo $EXTERNAL_STORAGE", shell=True).decode('utf-8')))


class RunTranslate(QThread):
    changeValue = Signal(int)

    def __init__(self, window):
        QThread.__init__(self)
        self.window = window
        

    def stop(self):
        self.terminate()


    def run(self):

        d.app_start('com.naver.labs.translator', stop=True)
        sleep(3)
        d.xpath('//*[@resource-id="com.naver.labs.translator:id/btn_ocr"]').click()
        sleep(1)

        


        src_dir = self.window.transed_file_dir.text().replace('/', '\\')

        imageTypes = ('jpg', 'png')
        imageList = []
        for ext in imageTypes:
            imageList.extend(glob.glob(f'{src_dir}\\*.{ext}'))


        if len(imageList) == 0:
            self.window.run_translate_btn.setText('번역하기')
            return


        for i, j in enumerate(imageList):

            srcLang = d.xpath('//*[@resource-id="com.naver.labs.translator:id/source_language_text"]')
            fLang = self.window.fromLang.currentText()

            if srcLang.text != fLang:
                srcLang.click()
                d().scroll.vert.toEnd()
                d(text=fLang).click()
            
            tgtLang = d.xpath('//*[@resource-id="com.naver.labs.translator:id/target_language_text"]')
            tLang = self.window.toLang.currentText()

            if tgtLang.text != tLang:
                tgtLang.click()
                d().scroll.vert.toEnd()
                d(text=tLang).click()



            src_path = f'{src_dir}\\{os.path.basename(j)}'
            dst_dir = f'{src_dir}\\PAPAGO_TRANSLATED'

            d.push(src=src_path, dst=f'{ext_storage}/Pictures/')
            d.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{ext_storage}/Pictures')

            d.xpath('//*[@resource-id="com.naver.labs.translator:id/btn_gallery"]').click()
            d.xpath('//*[@resource-id="com.android.documentsui:id/sub_menu"]').click()
            d.xpath('//*[@resource-id="com.android.documentsui:id/dir_list"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.ImageView[1]').click()
            d.xpath('//*[@resource-id="com.android.documentsui:id/option_menu_search"]').click()

            while not d(resourceId="com.naver.labs.translator:id/btn_save").exists: pass
            d(resourceId="com.naver.labs.translator:id/btn_save").click()
            d.xpath('//*[@text="저장하기"]').click()

            time_stamp = re.sub('[\D]', '', str(subprocess.check_output(f"utils\\adb.exe shell ls -l {ext_storage}/Pictures/papago_*", shell=True)).split(' ')[-1])
            transed_jpg = f'{ext_storage}/Pictures/papago_{time_stamp}.jpg'


            if not os.path.isdir(dst_dir): os.mkdir(dst_dir)
            
            d.pull(transed_jpg, f'{dst_dir}\\transed_{os.path.basename(j)}')

            d.shell(f'rm -rf {transed_jpg} {ext_storage}/Pictures/{os.path.basename(j)}')
            d.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{ext_storage}/Pictures')

            d.xpath('//*[@resource-id="com.naver.labs.translator:id/btn_back"]').click()

            self.window.f_log_browser.append(f'{dst_dir}\\transed_{os.path.basename(j)} 에 저장되었습니다.')
            self.changeValue.emit(int(100* (i+1)/len(imageList)))
            self.window.f_log_browser.verticalScrollBar().setValue(self.window.f_log_browser.verticalScrollBar().maximum())


        self.window.f_log_browser.append('\n번역 완료!')
        self.window.run_translate_btn.setText('번역하기')
        