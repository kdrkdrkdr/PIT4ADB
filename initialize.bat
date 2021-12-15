nox_adb install -r utils\Papago_base.apk
nox_adb install -r utils\ATX_base.apk
nox_adb push utils\atx-agent /data/local/tmp
nox_adb shell chmod 755 /data/local/tmp/atx-agent
nox_adb shell /data/local/tmp/atx-agent server -d