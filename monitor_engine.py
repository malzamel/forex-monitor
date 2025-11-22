"""
محرك المراقبة الرئيسي
Main Monitoring Engine
"""

from data_fetcher import ForexDataFetcher
from indicators import TechnicalIndicators
from database import Database
from datetime import datetime


class MonitorEngine:
    """محرك المراقبة الرئيسي"""
    
    def __init__(self):
        self.fetcher = ForexDataFetcher()
        self.indicators = TechnicalIndicators()
        self.db = Database()
    
    def should_send_notification(self, pair_symbol, new_signal_type):
        """
        تحديد ما إذا كان يجب إرسال إشعار
        
        Args:
            pair_symbol: رمز الزوج
            new_signal_type: نوع الإشارة الجديدة ('buy' أو 'sell')
        
        Returns:
            True إذا كان يجب إرسال الإشعار
        """
        last_signal = self.db.get_last_signal(pair_symbol)
        
        # لا توجد إشارة سابقة - أرسل الإشعار
        if not last_signal:
            return True
        
        # نوع الإشارة مختلف عن السابقة - أرسل الإشعار
        if last_signal['type'] != new_signal_type:
            return True
        
        # نفس نوع الإشارة - لا ترسل
        return False
    
    def check_pair(self, pair_info):
        """
        فحص زوج واحد
        
        Args:
            pair_info: معلومات الزوج
        
        Returns:
            قائمة الإشارات الجديدة
        """
        pair_symbol = pair_info['symbol']
        pair_display = pair_info['display']
        
        print(f"فحص الزوج: {pair_display} ({pair_symbol})")
        
        # جلب البيانات
        candles = self.fetcher.fetch_forex_data(pair_symbol)
        if not candles:
            print(f"  ❌ فشل جلب البيانات")
            return []
        
        print(f"  ✓ تم جلب {len(candles)} شمعة")
        
        # تحليل الزوج
        analysis = self.indicators.analyze_pair(candles, pair_symbol)
        if not analysis:
            print(f"  ❌ فشل التحليل")
            return []
        
        current_price = analysis['current_price']
        new_signals = []
        
        # معالجة إشارة StochRSI
        if analysis['stochrsi_signal']:
            signal = analysis['stochrsi_signal']
            signal_type = signal['type']
            
            if self.should_send_notification(pair_symbol, signal_type):
                # إضافة الإشارة إلى قاعدة البيانات
                signal_id = self.db.add_signal(
                    pair_symbol=pair_symbol,
                    pair_display_name=pair_display,
                    signal_type=signal_type,
                    indicator_type='stochrsi',
                    price=current_price,
                    indicator_value=signal['value'],
                    accuracy=signal['accuracy'],
                    profit_factor=signal['profit_factor']
                )
                
                new_signals.append({
                    'id': signal_id,
                    'pair_symbol': pair_symbol,
                    'pair_display': pair_display,
                    'signal_type': signal_type,
                    'indicator_type': 'StochRSI',
                    'price': current_price,
                    'accuracy': signal['accuracy'],
                    'profit_factor': signal['profit_factor']
                })
                
                # تحديث حالة المراقبة
                self.db.update_monitoring_status(pair_symbol, signal_type, current_price)
                
                print(f"  🔔 إشارة StochRSI جديدة: {signal_type.upper()}")
            else:
                print(f"  ⏭️  إشارة StochRSI مكررة: {signal_type.upper()} (تم تجاهلها)")
        
        # معالجة إشارة MACD
        if analysis['macd_signal']:
            signal = analysis['macd_signal']
            signal_type = signal['type']
            
            if self.should_send_notification(pair_symbol, signal_type):
                # إضافة الإشارة إلى قاعدة البيانات
                signal_id = self.db.add_signal(
                    pair_symbol=pair_symbol,
                    pair_display_name=pair_display,
                    signal_type=signal_type,
                    indicator_type='macd',
                    price=current_price,
                    indicator_value=signal['histogram'],
                    accuracy=signal['accuracy'],
                    profit_factor=signal['profit_factor']
                )
                
                new_signals.append({
                    'id': signal_id,
                    'pair_symbol': pair_symbol,
                    'pair_display': pair_display,
                    'signal_type': signal_type,
                    'indicator_type': 'MACD',
                    'price': current_price,
                    'accuracy': signal['accuracy'],
                    'profit_factor': signal['profit_factor']
                })
                
                # تحديث حالة المراقبة
                self.db.update_monitoring_status(pair_symbol, signal_type, current_price)
                
                print(f"  🔔 إشارة MACD جديدة: {signal_type.upper()}")
            else:
                print(f"  ⏭️  إشارة MACD مكررة: {signal_type.upper()} (تم تجاهلها)")
        
        if not new_signals:
            print(f"  ℹ️  لا توجد إشارات جديدة")
        
        return new_signals
    
    def check_all_pairs(self):
        """
        فحص جميع الأزواج
        
        Returns:
            قائمة جميع الإشارات الجديدة
        """
        print("=" * 50)
        print(f"بدء الفحص اليومي - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        all_pairs = self.fetcher.get_all_pairs()
        all_new_signals = []
        
        for pair_info in all_pairs:
            try:
                signals = self.check_pair(pair_info)
                all_new_signals.extend(signals)
            except Exception as e:
                print(f"  ❌ خطأ في فحص الزوج {pair_info['display']}: {str(e)}")
        
        print("=" * 50)
        print(f"انتهى الفحص - عدد الإشارات الجديدة: {len(all_new_signals)}")
        print("=" * 50)
        
        # تنظيف الإشارات القديمة (أكثر من 30 يوم)
        deleted_count = self.db.clean_old_signals(30)
        if deleted_count > 0:
            print(f"تم حذف {deleted_count} إشارة قديمة")
        
        return all_new_signals
