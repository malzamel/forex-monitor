"""
جلب بيانات الفوركس من Yahoo Finance
Forex Data Fetcher Module
"""

import requests
import json
from datetime import datetime


class ForexDataFetcher:
    """فئة جلب بيانات الفوركس"""
    
    BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"
    
    # قائمة الأزواج المراقبة
    PAIRS = [
        {'symbol': 'GBPUSD', 'display': 'GBP/USD', 'priority': 1},
        {'symbol': 'NZDUSD', 'display': 'NZD/USD', 'priority': 2},
        {'symbol': 'GBPJPY', 'display': 'GBP/JPY', 'priority': 3},
        {'symbol': 'USDJPY', 'display': 'USD/JPY', 'priority': 4},
        {'symbol': 'EURUSD', 'display': 'EUR/USD', 'priority': 5},
        {'symbol': 'AUDUSD', 'display': 'AUD/USD', 'priority': 6},
        {'symbol': 'USDCAD', 'display': 'USD/CAD', 'priority': 7},
        {'symbol': 'EURJPY', 'display': 'EUR/JPY', 'priority': 8},
        {'symbol': 'GBPAUD', 'display': 'GBP/AUD', 'priority': 9},
        {'symbol': 'USDCHF', 'display': 'USD/CHF', 'priority': 10}
    ]
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_forex_data(self, symbol, interval='1d', range_period='6mo'):
        """
        جلب بيانات الفوركس من Yahoo Finance
        
        Args:
            symbol: رمز الزوج (مثل GBPUSD)
            interval: الفترة الزمنية (1d للشموع اليومية)
            range_period: المدى الزمني (6mo لآخر 6 أشهر)
        
        Returns:
            قائمة الشموع أو None في حالة الخطأ
        """
        # إضافة =X إذا لم تكن موجودة
        if not symbol.endswith('=X'):
            symbol = f"{symbol}=X"
        
        url = f"{self.BASE_URL}{symbol}"
        params = {
            'interval': interval,
            'range': range_period
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            
            if response.status_code != 200:
                print(f"خطأ في API: {response.status_code} للزوج {symbol}")
                return None
            
            data = response.json()
            
            if not data.get('chart', {}).get('result'):
                print(f"لا توجد بيانات للزوج {symbol}")
                return None
            
            result = data['chart']['result'][0]
            timestamps = result.get('timestamp', [])
            quotes = result.get('indicators', {}).get('quote', [{}])[0]
            
            if not timestamps or not quotes:
                print(f"بيانات غير كاملة للزوج {symbol}")
                return None
            
            candles = []
            for i in range(len(timestamps)):
                close_price = quotes.get('close', [])[i] if i < len(quotes.get('close', [])) else None
                
                if close_price is not None:
                    candles.append({
                        'timestamp': timestamps[i] * 1000,  # تحويل إلى milliseconds
                        'open': quotes.get('open', [])[i] if i < len(quotes.get('open', [])) else close_price,
                        'high': quotes.get('high', [])[i] if i < len(quotes.get('high', [])) else close_price,
                        'low': quotes.get('low', [])[i] if i < len(quotes.get('low', [])) else close_price,
                        'close': close_price,
                        'volume': quotes.get('volume', [])[i] if i < len(quotes.get('volume', [])) else 0
                    })
            
            if len(candles) < 50:
                print(f"بيانات غير كافية للزوج {symbol}: {len(candles)} شمعة فقط")
                return None
            
            return candles
            
        except requests.Timeout:
            print(f"انتهت مهلة الطلب للزوج {symbol}")
            return None
        except Exception as e:
            print(f"خطأ في جلب البيانات للزوج {symbol}: {str(e)}")
            return None
    
    def get_all_pairs(self):
        """الحصول على قائمة جميع الأزواج"""
        return self.PAIRS
    
    def get_pair_info(self, symbol):
        """الحصول على معلومات زوج معين"""
        for pair in self.PAIRS:
            if pair['symbol'] == symbol:
                return pair
        return None
