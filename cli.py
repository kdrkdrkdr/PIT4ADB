import uiautomator2 as ui
from time import sleep
import subprocess
import re, os



d = ui.connect()

d.app_start('com.naver.labs.translator', stop=True)
sleep(3)
d.xpath('//*[@resource-id="com.naver.labs.translator:id/btn_ocr"]').click()


src_dir = r'C:\Users\power\Desktop\Project\Dev\PIT4ADB\MyImages'


for i in os.listdir(src_dir):

    src_path = f'{src_dir}\\{i}'

    dst_dir = f'{src_dir}\\PAPAGO_TRANSLATED'

    d.push(src=src_path, dst='/sdcard/Pictures/')
    d.shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Pictures')

    d.xpath('//*[@resource-id="com.naver.labs.translator:id/btn_gallery"]').click()
    d.xpath('//*[@resource-id="com.android.documentsui:id/sub_menu"]').click()
    d.xpath('//*[@resource-id="com.android.documentsui:id/dir_list"]/android.widget.LinearLayout[1]').click()

    while not d(resourceId="com.naver.labs.translator:id/btn_save").exists: pass
    d(resourceId="com.naver.labs.translator:id/btn_save").click()
    d.xpath('//*[@text="저장하기"]').click()

    time_stamp = re.sub('[\D]', '', str(subprocess.check_output("utils\\adb.exe shell ls -l /sdcard/Pictures/papago_*", shell=True)).split(' ')[-1])
    transed_jpg = f'/sdcard/Pictures/papago_{time_stamp}.jpg'


    if not os.path.isdir(dst_dir): os.mkdir(dst_dir)

    d.pull(transed_jpg, f'{dst_dir}\\transed_{i}')

    d.shell(f'rm -rf {transed_jpg} /sdcard/Pictures/{i}')
    d.shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Pictures')

    d.xpath('//*[@resource-id="com.naver.labs.translator:id/btn_back"]').click()