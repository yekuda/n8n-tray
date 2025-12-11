"""
n8n Tray - Ana Uygulama
n8n ve Cloudflare tunnel'larını system tray'den yöneten uygulama.
"""

import sys

# __pycache__ oluşmasını engelle
sys.dont_write_bytecode = True

from PyQt5 import QtWidgets, QtGui

# Kendi modüllerimiz
import process_manager
from gui import MainWindow
from tray_manager import create_tray


def main():
    """Ana uygulama"""
    
    # Qt Uygulaması
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern görünüm
    
    # Dark Theme Palette - Modern
    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(30, 30, 30))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(232, 232, 232))
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(37, 37, 37))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(56, 56, 56))
    dark_palette.setColor(QtGui.QPalette.Text, QtGui.QColor(232, 232, 232))
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(56, 56, 56))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(232, 232, 232))
    app.setPalette(dark_palette)
    
    # Icon yükle
    icon = QtGui.QIcon("icon.ico")
    
    # Ana pencereyi oluştur
    window = MainWindow(icon, process_manager)
    
    # Process manager'a GUI referanslarını ver
    process_manager.set_gui_references(
        window.log_text,
        None,  # Tray henüz oluşturulmadı
        window.update_status
    )
    
    # System tray oluştur
    tray = create_tray(app, icon, process_manager, window.show_window)
    
    # Tray referansını process manager'a ver
    process_manager.tray = tray
    
    # Uygulamayı başlat
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
