# إعداد GitHub Actions لبناء APK تلقائياً

## الخطوات البسيطة

### 1. إنشاء مستودع GitHub جديد

1. اذهب إلى https://github.com
2. سجّل الدخول أو أنشئ حساب
3. اضغط على **New repository** (أو الزر الأخضر)
4. املأ التفاصيل:
   - **Repository name**: `forex-monitor`
   - **Description**: تطبيق مراقبة الفوركس
   - **Public** أو **Private** (اختر ما تريد)
   - ✅ **Add a README file** (اختياري)
5. اضغط **Create repository**

### 2. رفع الكود إلى GitHub

#### الطريقة 1: عبر واجهة الويب (الأسهل)

1. في صفحة المستودع، اضغط **Add file** → **Upload files**
2. اسحب جميع الملفات من مجلد `forex_monitor` (ما عدا `.git`)
3. اكتب رسالة commit: "Initial commit"
4. اضغط **Commit changes**

#### الطريقة 2: عبر Git (للمتقدمين)

```bash
cd ~/Downloads/forex_monitor

# تهيئة Git
git init
git add .
git commit -m "Initial commit"

# ربط المستودع (استبدل USERNAME باسم المستخدم)
git remote add origin https://github.com/USERNAME/forex-monitor.git

# رفع الكود
git branch -M main
git push -u origin main
```

### 3. تفعيل GitHub Actions

GitHub Actions يعمل تلقائياً! بمجرد رفع الكود:

1. اذهب إلى تبويب **Actions** في المستودع
2. ستجد workflow يسمى "Build Android APK"
3. سيبدأ البناء تلقائياً (يستغرق 30-60 دقيقة)

### 4. تحميل APK

بعد انتهاء البناء:

#### من Artifacts:
1. اذهب إلى **Actions**
2. اضغط على آخر workflow ناجح (✅ علامة خضراء)
3. في الأسفل، تحت **Artifacts**، اضغط على `forex-monitor-apk`
4. حمّل الملف وفك الضغط
5. ثبّت APK على هاتفك

#### من Releases:
1. اذهب إلى تبويب **Releases**
2. حمّل APK من آخر إصدار
3. ثبّت على هاتفك مباشرة

### 5. البناء التلقائي

كل مرة تعدّل الكود وترفعه:
```bash
git add .
git commit -m "تحديث التطبيق"
git push
```

سيتم بناء APK جديد تلقائياً!

## المزايا

✅ **لا حاجة لتثبيت أي شيء محلياً**
✅ **البناء في السحابة (مجاناً)**
✅ **APK جاهز للتحميل مباشرة**
✅ **بناء تلقائي عند كل تحديث**
✅ **يعمل على أي نظام تشغيل**

## استكشاف الأخطاء

### إذا فشل البناء:
1. اذهب إلى **Actions**
2. اضغط على الworkflow الفاشل
3. اقرأ السجلات (logs) لمعرفة الخطأ
4. أصلح الخطأ وارفع الكود مرة أخرى

### إذا لم تجد Artifacts:
- تأكد أن الworkflow انتهى بنجاح (✅)
- انتظر حتى ينتهي البناء كاملاً
- Artifacts تبقى لمدة 30 يوم فقط

## ملاحظات

- البناء الأول يستغرق 45-60 دقيقة
- البناءات التالية أسرع (20-30 دقيقة)
- GitHub Actions مجاني للمستودعات العامة
- للمستودعات الخاصة: 2000 دقيقة مجاناً شهرياً

---

**هذا هو الحل الأسهل والأكثر موثوقية! ✨**
