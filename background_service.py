"""
خدمة الخلفية والجدولة
Background Service and Scheduler
"""

import schedule
import time
from datetime import datetime
from monitor_engine import MonitorEngine
from notifications import NotificationManager


class BackgroundService:
    """خدمة الخلفية للفحص التلقائي"""
    
    def __init__(self):
        self.engine = MonitorEngine()
        self.notifier = NotificationManager()
        self.is_running = False
    
    def daily_check(self):
        """الفحص اليومي"""
        print(f"\n{'='*60}")
        print(f"بدء الفحص اليومي المجدول - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        try:
            # فحص جميع الأزواج
            new_signals = self.engine.check_all_pairs()
            
            # إرسال الإشعارات
            if new_signals:
                print(f"\n🔔 إرسال {len(new_signals)} إشعار...")
                self.notifier.send_batch_notifications(new_signals)
            else:
                print("\nℹ️  لا توجد إشارات جديدة للإشعار")
            
            print(f"\n{'='*60}")
            print(f"انتهى الفحص اليومي")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"\n❌ خطأ في الفحص اليومي: {str(e)}\n")
    
    def start_scheduler(self):
        """بدء المجدول"""
        # جدولة الفحص اليومي عند 00:05 UTC
        schedule.every().day.at("00:05").do(self.daily_check)
        
        print("✓ تم تشغيل المجدول")
        print("⏰ الفحص اليومي مجدول عند 00:05 UTC (3:05 صباحاً بتوقيت السعودية)")
        
        self.is_running = True
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # فحص كل دقيقة
    
    def stop_scheduler(self):
        """إيقاف المجدول"""
        self.is_running = False
        print("✓ تم إيقاف المجدول")


def run_service():
    """تشغيل الخدمة"""
    service = BackgroundService()
    
    print("\n" + "="*60)
    print("خدمة مراقبة الفوركس - Background Service")
    print("="*60 + "\n")
    
    try:
        service.start_scheduler()
    except KeyboardInterrupt:
        print("\n\nإيقاف الخدمة...")
        service.stop_scheduler()
        print("تم إيقاف الخدمة بنجاح\n")


if __name__ == '__main__':
    run_service()
