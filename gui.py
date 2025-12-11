"""
n8n Tray - GUI Modülü
Bu modül ana pencere ve tüm GUI bileşenlerini oluşturur.
"""

from PyQt5 import QtWidgets, QtGui, QtCore
import styles


class MainWindow(QtWidgets.QWidget):
    """Ana pencere sınıfı"""
    
    def __init__(self, icon, process_manager):
        super().__init__()
        self.process_manager = process_manager
        self.init_ui(icon)
        
    def init_ui(self, icon):
        """UI'ı başlat"""
        self.setWindowTitle("n8n Control Panel")
        self.setWindowIcon(icon)
        self.setFixedSize(600, 520)
        self.setStyleSheet(styles.WINDOW_STYLE)
        
        # Ana layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        
        # Header
        self.create_header(layout)
        layout.addSpacing(10)
        
        # Status indicators
        self.create_status_indicators(layout)
        layout.addSpacing(12)
        
        # Butonlar
        self.create_buttons(layout)
        layout.addSpacing(8)
        
        # Emergency Kill butonu
        self.create_emergency_button(layout)
        layout.addSpacing(10)
        
        # Log alanı
        self.create_log_area(layout)
        
        self.setLayout(layout)
        self.update_status()
    
    def create_header(self, layout):
        """Header oluştur"""
        header = QtWidgets.QLabel("n8n Control Panel")
        header.setStyleSheet(styles.HEADER_STYLE)
        header.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(header)
    
    def create_status_indicators(self, layout):
        """Status indicator'ları oluştur"""
        status_container = QtWidgets.QWidget()
        status_layout = QtWidgets.QHBoxLayout(status_container)
        status_layout.setSpacing(12)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        self.n8n_status = QtWidgets.QLabel()
        self.cf_status = QtWidgets.QLabel()
        
        status_layout.addWidget(self.n8n_status)
        status_layout.addWidget(self.cf_status)
        layout.addWidget(status_container)
    
    def create_buttons(self, layout):
        """Butonları oluştur"""
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QGridLayout(button_container)
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        # n8n butonları
        btn_start_n8n = QtWidgets.QPushButton("n8n Başlat")
        btn_start_n8n.setStyleSheet(styles.BUTTON_STYLE_START)
        btn_start_n8n.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_start_n8n.clicked.connect(self.on_start_n8n)
        
        btn_stop_n8n = QtWidgets.QPushButton("n8n Durdur")
        btn_stop_n8n.setStyleSheet(styles.BUTTON_STYLE_STOP)
        btn_stop_n8n.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_stop_n8n.clicked.connect(self.on_stop_n8n)
        
        # Cloudflare butonları
        btn_start_cf = QtWidgets.QPushButton("Cloudflare Başlat")
        btn_start_cf.setStyleSheet(styles.BUTTON_STYLE_START)
        btn_start_cf.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_start_cf.clicked.connect(self.on_start_cloudflare)
        
        btn_stop_cf = QtWidgets.QPushButton("Cloudflare Durdur")
        btn_stop_cf.setStyleSheet(styles.BUTTON_STYLE_STOP)
        btn_stop_cf.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_stop_cf.clicked.connect(self.on_stop_cloudflare)
        
        # Grid'e ekle
        button_layout.addWidget(btn_start_n8n, 0, 0)
        button_layout.addWidget(btn_stop_n8n, 0, 1)
        button_layout.addWidget(btn_start_cf, 1, 0)
        button_layout.addWidget(btn_stop_cf, 1, 1)
        
        layout.addWidget(button_container)
    
    def create_emergency_button(self, layout):
        """Emergency kill butonu oluştur"""
        emergency_container = QtWidgets.QWidget()
        emergency_layout = QtWidgets.QHBoxLayout(emergency_container)
        emergency_layout.setContentsMargins(0, 0, 0, 0)
        emergency_layout.setSpacing(8)
        
        emergency_layout.addStretch()
        
        # Emergency kill button - sade stil
        btn_emergency_kill = QtWidgets.QPushButton("Kill All Node.js")
        btn_emergency_kill.setStyleSheet("""
            QPushButton {
                background: #3a3a3a;
                color: #b0b0b0;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #454545;
                border: 1px solid #555555;
            }
            QPushButton:pressed {
                background: #303030;
            }
        """)
        btn_emergency_kill.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_emergency_kill.clicked.connect(self.on_emergency_kill)
        emergency_layout.addWidget(btn_emergency_kill)
        
        emergency_layout.addStretch()
        
        layout.addWidget(emergency_container)
    
    def on_emergency_kill(self):
        """Emergency kill işlemi"""
        # Onay dialogu göster
        reply = QtWidgets.QMessageBox.warning(
            self,
            "Emergency Kill Node.js",
            "Tüm Node.js process'lerini zorla sonlandırmak istiyor musunuz?\n\n"
            "Bu işlem:\n"
            "• Tüm node.exe process'lerini öldürür\n"
            "• n8n ve diğer Node.js uygulamaları kapanır\n"
            "• Kaydedilmemiş veriler kaybolabilir\n\n"
            "NOT: Cloudflare tunnel etkilenmez.\n\n"
            "Devam etmek istiyor musunuz?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.process_manager.emergency_kill_all()
            self.update_status()
    
    def create_log_area(self, layout):
        """Log alanını oluştur"""
        # Log header ve butonlar
        log_header_container = QtWidgets.QWidget()
        log_header_layout = QtWidgets.QHBoxLayout(log_header_container)
        log_header_layout.setContentsMargins(0, 0, 0, 0)
        log_header_layout.setSpacing(8)
        
        log_header = QtWidgets.QLabel("Activity Log")
        log_header.setStyleSheet(styles.LOG_HEADER_STYLE)
        log_header_layout.addWidget(log_header)
        
        log_header_layout.addStretch()
        
        # Clear button
        btn_clear_log = QtWidgets.QPushButton("Clear")
        btn_clear_log.setStyleSheet("""
            QPushButton {
                background: #3a3a3a;
                color: #b0b0b0;
                border: 1px solid #444444;
                border-radius: 3px;
                padding: 4px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #454545;
            }
        """)
        btn_clear_log.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_clear_log.clicked.connect(self.clear_log)
        log_header_layout.addWidget(btn_clear_log)
        
        # Save button
        btn_save_log = QtWidgets.QPushButton("Save")
        btn_save_log.setStyleSheet("""
            QPushButton {
                background: #3a3a3a;
                color: #b0b0b0;
                border: 1px solid #444444;
                border-radius: 3px;
                padding: 4px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #454545;
            }
        """)
        btn_save_log.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_save_log.clicked.connect(self.save_log)
        log_header_layout.addWidget(btn_save_log)
        
        layout.addWidget(log_header_container)
        
        self.log_text = QtWidgets.QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(styles.LOG_TEXT_STYLE)
        self.log_text.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.log_text.customContextMenuRequested.connect(self.show_log_context_menu)
        layout.addWidget(self.log_text, 1)  # Stretch factor
    
    def show_log_context_menu(self, position):
        """Log için context menu göster"""
        menu = QtWidgets.QMenu()
        
        copy_action = menu.addAction("Copy All")
        clear_action = menu.addAction("Clear Log")
        menu.addSeparator()
        save_action = menu.addAction("Save to File...")
        
        action = menu.exec_(self.log_text.mapToGlobal(position))
        
        if action == copy_action:
            self.copy_log()
        elif action == clear_action:
            self.clear_log()
        elif action == save_action:
            self.save_log()
    
    def clear_log(self):
        """Log'u temizle"""
        self.log_text.clear()
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] Log temizlendi")
    
    def copy_log(self):
        """Log içeriğini kopyala"""
        from PyQt5.QtWidgets import QApplication
        QApplication.clipboard().setText(self.log_text.toPlainText())
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] Log panoya kopyalandı")
    
    def save_log(self):
        """Log'u dosyaya kaydet"""
        from PyQt5.QtWidgets import QFileDialog
        from datetime import datetime
        
        default_name = f"n8n_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Log File",
            default_name,
            "Text Files (*.txt);;All Files (*.*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.log_text.append(f"[{timestamp}] Log kaydedildi: {filename}")
            except Exception as e:
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.log_text.append(f"[{timestamp}] Hata: {str(e)}")
    
    def update_status(self):
        """Status indicator'ları güncelle"""
        # n8n status
        if self.process_manager.is_n8n_running():
            self.n8n_status.setText("n8n: Çalışıyor")
            self.n8n_status.setStyleSheet(styles.STATUS_RUNNING_STYLE)
        else:
            self.n8n_status.setText("n8n: Kapalı")
            self.n8n_status.setStyleSheet(styles.STATUS_STOPPED_STYLE)
        
        # Cloudflare status
        if self.process_manager.is_cloudflare_running():
            self.cf_status.setText("Cloudflare: Çalışıyor")
            self.cf_status.setStyleSheet(styles.STATUS_CF_RUNNING_STYLE)
        else:
            self.cf_status.setText("Cloudflare: Kapalı")
            self.cf_status.setStyleSheet(styles.STATUS_STOPPED_STYLE)
    
    def show_window(self):
        """Pencereyi göster"""
        self.show()
        self.raise_()
        self.activateWindow()
        self.update_status()
    
    # Button callbacks
    def on_start_n8n(self):
        self.process_manager.start_n8n()
        self.update_status()
    
    def on_stop_n8n(self):
        self.process_manager.stop_n8n()
        self.update_status()
    
    def on_start_cloudflare(self):
        self.process_manager.start_cloudflare()
        self.update_status()
    
    def on_stop_cloudflare(self):
        self.process_manager.stop_cloudflare()
        self.update_status()
