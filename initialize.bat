utils\adb install -r utils\ATX_base.apk
utils\adb push utils\atx-agent /data/local/tmp
utils\adb shell chmod 755 /data/local/tmp/atx-agent
utils\adb shell /data/local/tmp/atx-agent server -d