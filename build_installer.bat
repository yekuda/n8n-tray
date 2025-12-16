@echo off
chcp 65001 >nul
echo ========================================
echo n8n-Tray Installer Builder
echo ========================================
echo.

REM Renkli output için
color 0A

echo [1/4] Eski build dosyalarını temizleme...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
echo ✓ Temizleme tamamlandı
echo.

echo [2/4] PyInstaller ile EXE derleniyor...
pyinstaller n8n-Tray.spec --clean --noconfirm
if errorlevel 1 (
    color 0C
    echo ✗ EXE derleme başarısız!
    pause
    exit /b 1
)
echo ✓ EXE derleme tamamlandı
echo.

echo [3/4] Inno Setup ile Setup.exe oluşturuluyor...
REM Inno Setup'ın varsayılan kurulum yolları
set INNO_PATH1=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
set INNO_PATH2=C:\Program Files\Inno Setup 6\ISCC.exe
set INNO_PATH3=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe
set INNO_PATH4=%ProgramFiles%\Inno Setup 6\ISCC.exe

if exist "%INNO_PATH1%" (
    "%INNO_PATH1%" installer.iss
) else if exist "%INNO_PATH2%" (
    "%INNO_PATH2%" installer.iss
) else if exist "%INNO_PATH3%" (
    "%INNO_PATH3%" installer.iss
) else if exist "%INNO_PATH4%" (
    "%INNO_PATH4%" installer.iss
) else (
    color 0E
    echo.
    echo ⚠ Inno Setup bulunamadı!
    echo.
    echo Inno Setup'ı şu adresten indirin:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo İndirip kurduktan sonra bu scripti tekrar çalıştırın.
    echo.
    pause
    exit /b 1
)

if errorlevel 1 (
    color 0C
    echo ✗ Setup oluşturma başarısız!
    pause
    exit /b 1
)
echo ✓ Setup oluşturma tamamlandı
echo.

echo [4/4] Setup dosyası hazır!
echo.
echo ========================================
echo ✓ BAŞARILI!
echo ========================================
echo.
echo Setup dosyası: setup\n8n-Tray_Setup_v1.0.0.exe
echo.
echo Setup klasörünü açmak ister misiniz? (E/H)
choice /C EH /N /M "Seçiminiz: "
if errorlevel 2 goto end
if errorlevel 1 start explorer setup

:end
echo.
pause
