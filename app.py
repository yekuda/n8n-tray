"""
n8n Tray - Ana Uygulama
n8n ve Cloudflare tunnel'larını system tray'den yöneten uygulama.
"""

import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# __pycache__ oluşmasını engelle
sys.dont_write_bytecode = True

from PyQt5 import QtWidgets, QtGui, QtCore, QtNetwork

# Kendi modüllerimiz
from process_manager import ProcessManager
from gui import MainWindow
from tray_manager import create_tray


def main():
    """Ana uygulama"""
    
    # Qt Uygulaması
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("n8n-tray")
    
    # Single Instance kontrolü - Sadece bir instance çalışabilir
    server_name = "n8n_tray_single_instance"
    socket = QtNetwork.QLocalSocket()
    socket.connectToServer(server_name)
    
    # Eğer başka bir instance varsa, ona sinyal gönder ve çık
    if socket.waitForConnected(500):
        # Başka instance'a mesaj gönder (pencereyi göster)
        socket.write(b"show")
        socket.flush()
        socket.waitForBytesWritten(1000)
        socket.disconnectFromServer()
        sys.exit(0)
    
    # İlk instance - Server oluştur
    local_server = QtNetwork.QLocalServer()
    local_server.removeServer(server_name)  # Eski server varsa temizle
    local_server.listen(server_name)
    
    # Eğer sistem tepsisi desteklenmiyorsa uyar (Opsiyonel ama iyi bir kontrol)
    if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
        QtWidgets.QMessageBox.critical(None, "Hata", "Sistem tepsisi bu sistemde desteklenmiyor.")
        sys.exit(1)

    app.setQuitOnLastWindowClosed(False) # Pencere kapanınca uygulamanın kapanmasını engelle (Tray için önemli)
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
    
    # Icon yükle (Resource path ile)
    icon_path = resource_path("icon.ico")
    icon = QtGui.QIcon(icon_path)
    app.setWindowIcon(icon) # Uygulama ikonu
    
    # Process manager instance oluştur
    process_manager = ProcessManager()
    
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
    
    # Başka instance'tan gelen istekleri dinle
    def on_new_connection():
        client = local_server.nextPendingConnection()
        if client and client.waitForReadyRead(1000):
            message = client.readAll().data()
            if message == b"show":
                # Pencereyi göster
                window.show_window()
    
    local_server.newConnection.connect(on_new_connection)
    
    # Uygulama başlarken pencereyi göster
    window.show_window()
    
    # Uygulamayı başlat
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
