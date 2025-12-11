"""
n8n Tray - Stil Tanımlamaları
Bu modül tüm CSS stillerini ve renk paletini içerir.
"""

# Renk Paleti - Modern & Sade
COLORS = {
    'bg_primary': '#1e1e1e',
    'bg_secondary': '#2d2d2d',
    'bg_card': '#383838',
    'border': '#4a4a4a',
    'text_primary': '#e8e8e8',
    'text_secondary': '#a8a8a8',
    'accent_green': '#4ec9b0',
    'accent_red': '#f48771',
}

# Ana Pencere Stili
WINDOW_STYLE = """
    QWidget {
        background-color: #1e1e1e;
        color: #e8e8e8;
        font-family: 'Segoe UI', -apple-system, system-ui, sans-serif;
    }
"""

# Header Stili - Modern
HEADER_STYLE = """
    font-size: 18px;
    font-weight: 600;
    color: #e8e8e8;
    padding: 12px 0;
    border-bottom: 1px solid #383838;
    letter-spacing: -0.3px;
"""

# Status Indicator - Çalışıyor (Yeşil) - Modern Card
STATUS_RUNNING_STYLE = """
    color: #4ec9b0;
    font-size: 13px;
    font-weight: 500;
    padding: 10px 14px;
    background: #2d2d2d;
    border: 1px solid #4ec9b0;
    border-radius: 6px;
"""

# Status Indicator - Kapalı (Kırmızı) - Modern Card
STATUS_STOPPED_STYLE = """
    color: #f48771;
    font-size: 13px;
    font-weight: 500;
    padding: 10px 14px;
    background: #2d2d2d;
    border: 1px solid #f48771;
    border-radius: 6px;
"""

# Status Indicator - Cloudflare Çalışıyor
STATUS_CF_RUNNING_STYLE = STATUS_RUNNING_STYLE

# Buton Stili - Modern Minimal
BUTTON_STYLE_START = """
    QPushButton {
        background: #383838;
        color: #e8e8e8;
        border: 1px solid #4a4a4a;
        border-radius: 6px;
        padding: 10px 16px;
        font-size: 13px;
        font-weight: 500;
        min-height: 34px;
    }
    QPushButton:hover {
        background: #424242;
        border: 1px solid #5a5a5a;
    }
    QPushButton:pressed {
        background: #2d2d2d;
    }
"""

BUTTON_STYLE_STOP = BUTTON_STYLE_START

# Log Header Stili
LOG_HEADER_STYLE = """
    font-size: 13px;
    font-weight: 600;
    color: #a8a8a8;
    padding: 6px 0;
    letter-spacing: -0.2px;
"""

# Log Text Area Stili - Modern
LOG_TEXT_STYLE = """
    QTextEdit {
        background-color: #252525;
        color: #d4d4d4;
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        padding: 10px;
        font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
        font-size: 11px;
        line-height: 1.6;
    }
    QScrollBar:vertical {
        background: #252525;
        width: 12px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical {
        background: #4a4a4a;
        border-radius: 6px;
        min-height: 30px;
    }
    QScrollBar::handle:vertical:hover {
        background: #5a5a5a;
    }
"""
