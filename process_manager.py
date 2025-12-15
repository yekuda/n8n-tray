"""
n8n Tray - Process Yönetimi
Bu modül n8n ve Cloudflare process'lerini yönetir.
"""

import subprocess
import os
import threading
from PyQt5 import QtCore, QtWidgets


class LogSignalEmitter(QtCore.QObject):
    """Thread-safe log sinyali için yardımcı sınıf"""
    log_message = QtCore.pyqtSignal(str)


class ProcessManager:
    """Process yönetimi için class"""
    
    def __init__(self):
        self.n8n_process = None
        self.cloudflare_process = None
        
        # Signal emitter oluştur
        self.log_emitter = LogSignalEmitter()
        
        # GUI referansları
        self.log_text = None
        self.tray = None
        self.update_status_callback = None
    
    def set_gui_references(self, log_widget, tray_icon, status_callback):
        """GUI referanslarını ayarla"""
        self.log_text = log_widget
        self.tray = tray_icon
        self.update_status_callback = status_callback
        
        # Log sinyal bağlantısını kur
        self.log_emitter.log_message.connect(self._append_to_log)
    
    def log_append(self, text):
        """Log mesajı ekle (timestamp ile)"""
        if self.log_text:
            try:
                from datetime import datetime
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.log_emitter.log_message.emit(f"[{timestamp}] {text}")
            except Exception as e:
                print(f"Log append error: {e}")
    
    def _append_to_log(self, text):
        """Thread-safe log ekleme (main thread'de çalışır)"""
        if self.log_text:
            try:
                self.log_text.append(text)
                self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())
            except Exception as e:
                print(f"Log append error: {e}")
    
    def poll_process(self, proc, tag):
        """Process çıktılarını takip et"""
        try:
            while proc and proc.poll() is None:
                line = proc.stdout.readline()
                if line:
                    # Thread-safe sinyal emisyonu
                    self.log_emitter.log_message.emit(f"[{tag}] {line.strip()}")
            
            # Process doğal olarak kapandıysa bilgi ver
            if tag == "n8n":
                if self.n8n_process and self.n8n_process.poll() is not None:
                    self.n8n_process = None
                    self.log_emitter.log_message.emit("[n8n] Process beklenmedik şekilde kapandı")
            elif tag == "CF":
                if self.cloudflare_process and self.cloudflare_process.poll() is not None:
                    self.cloudflare_process = None
                    self.log_emitter.log_message.emit("[CF] Process beklenmedik şekilde kapandı")
            
            if self.update_status_callback:
                self.update_status_callback()
        except Exception as e:
            self.log_append(f"Poll process error: {e}")
    
    def start_n8n(self):
        """n8n'i başlat"""
        try:
            if self.n8n_process is None:
                env = dict(**os.environ)
                env["N8N_SECURE_COOKIE"] = "false"
                env["N8N_RUNNERS_ENABLED"] = "true"
                
                # PowerShell yerine doğrudan n8n komutunu çağırıyoruz
                # CREATE_NO_WINDOW bayrağı ile console penceresi açılmasını engelle
                self.n8n_process = subprocess.Popen(
                    "n8n",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    env=env,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                if self.tray:
                    self.tray.showMessage("n8n", "n8n başlatıldı", QtWidgets.QSystemTrayIcon.Information)
                
                self.log_append("n8n başlatıldı")
                threading.Thread(target=self.poll_process, args=(self.n8n_process, "n8n"), daemon=True).start()
                
                if self.update_status_callback:
                    self.update_status_callback()
            else:
                if self.tray:
                    self.tray.showMessage("n8n", "Zaten çalışıyor.", QtWidgets.QSystemTrayIcon.Warning)
                self.log_append("n8n zaten çalışıyor")
        except Exception as e:
            self.log_append(f"n8n başlatma hatası: {e}")
            if self.tray:
                self.tray.showMessage("Hata", f"n8n başlatılamadı: {e}", QtWidgets.QSystemTrayIcon.Critical)
    
    def stop_n8n(self):
        """n8n'i durdur"""
        if self.n8n_process:
            # Thread içinde durdur ki GUI donmasın
            threading.Thread(target=self._stop_n8n_worker, daemon=True).start()
        else:
            if self.tray:
                self.tray.showMessage("n8n", "n8n zaten kapalı.", QtWidgets.QSystemTrayIcon.Warning)
            self.log_append("n8n zaten kapalı")
    
    def _stop_n8n_worker(self):
        """n8n'i durduran worker thread"""
        try:
            if self.n8n_process:
                try:
                    # /F: Zorla kapat, /T: Alt processleri de kapat (Tree kill)
                    # CREATE_NO_WINDOW flag ekle
                    subprocess.call(
                        ['taskkill', '/F', '/T', '/PID', str(self.n8n_process.pid)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    self.n8n_process = None
                    self.log_append("n8n durduruldu (process tree temizlendi)")
                    
                    if self.update_status_callback:
                        self.update_status_callback()
                except Exception as e:
                    self.log_append(f"n8n durdurulurken hata: {e}")
        except Exception as e:
            self.log_append(f"n8n durdurma hatası: {e}")
    
    def start_cloudflare(self):
        """Cloudflare tunnel'ı başlat"""
        try:
            if self.cloudflare_process is None:
                # CREATE_NO_WINDOW bayrağı ile console penceresi açılmasını engelle
                self.cloudflare_process = subprocess.Popen(
                    [r"C:\Cloudflare\cloudflared.exe", "tunnel", "run", "--url", "http://localhost:5678", "n8n-pc"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                if self.tray:
                    self.tray.showMessage("Cloudflare", "Cloudflare başlatıldı", QtWidgets.QSystemTrayIcon.Information)
                
                self.log_append("Cloudflare başlatıldı")
                threading.Thread(target=self.poll_process, args=(self.cloudflare_process, "CF"), daemon=True).start()
                
                if self.update_status_callback:
                    self.update_status_callback()
            else:
                if self.tray:
                    self.tray.showMessage("Cloudflare", "Zaten açık.", QtWidgets.QSystemTrayIcon.Warning)
                self.log_append("Cloudflare zaten çalışıyor")
        except Exception as e:
            self.log_append(f"Cloudflare başlatma hatası: {e}")
            if self.tray:
                self.tray.showMessage("Hata", f"Cloudflare başlatılamadı: {e}", QtWidgets.QSystemTrayIcon.Critical)
    
    def stop_cloudflare(self):
        """Cloudflare tunnel'ı durdur"""
        if self.cloudflare_process:
            # Thread içinde durdur ki GUI donmasın
            threading.Thread(target=self._stop_cloudflare_worker, daemon=True).start()
        else:
            if self.tray:
                self.tray.showMessage("Cloudflare", "Zaten kapalı.", QtWidgets.QSystemTrayIcon.Warning)
            self.log_append("Cloudflare zaten kapalı")
    
    def _stop_cloudflare_worker(self):
        """Cloudflare'i durduran worker thread"""
        try:
            if self.cloudflare_process:
                try:
                    # Cloudflare için de process tree'yi temizle
                    # CREATE_NO_WINDOW flag ekle
                    subprocess.call(
                        ['taskkill', '/F', '/T', '/PID', str(self.cloudflare_process.pid)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    self.cloudflare_process = None
                    self.log_append("Cloudflare durduruldu (process tree temizlendi)")
                    
                    if self.update_status_callback:
                        self.update_status_callback()
                except Exception as e:
                    self.log_append(f"Cloudflare durdurulurken hata: {e}")
        except Exception as e:
            self.log_append(f"Cloudflare durdurma hatası: {e}")
    
    def is_n8n_running(self):
        """n8n çalışıyor mu?"""
        return self.n8n_process is not None
    
    def is_cloudflare_running(self):
        """Cloudflare çalışıyor mu?"""
        return self.cloudflare_process is not None
    
    def emergency_kill_all(self):
        """ACİL: Tüm node.exe process'lerini zorla sonlandır"""
        try:
            # node.exe process'lerini bul ve öldür
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq node.exe', '/FO', 'CSV', '/NH'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if 'node.exe' in result.stdout:
                subprocess.run(
                    ['taskkill', '/F', '/IM', 'node.exe'], 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                self.log_append("EMERGENCY: Tüm node.exe process'leri zorla sonlandırıldı")
                
                # Global değişkeni temizle
                self.n8n_process = None
                
                if self.update_status_callback:
                    self.update_status_callback()
                
                if self.tray:
                    self.tray.showMessage("Emergency Kill", "Tüm node.exe process'leri sonlandırıldı", QtWidgets.QSystemTrayIcon.Warning)
            else:
                self.log_append("Aktif node.exe process'i bulunamadı")
                if self.tray:
                    self.tray.showMessage("Emergency Kill", "Aktif node.exe bulunamadı", QtWidgets.QSystemTrayIcon.Information)
        
        except Exception as e:
            self.log_append(f"Emergency kill hatası: {e}")
            if self.tray:
                self.tray.showMessage("Hata", f"Emergency kill hatası: {e}", QtWidgets.QSystemTrayIcon.Critical)
