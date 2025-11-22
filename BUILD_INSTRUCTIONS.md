# تعليمات بناء تطبيق Forex Monitor

## المتطلبات الأساسية

### على Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install -y python3-pip build-essential git zip unzip openjdk-17-jdk
sudo apt install -y python3-dev libffi-dev libssl-dev
sudo apt install -y autoconf libtool pkg-config zlib1g-dev libncurses5-dev
sudo apt install -y libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

### تثبيت Buildozer:
```bash
pip3 install --upgrade buildozer
pip3 install --upgrade cython
```

## خطوات البناء

### 1. التأكد من وجود جميع الملفات
```bash
cd forex_monitor
ls -la
```

يجب أن ترى:
- main.py
- database.py
- data_fetcher.py
- indicators.py
- monitor_engine.py
- notifications.py
- background_service.py
- buildozer.spec
- requirements.txt

### 2. تنظيف البناء السابق (اختياري)
```bash
buildozer android clean
```

### 3. بناء APK
```bash
buildozer android debug
```

**ملاحظة:** البناء الأول قد يستغرق 30-60 دقيقة لأنه سيقوم بتحميل:
- Android SDK
- Android NDK
- Python-for-Android
- جميع المكتبات المطلوبة

### 4. العثور على ملف APK
بعد اكتمال البناء، ستجد ملف APK في:
```
bin/forexmonitor-1.0-armeabi-v7a-debug.apk
```

## نقل APK إلى الهاتف

### الطريقة 1: USB
```bash
adb install bin/forexmonitor-1.0-armeabi-v7a-debug.apk
```

### الطريقة 2: نسخ الملف
انسخ ملف APK إلى هاتفك وقم بتثبيته مباشرة.

## استكشاف الأخطاء

### خطأ في البناء:
```bash
buildozer android logcat
```

### إعادة البناء بالكامل:
```bash
rm -rf .buildozer
buildozer android debug
```

### مشاكل الأذونات:
تأكد من منح التطبيق جميع الأذونات المطلوبة:
- الإنترنت
- الإشعارات
- الاهتزاز

## اختبار التطبيق

بعد التثبيت:
1. افتح التطبيق
2. انتظر تحميل البيانات
3. اضغط على زر التحديث لفحص الأزواج
4. تحقق من الإشعارات في الإعدادات

## ملاحظات مهمة

- التطبيق يحتاج اتصال إنترنت لجلب البيانات
- الفحص التلقائي يعمل عند 00:05 UTC يومياً
- الإشعارات تُرسل فقط عند ظهور إشارات جديدة
- لا يوجد تتبع أو إرسال بيانات لخوادم خارجية

## الدعم

للمشاكل التقنية، راجع:
- ملف README.md
- ملف المواصفات التقنية الأصلي
