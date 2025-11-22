[app]

# اسم التطبيق
title = Forex Monitor

# اسم الحزمة
package.name = forexmonitor

# نطاق الحزمة
package.domain = com.forexmonitor

# مجلد المصدر
source.dir = .

# امتدادات الملفات المضمنة
source.include_exts = py,png,jpg,kv,atlas,db

# الملفات المستبعدة
source.exclude_exts = spec

# الإصدار
version = 1.0

# المتطلبات
requirements = python3,kivy,kivymd,requests,schedule,pillow,android

# التوجه
orientation = portrait

# الخدمات
services = BackgroundService:background_service.py

# الأيقونة (اختياري)
#icon.filename = %(source.dir)s/data/icon.png

# شاشة البداية (اختياري)
#presplash.filename = %(source.dir)s/data/presplash.png

# الأذونات المطلوبة
android.permissions = INTERNET,WAKE_LOCK,VIBRATE,POST_NOTIFICATIONS,FOREGROUND_SERVICE,RECEIVE_BOOT_COMPLETED

# الميزات
# android.features = android.hardware.wifi

# API المستهدف
android.api = 33

# الحد الأدنى للـ API
android.minapi = 21

# NDK
android.ndk = 25b

# قبول رخصة SDK
android.accept_sdk_license = True

# الأرشيفة
android.archs = arm64-v8a,armeabi-v7a

# وضع الإصدار
android.release = False

# معلومات التطبيق
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# السماح بالنسخ الاحتياطي
android.allow_backup = True

# الموضوع
android.theme = @android:style/Theme.NoTitleBar

# Gradle dependencies (اختياري)
android.gradle_dependencies = 

# Java build options
android.add_src = 

# Whitelist
android.whitelist = 

# وضع p4a
p4a.branch = master

# Bootstrap
p4a.bootstrap = sdl2

# الأوامر قبل البناء
#android.ant_path = 

# الأوامر بعد البناء
#android.add_jars = 

# استخدام --private
fullscreen = 0

# سجل التطبيق
log_level = 2

# تحذيرات
warn_on_root = 1


[buildozer]

# سجل buildozer
log_level = 2

# مسار buildozer
#bin_dir = /home/user/.buildozer/android/platform/build/...
