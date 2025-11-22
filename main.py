"""
تطبيق مراقبة الفوركس - Forex Monitor
التطبيق الرئيسي
"""

import os
os.environ['KIVY_NO_CONSOLELOG'] = '1'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from database import Database
from monitor_engine import MonitorEngine
from datetime import datetime
import threading

# تعيين اتجاه النص من اليمين لليسار
Window.softinput_mode = "below_target"


class StatsCard(MDCard):
    """بطاقة الإحصائيات"""
    
    def __init__(self, title, value, subtitle, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(120)
        self.md_bg_color = [1, 1, 1, 1]  # أبيض
        self.elevation = 2
        self.radius = [10, 10, 10, 10]
        
        # القيمة الكبيرة
        value_label = MDLabel(
            text=str(value),
            font_style="H3",
            halign="center",
            theme_text_color="Custom",
            text_color=[0.1, 0.1, 0.1, 1]
        )
        self.add_widget(value_label)
        
        # العنوان
        title_label = MDLabel(
            text=subtitle,
            halign="center",
            theme_text_color="Secondary",
            font_size="14sp"
        )
        self.add_widget(title_label)


class SignalCard(MDCard):
    """بطاقة عرض الإشارة"""
    
    def __init__(self, signal, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = dp(15)
        self.spacing = dp(15)
        self.size_hint_y = None
        self.height = dp(90)
        self.md_bg_color = [1, 1, 1, 1]  # أبيض
        self.elevation = 2
        self.radius = [10, 10, 10, 10]
        
        # تحديد اللون والأيقونة
        if signal['signal_type'] == 'buy':
            icon_bg_color = [0.82, 0.98, 0.90, 1]  # أخضر فاتح
            icon_color = [0.06, 0.73, 0.51, 1]  # أخضر
            icon_name = "arrow-up-bold"
            signal_text = "إشارة شراء"
        else:
            icon_bg_color = [1.0, 0.89, 0.89, 1]  # أحمر فاتح
            icon_color = [0.94, 0.27, 0.27, 1]  # أحمر
            icon_name = "arrow-down-bold"
            signal_text = "إشارة بيع"
        
        # الأيقونة الدائرية
        icon_container = MDBoxLayout(
            size_hint_x=None,
            width=dp(50),
            md_bg_color=icon_bg_color,
            radius=[25, 25, 25, 25]
        )
        icon = MDIconButton(
            icon=icon_name,
            theme_text_color="Custom",
            text_color=icon_color,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        icon_container.add_widget(icon)
        self.add_widget(icon_container)
        
        # المحتوى
        content = MDBoxLayout(orientation='vertical', spacing=dp(3))
        
        # اسم الزوج
        pair_label = MDLabel(
            text=signal['pair_display_name'],
            font_style="H6",
            theme_text_color="Custom",
            text_color=[0.1, 0.1, 0.1, 1],
            size_hint_y=None,
            height=dp(20)
        )
        content.add_widget(pair_label)
        
        # نوع الإشارة والوقت
        time_ago = self.get_time_ago(signal['created_at'])
        signal_label = MDLabel(
            text=f"{signal_text} • {time_ago}",
            theme_text_color="Secondary",
            font_size="13sp",
            size_hint_y=None,
            height=dp(18)
        )
        content.add_widget(signal_label)
        
        # السعر والدقة
        details_label = MDLabel(
            text=f"السعر: {signal['price']:.5f}     دقة {signal['accuracy']:.1f}%     PF {signal['profit_factor']:.2f}",
            theme_text_color="Secondary",
            font_size="12sp",
            size_hint_y=None,
            height=dp(18)
        )
        content.add_widget(details_label)
        
        self.add_widget(content)
    
    def get_time_ago(self, timestamp):
        """حساب الوقت المنقضي"""
        now = datetime.now().timestamp() * 1000
        diff = now - timestamp
        
        seconds = diff / 1000
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        
        if days >= 1:
            return f"منذ {int(days)} يوم"
        elif hours >= 1:
            return f"منذ {int(hours)} ساعة"
        elif minutes >= 1:
            return f"منذ {int(minutes)} دقيقة"
        else:
            return "الآن"


class MainScreen(Screen):
    """الشاشة الرئيسية"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.engine = MonitorEngine()
        Clock.schedule_once(self.build_ui, 0.1)
    
    def build_ui(self, dt=None):
        """بناء الواجهة"""
        main_layout = MDBoxLayout(orientation='vertical')
        
        # شريط العنوان
        toolbar = MDTopAppBar(
            title="Forex Monitor",
            md_bg_color=[0.2, 0.6, 1.0, 1],  # أزرق
            right_action_items=[
                ["refresh", lambda x: self.refresh_signals()],
                ["cog", lambda x: setattr(self.manager, 'current', 'settings')]
            ],
            elevation=3
        )
        main_layout.add_widget(toolbar)
        
        # المحتوى القابل للتمرير
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView()
        
        content = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            padding=dp(15),
            spacing=dp(15)
        )
        
        # بطاقات الإحصائيات
        stats_container = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(120)
        )
        
        # عدد الأزواج
        stats_container.add_widget(
            StatsCard("أزواج", 10, "أزواج مراقبة نشطة")
        )
        
        # إشارات اليوم
        today_signals = self.get_today_signals_count()
        stats_container.add_widget(
            StatsCard("اليوم", today_signals, "إشارات اليوم")
        )
        
        # المراقبة النشطة
        stats_container.add_widget(
            StatsCard("نشط", 10, "أنظمة مراقبة")
        )
        
        content.add_widget(stats_container)
        
        # عنوان الإشارات
        signals_header = MDLabel(
            text="إشارات حديثة",
            font_style="H5",
            theme_text_color="Custom",
            text_color=[0.1, 0.1, 0.1, 1],
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(signals_header)
        
        signals_subtitle = MDLabel(
            text="آخر إشارات البيع والشراء المكتشفة",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(25)
        )
        content.add_widget(signals_subtitle)
        
        # قائمة الإشارات
        self.signals_container = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=dp(10)
        )
        content.add_widget(self.signals_container)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
        
        # تحميل الإشارات
        self.load_signals()
    
    def get_today_signals_count(self):
        """حساب عدد إشارات اليوم"""
        try:
            from datetime import datetime, timedelta
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_start_ts = int(today_start.timestamp() * 1000)
            
            signals = self.db.get_recent_signals(100)
            today_count = sum(1 for s in signals if s['created_at'] >= today_start_ts)
            return today_count
        except:
            return 0
    
    def load_signals(self):
        """تحميل الإشارات"""
        try:
            signals = self.db.get_recent_signals(10)
            
            self.signals_container.clear_widgets()
            
            if not signals:
                no_signals = MDLabel(
                    text="لا توجد إشارات حالياً",
                    halign="center",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height=dp(50)
                )
                self.signals_container.add_widget(no_signals)
            else:
                for signal in signals:
                    card = SignalCard(signal)
                    self.signals_container.add_widget(card)
        except Exception as e:
            print(f"خطأ في تحميل الإشارات: {str(e)}")
    
    def refresh_signals(self):
        """تحديث الإشارات"""
        Snackbar(text="جاري التحديث...").open()
        threading.Thread(target=self._refresh_thread, daemon=True).start()
    
    def _refresh_thread(self):
        """تحديث في الخلفية"""
        try:
            new_signals = self.engine.check_all_pairs()
            Clock.schedule_once(lambda dt: self._refresh_complete(new_signals), 0)
        except Exception as e:
            print(f"خطأ في التحديث: {str(e)}")
            Clock.schedule_once(lambda dt: Snackbar(text="فشل التحديث").open(), 0)
    
    def _refresh_complete(self, new_signals):
        """اكتمال التحديث"""
        self.load_signals()
        if new_signals:
            Snackbar(text=f"تم العثور على {len(new_signals)} إشارة جديدة").open()
        else:
            Snackbar(text="لا توجد إشارات جديدة").open()


class SettingsScreen(Screen):
    """شاشة الإعدادات"""
    pass


class AboutScreen(Screen):
    """شاشة عن التطبيق"""
    pass


class ForexMonitorApp(MDApp):
    """التطبيق الرئيسي"""
    
    def build(self):
        # تعيين السمة الفاتحة
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"  # وضع فاتح
        self.theme_cls.primary_hue = "500"
        
        # إنشاء مدير الشاشات
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(AboutScreen(name='about'))
        
        return sm


if __name__ == '__main__':
    ForexMonitorApp().run()
