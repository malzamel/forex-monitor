"""
قاعدة البيانات المحلية للتطبيق
Local Database Module
"""

import sqlite3
import os
from datetime import datetime, timedelta


class Database:
    def __init__(self, db_path='forex_monitor.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """إنشاء اتصال بقاعدة البيانات"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """إنشاء الجداول إذا لم تكن موجودة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول الإشارات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair_symbol TEXT NOT NULL,
                pair_display_name TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                indicator_type TEXT NOT NULL,
                price REAL NOT NULL,
                indicator_value REAL,
                accuracy REAL NOT NULL,
                profit_factor REAL NOT NULL,
                created_at INTEGER NOT NULL,
                is_notified INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_signals_pair ON signals(pair_symbol)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_signals_created ON signals(created_at DESC)')
        
        # جدول حالة المراقبة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitoring_status (
                pair_symbol TEXT PRIMARY KEY,
                last_checked INTEGER,
                last_signal_type TEXT,
                last_signal_at INTEGER,
                current_price REAL,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # جدول الإعدادات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        # إضافة الإعدادات الافتراضية
        default_settings = [
            ('notifications_enabled', '1'),
            ('check_time_utc', '00:05'),
            ('widget_size', 'medium'),
            ('language', 'ar'),
            ('show_stochrsi', '1'),
            ('show_macd', '1'),
            ('vibrate_enabled', '1'),
            ('sound_enabled', '1')
        ]
        
        for key, value in default_settings:
            cursor.execute('INSERT OR IGNORE INTO settings VALUES (?, ?)', (key, value))
        
        conn.commit()
        conn.close()
    
    def add_signal(self, pair_symbol, pair_display_name, signal_type, indicator_type, 
                   price, indicator_value, accuracy, profit_factor):
        """إضافة إشارة جديدة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        created_at = int(datetime.now().timestamp() * 1000)
        
        cursor.execute('''
            INSERT INTO signals 
            (pair_symbol, pair_display_name, signal_type, indicator_type, price, 
             indicator_value, accuracy, profit_factor, created_at, is_notified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        ''', (pair_symbol, pair_display_name, signal_type, indicator_type, price,
              indicator_value, accuracy, profit_factor, created_at))
        
        signal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return signal_id
    
    def get_last_signal(self, pair_symbol):
        """الحصول على آخر إشارة لزوج معين"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT signal_type, created_at 
            FROM signals 
            WHERE pair_symbol = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        ''', (pair_symbol,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {'type': result[0], 'timestamp': result[1]}
        return None
    
    def get_recent_signals(self, limit=10):
        """الحصول على آخر الإشارات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, pair_symbol, pair_display_name, signal_type, indicator_type,
                   price, indicator_value, accuracy, profit_factor, created_at
            FROM signals
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        signals = []
        for row in results:
            signals.append({
                'id': row[0],
                'pair_symbol': row[1],
                'pair_display_name': row[2],
                'signal_type': row[3],
                'indicator_type': row[4],
                'price': row[5],
                'indicator_value': row[6],
                'accuracy': row[7],
                'profit_factor': row[8],
                'created_at': row[9]
            })
        
        return signals
    
    def update_monitoring_status(self, pair_symbol, signal_type=None, price=None):
        """تحديث حالة المراقبة لزوج"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        current_time = int(datetime.now().timestamp() * 1000)
        
        cursor.execute('''
            INSERT OR REPLACE INTO monitoring_status 
            (pair_symbol, last_checked, last_signal_type, last_signal_at, current_price, status)
            VALUES (?, ?, ?, ?, ?, 'active')
        ''', (pair_symbol, current_time, signal_type, 
              current_time if signal_type else None, price))
        
        conn.commit()
        conn.close()
    
    def get_setting(self, key, default=None):
        """الحصول على إعداد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else default
    
    def set_setting(self, key, value):
        """تعيين إعداد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT OR REPLACE INTO settings VALUES (?, ?)', (key, str(value)))
        conn.commit()
        conn.close()
    
    def clean_old_signals(self, days=30):
        """حذف الإشارات القديمة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cutoff_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        
        cursor.execute('DELETE FROM signals WHERE created_at < ?', (cutoff_time,))
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def mark_signal_notified(self, signal_id):
        """تحديد إشارة كمُرسلة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE signals SET is_notified = 1 WHERE id = ?', (signal_id,))
        conn.commit()
        conn.close()
