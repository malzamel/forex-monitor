"""
اختبار سريع للتطبيق
"""

print("=" * 60)
print("اختبار تطبيق مراقبة الفوركس")
print("=" * 60)

# اختبار قاعدة البيانات
print("\n1. اختبار قاعدة البيانات...")
from database import Database
db = Database()
print("   ✓ قاعدة البيانات تعمل بنجاح")

# اختبار جلب البيانات
print("\n2. اختبار جلب البيانات...")
from data_fetcher import ForexDataFetcher
fetcher = ForexDataFetcher()
pairs = fetcher.get_all_pairs()
print(f"   ✓ تم تحميل {len(pairs)} زوج")

# اختبار المؤشرات
print("\n3. اختبار المؤشرات...")
from indicators import TechnicalIndicators
indicators = TechnicalIndicators()
print("   ✓ المؤشرات جاهزة")

# اختبار المحرك
print("\n4. اختبار المحرك...")
from monitor_engine import MonitorEngine
engine = MonitorEngine()
print("   ✓ المحرك جاهز")

# اختبار الإشعارات
print("\n5. اختبار الإشعارات...")
from notifications import NotificationManager
notifier = NotificationManager()
print("   ✓ نظام الإشعارات جاهز")

print("\n" + "=" * 60)
print("✅ جميع الاختبارات نجحت!")
print("=" * 60)
print("\nالتطبيق جاهز للاستخدام!")
print("لتشغيل التطبيق: python3 main.py")
print("=" * 60)
