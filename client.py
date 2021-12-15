
from typing import Text
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import uiautomator2 as ui
from time import sleep
import subprocess
import re, os, glob



d = ui.connect()

adb_location = 'nox_adb'

ext_storage = re.sub('[\t\n\r]', '', str(subprocess.check_output(f"{adb_location} shell echo $EXTERNAL_STORAGE", shell=True).decode('utf-8')))

push_ori_dir = f'{ext_storage}/PIT4ADB_TEMP'
pull_transed_dir = f'{ext_storage}/papago'



class RunTranslate(QThread):
    changeValue = Signal(int)

    def __init__(self, window):
        QThread.__init__(self)
        self.window = window
        

    def stop(self):
        self.terminate()


    def run(self):

        os.system(f'{adb_location} shell rm -rf {push_ori_dir}')
        os.system(f'{adb_location} shell mkdir {push_ori_dir}')
        os.system(f'{adb_location} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{ext_storage}')
        sleep(3)

        d.app_start('com.naver.labs.translator', stop=True)
        sleep(5)
        d.xpath('//*[@resource-id="com.naver.labs.translator:id/btn_ocr"]').click()
        

        src_dir = self.window.transed_file_dir.text().replace('/', '\\')
        # src_dir = 'C:\\Users\\power\\Desktop\\Project\\Dev\\PIT4ADB\\MyImages'

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


            os.system(f'{adb_location} push {src_path} {push_ori_dir}/{os.path.basename(j)}')
            os.system(f'{adb_location} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{push_ori_dir}/{os.path.basename(j)}')
            # sleep(2)
            d.xpath('//*[@resource-id="com.naver.labs.translator:id/btn_gallery"]').click()


            d.xpath('//*[@content-desc="루트 표시"]').click()
            sleep(1)
            d.xpath('//*[@text="이미지"]').click()
            sleep(1)
            d.xpath('//*[@text="PIT4ADB_TEMP"]').click()

            try:
                k = d.xpath('//*[@resource-id="com.android.documentsui:id/menu_grid"]')
                if k.exists:
                    print(k.click())
            except:
                print("그냥 지나가라")

            sleep(1)
            d.xpath('//*[@resource-id="com.android.documentsui:id/dir_list"]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]').click()

            while not d(resourceId="com.naver.labs.translator:id/btn_save").exists: pass
            d(resourceId="com.naver.labs.translator:id/btn_save").click()
            d.xpath('//*[@text="저장하기"]').click()

            time_stamp = re.sub('[\D]', '', str(subprocess.check_output(f"{adb_location} shell ls -l {pull_transed_dir}/papago_*", shell=True)).split(' ')[-1])
            transed_jpg = f'{pull_transed_dir}/papago_{time_stamp}.jpg'


            if not os.path.isdir(dst_dir): os.mkdir(dst_dir)
            
            os.system(f'{adb_location} pull {transed_jpg} {dst_dir}\\transed_{os.path.basename(j)}')

            os.system(f'{adb_location} shell rm -rf {transed_jpg} {push_ori_dir}/{os.path.basename(j)}')

            os.system(f'{adb_location} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{transed_jpg}')
            os.system(f'{adb_location} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{push_ori_dir}/{os.path.basename(j)}')
            
            # sleep(2)
            d.xpath('//*[@resource-id="com.naver.labs.translator:id/btn_back"]').click()

            self.window.f_log_browser.append(f'{dst_dir}\\transed_{os.path.basename(j)} 에 저장되었습니다.')
            self.changeValue.emit(int(100* (i+1)/len(imageList)))
            self.window.f_log_browser.verticalScrollBar().setValue(self.window.f_log_browser.verticalScrollBar().maximum())


        self.window.f_log_browser.append('\n번역 완료!')
        self.window.run_translate_btn.setText('번역하기')
        