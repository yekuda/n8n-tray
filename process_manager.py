"""
n8n Tray - Process Yönetimi
Bu modül n8n ve Cloudflare process'lerini yönetir.
"""

import subprocess
import os
import threading
from PyQt5 import QtCore

# Global process variables
n8n_process = None
cloudflare_process = None

# GUI referansları (dışarıdan set edilecek)
log_text = None
tray = None
update_status_callback = None


def set_gui_references(log_widget, tray_icon, status_callback):
    """GUI referanslarını ayarla"""
    global log_text, tray, update_status_callback
    log_text = log_widget
    tray = tray_icon
    update_status_callback = status_callback


def log_append(text):
    """Log mesajı ekle (timestamp ile)"""
    if log_text:
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_text.append(f"[{timestamp}] {text}")
        log_text.verticalScrollBar().setValue(log_text.verticalScrollBar().maximum())


def poll_process(proc, tag):
    """Process çıktılarını takip et"""
    global n8n_process, cloudflare_process
    
    while proc and proc.poll() is None:
        line = proc.stdout.readline()
        if line:
            QtCore.QMetaObject.invokeMethod(
                log_text,
                "append",
                QtCore.Qt.QueuedConnection,
                QtCore.Q_ARG(str, f"[{tag}] {line.strip()}")
            )
    
    # Process doğal olarak kapandıysa bilgi ver
    if tag == "n8n":
        if n8n_process and n8n_process.poll() is not None:
            n8n_process = None
            QtCore.QMetaObject.invokeMethod(
                log_text, "append", QtCore.Qt.QueuedConnection,
                QtCore.Q_ARG(str, "[n8n] Process beklenmedik şekilde kapandı")
            )
    elif tag == "CF":
        if cloudflare_process and cloudflare_process.poll() is not None:
            cloudflare_process = None
            QtCore.QMetaObject.invokeMethod(
                log_text, "append", QtCore.Qt.QueuedConnection,
                QtCore.Q_ARG(str, "[CF] Process beklenmedik şekilde kapandı")
            )
    
    if update_status_callback:
        update_status_callback()


def start_n8n():
    """n8n'i başlat"""
    global n8n_process
    
    if n8n_process is None:
        env = dict(**os.environ)
        env["N8N_SECURE_COOKIE"] = "false"
        env["N8N_RUNNERS_ENABLED"] = "true"
        
        # PowerShell yerine doğrudan n8n komutunu çağırıyoruz
        n8n_process = subprocess.Popen(
            "n8n",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env
        )
        
        if tray:
            from PyQt5 import QtWidgets
            tray.showMessage("n8n", "n8n başlatıldı", QtWidgets.QSystemTrayIcon.Information)
        
        log_append("n8n başlatıldı")
        threading.Thread(target=poll_process, args=(n8n_process, "n8n"), daemon=True).start()
        
        if update_status_callback:
            update_status_callback()
    else:
        if tray:
            from PyQt5 import QtWidgets
            tray.showMessage("n8n", "Zaten çalışıyor.", QtWidgets.QSystemTrayIcon.Warning)


def stop_n8n():
    """n8n'i durdur"""
    global n8n_process
    
    if n8n_process:
        try:
            # /F: Zorla kapat, /T: Alt processleri de kapat (Tree kill)
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(n8n_process.pid)],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
            n8n_process = None
            log_append("n8n durduruldu (process tree temizlendi)")
            
            if update_status_callback:
                update_status_callback()
        except Exception as e:
            log_append(f"n8n durdurulurken hata: {e}")
    else:
        if tray:
            from PyQt5 import QtWidgets
            tray.showMessage("n8n", "n8n zaten kapalı.", QtWidgets.QSystemTrayIcon.Warning)


def start_cloudflare():
    """Cloudflare tunnel'ı başlat"""
    global cloudflare_process
    
    if cloudflare_process is None:
        cloudflare_process = subprocess.Popen(
            [r"C:\Cloudflare\cloudflared.exe", "tunnel", "run", "--url", "http://localhost:5678", "n8n-pc"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        if tray:
            from PyQt5 import QtWidgets
            tray.showMessage("Cloudflare", "Cloudflare başlatıldı", QtWidgets.QSystemTrayIcon.Information)
        
        log_append("Cloudflare başlatıldı")
        threading.Thread(target=poll_process, args=(cloudflare_process, "CF"), daemon=True).start()
        
        if update_status_callback:
            update_status_callback()
    else:
        if tray:
            from PyQt5 import QtWidgets
            tray.showMessage("Cloudflare", "Zaten açık.", QtWidgets.QSystemTrayIcon.Warning)


def stop_cloudflare():
    """Cloudflare tunnel'ı durdur"""
    global cloudflare_process
    
    if cloudflare_process:
        try:
            # Cloudflare için de process tree'yi temizle
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(cloudflare_process.pid)],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
            cloudflare_process = None
            log_append("Cloudflare durduruldu (process tree temizlendi)")
            
            if update_status_callback:
                update_status_callback()
        except Exception as e:
            log_append(f"Cloudflare durdurulurken hata: {e}")
    else:
        if tray:
            from PyQt5 import QtWidgets
            tray.showMessage("Cloudflare", "Zaten kapalı.", QtWidgets.QSystemTrayIcon.Warning)


def is_n8n_running():
    """n8n çalışıyor mu?"""
    return n8n_process is not None


def is_cloudflare_running():
    """Cloudflare çalışıyor mu?"""
    return cloudflare_process is not None


def emergency_kill_all():
    """ACİL: Tüm node.exe process'lerini zorla sonlandır"""
    global n8n_process
    
    try:
        # node.exe process'lerini bul ve öldür
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq node.exe', '/FO', 'CSV', '/NH'],
            capture_output=True,
            text=True
        )
        
        if 'node.exe' in result.stdout:
            subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
            log_append("EMERGENCY: Tüm node.exe process'leri zorla sonlandırıldı")
            
            # Global değişkeni temizle
            n8n_process = None
            
            if update_status_callback:
                update_status_callback()
            
            if tray:
                from PyQt5 import QtWidgets
                tray.showMessage("Emergency Kill", "Tüm node.exe process'leri sonlandırıldı", QtWidgets.QSystemTrayIcon.Warning)
        else:
            log_append("Aktif node.exe process'i bulunamadı")
            if tray:
                from PyQt5 import QtWidgets
                tray.showMessage("Emergency Kill", "Aktif node.exe bulunamadı", QtWidgets.QSystemTrayIcon.Information)
    
    except Exception as e:
        log_append(f"Emergency kill hatası: {e}")
        if tray:
            from PyQt5 import QtWidgets
            tray.showMessage("Hata", f"Emergency kill hatası: {e}", QtWidgets.QSystemTrayIcon.Critical)


