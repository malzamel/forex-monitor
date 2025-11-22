# تعليمات البناء النهائية - Forex Monitor APK

## المتطلبات
- Ubuntu 22.04 LTS
- اتصال إنترنت مستقر
- 4GB مساحة حرة على الأقل

## الخطوات (نسخ ولصق فقط)

### 1. تثبيت المتطلبات الأساسية

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv build-essential git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libffi-dev libssl-dev cmake ninja-build ccache
```

### 2. استخراج المشروع

```bash
cd ~/Downloads
tar -xzf forex_monitor_FINAL.tar.gz
cd forex_monitor
```

### 3. إنشاء البيئة الافتراضية

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. تثبيت Buildozer

```bash
pip install --upgrade pip
pip install --upgrade buildozer
pip install cython==0.29.36
```

### 5. بناء APK (سيستغرق 30-60 دقيقة)

```bash
buildozer -v android debug
```

**مهم:** لا تقاطع العملية! دعها تكمل حتى النهاية.

### 6. العثور على APK

```bash
ls -lh bin/*.apk
```

سيكون الملف:
```
bin/forexmonitor-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

## في حالة الأخطاء

### إذا ظهر خطأ pyjnius/long:
```bash
pip uninstall cython -y
pip install cython==0.29.36
buildozer android clean
buildozer -v android debug
```

### إذا ظهر خطأ distutils:
```bash
pip install setuptools
```

### إذا ظهر خطأ cmake:
```bash
sudo apt install cmake
```

## الملاحظات
- جميع الأخطاء السابقة تم إصلاحها
- الملف buildozer.spec محدّث
- ملف main.py مصلح (syntax error)
- المتطلبات محسّنة للتوافق

## بعد البناء الناجح

انسخ APK إلى هاتفك:
```bash
cp bin/*.apk ~/
```

ثم انقله إلى هاتف أندرويد وثبّته.

---

**تم الإصلاح والاختبار ✅**
