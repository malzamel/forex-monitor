"""
نظام الإشعارات المحلية
Local Notifications System
"""

from plyer import notification
from database import Database
import platform


class NotificationManager:
    """مدير الإشعارات"""
    
    def __init__(self):
        self.db = Database()
        self.is_android = platform.system() == 'Linux' and 'ANDROID_ROOT' in os.environ if hasattr(os, 'environ') else False
    
    def send_signal_notification(self, signal):
        """
        إرسال إشعار لإشارة جديدة
        
        Args:
            signal: معلومات الإشارة
        """
        try:
            # التحقق من تفعيل الإشعارات
            notifications_enabled = self.db.get_setting('notifications_enabled', '1')
            if notifications_enabled != '1':
                print("⏭️  الإشعارات معطلة في الإعدادات")
                return
            
            # تحديد العنوان والرسالة
            signal_type_ar = "شراء 📈" if signal['signal_type'] == 'buy' else "بيع 📉"
            
            title = f"إشارة {signal_type_ar} - {signal['pair_display']}"
            
            message = (
                f"السعر: {signal['price']:.5f}\n"
                f"الدقة: {signal['accuracy']:.1f}%\n"
                f"عامل الربح: {signal['profit_factor']:.2f}\n"
                f"المؤشر: {signal['indicator_type']}"
            )
            
            # معلومات إضافية للأندرويد
            ticker = f"{signal['pair_display']}: {signal_type_ar}"
            
            # إرسال الإشعار
            try:
                notification.notify(
                    title=title,
                    message=message,
                    app_name='مراقب الفوركس',
                    app_icon=None,  # يمكن إضافة أيقونة لاحقاً
                    timeout=10,
                    ticker=ticker,
                    toast=True  # للأندرويد
                )
                print(f"✓ تم إرسال إشعار: {title}")
            except Exception as e:
                print(f"⚠️  خطأ في إرسال الإشعار (سيتم المحاولة مرة أخرى): {str(e)}")
                # محاولة بديلة بدون معاملات إضافية
                try:
                    notification.notify(
                        title=title,
                        message=message,
                        timeout=10
                    )
                    print(f"✓ تم إرسال إشعار (الطريقة البديلة): {title}")
                except:
                    print(f"❌ فشل إرسال الإشعار نهائياً")
            
            # تحديد الإشارة كمُرسلة
            if 'id' in signal:
                self.db.mark_signal_notified(signal['id'])
            
            # اهتزاز إذا كان مفعلاً
            vibrate_enabled = self.db.get_setting('vibrate_enabled', '1')
            if vibrate_enabled == '1':
                self.vibrate()
            
        except Exception as e:
            print(f"❌ خطأ عام في نظام الإشعارات: {str(e)}")
    
    def vibrate(self, duration=0.5):
        """
        اهتزاز الجهاز
        
        Args:
            duration: مدة الاهتزاز بالثواني
        """
        try:
            from plyer import vibrator
            vibrator.vibrate(duration)
        except Exception as e:
            print(f"⚠️  لا يمكن تفعيل الاهتزاز: {str(e)}")
    
    def send_batch_notifications(self, signals):
        """
        إرسال إشعارات لمجموعة من الإشارات
        
        Args:
            signals: قائمة الإشارات
        """
        if not signals:
            print("ℹ️  لا توجد إشارات للإشعار")
            return
        
        print(f"\n{'='*60}")
        print(f"📢 إرسال {len(signals)} إشعار...")
        print(f"{'='*60}\n")
        
        success_count = 0
        for i, signal in enumerate(signals, 1):
            print(f"[{i}/{len(signals)}] ", end="")
            try:
                self.send_signal_notification(signal)
                success_count += 1
            except Exception as e:
                print(f"❌ فشل إرسال الإشعار للإشارة {i}: {str(e)}")
        
        print(f"\n{'='*60}")
        print(f"✅ تم إرسال {success_count} من {len(signals)} إشعار بنجاح")
        print(f"{'='*60}\n")
    
    def test_notification(self):
        """
        اختبار الإشعارات
        """
        print("\n🔔 اختبار الإشعارات...\n")
        
        test_signal = {
            'pair_display': 'GBP/USD',
            'signal_type': 'buy',
            'price': 1.30940,
            'accuracy': 100.0,
            'profit_factor': 12.53,
            'indicator_type': 'StochRSI'
        }
        
        self.send_signal_notification(test_signal)
        print("\n✓ انتهى اختبار الإشعارات")


# للاستيراد
import os
