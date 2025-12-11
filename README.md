# n8n Tray Control Panel

Bu uygulama, Windows System Tray (Bildirim Alanı) üzerinden n8n ve Cloudflare tünelini yönetmenizi sağlayan bir masaüstü aracıdır.

## Özellikler

- **n8n Yönetimi**: n8n'i başlatma ve durdurma.
- **Cloudflare Tunnel Yönetimi**: Cloudflare tünelini başlatma ve durdurma.
- **System Tray Entegrasyonu**: Uygulama arka planda çalışırken sistem tepsisinden kontrol edilebilir.
- **Şık Arayüz**: Modern ve karanlık mod arayüzü.
- **Process Takibi**: Çalışan işlemlerin loglarını görüntüleme.
- **Acil Durum (Emergency Kill)**: Takılı kalan Node.js işlemlerini tek tuşla temizleme.

## Gereksinimler

- Python 3.x
- `n8n` (Sistem yolunda (PATH) ekli olmalıdır)
- Cloudflare `cloudflared` (Varsayılan olarak `C:\Cloudflare\cloudflared.exe` konumunda beklenmektedir)

## Kurulum

1. Depoyu klonlayın veya indirin.
2. Gerekli Python kütüphanelerini yükleyin:

```bash
pip install -r requirements.txt
```

## Yapılandırma

**Önemli Not:** Uygulama şu anda Cloudflare `cloudflared.exe` dosyasını `C:\Cloudflare\cloudflared.exe` konumunda aramaktadır. Eğer `cloudflared` farklı bir konumdaysa, `process_manager.py` dosyasında aşağıdaki satırı düzenlemeniz gerekmektedir:

```python
# process_manager.py - Satır 135 civarı
[r"C:\Cloudflare\cloudflared.exe", "tunnel", "run", ...]
```

## Çalıştırma

Uygulamayı başlatmak için:

```bash
python app.py
```

## Dosyalar

- `app.py`: Ana giriş noktası.
- `gui.py`: Grafik arayüz kodları.
- `process_manager.py`: Arka plan işlem yönetimi.
- `tray_manager.py`: Sistem tepsisi simge yönetimi.
- `styles.py`: Arayüz stilleri.
- `icon.ico`: Uygulama simgesi.
