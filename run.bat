@echo off
REM ================================================================================
REM  SCRIPT DE EJECUCIÓN - SISTEMA DE GESTIÓN DE TORNEOS DE TAEKWONDO
REM  Versión 1.0.0
REM ================================================================================

title Sistema de Gestion de Torneos - Iniciando...
color 0B

echo.
echo ================================================================================
echo   SISTEMA DE GESTION DE TORNEOS DE TAEKWONDO
echo   Iniciando aplicacion...
echo ================================================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python no esta instalado o no esta en PATH
    echo.
    echo Por favor instala Python 3.8 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo [OK] Python detectado
python --version
echo.

REM Verificar si pip está disponible
python -m pip --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] pip no esta disponible
    echo.
    echo Instalando pip...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
    echo.
)

echo [OK] pip disponible
python -m pip --version
echo.

REM Verificar si existe el archivo requirements.txt
if not exist "requirements.txt" (
    color 0C
    echo [ERROR] No se encuentra requirements.txt
    echo.
    echo Asegurate de ejecutar este script desde la carpeta del proyecto
    echo.
    pause
    exit /b 1
)

REM Verificar si las dependencias están instaladas
echo Verificando dependencias...
echo.

python -c "import kivy" >nul 2>&1
if errorlevel 1 (
    echo [INSTALANDO] Faltan dependencias. Instalando...
    echo.
    echo Esto puede tomar varios minutos la primera vez...
    echo.
    
    REM Actualizar pip primero
    python -m pip install --upgrade pip
    
    REM Instalar dependencias
    python -m pip install -r requirements.txt
    
    if errorlevel 1 (
        color 0C
        echo.
        echo [ERROR] No se pudieron instalar las dependencias
        echo.
        echo Soluciones posibles:
        echo 1. Ejecuta como Administrador
        echo 2. Instala Visual C++ Redistributable:
        echo    https://aka.ms/vs/17/release/vc_redist.x64.exe
        echo 3. Actualiza pip: python -m pip install --upgrade pip
        echo 4. Intenta instalar manualmente: pip install kivy requests websocket-client
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo [OK] Dependencias instaladas correctamente
    echo.
) else (
    echo [OK] Todas las dependencias ya estan instaladas
    echo.
)

REM Verificar que el backend esté accesible (opcional, no bloqueante)
echo Verificando conexion con el backend...
python -c "import requests; requests.get('http://localhost:8080', timeout=2)" >nul 2>&1
if errorlevel 1 (
    color 0E
    echo [ADVERTENCIA] No se puede conectar con el backend en http://localhost:8080
    echo.
    echo El sistema puede no funcionar correctamente sin el backend
    echo.
    echo Asegurate de que el servidor backend este corriendo antes de continuar
    echo.
    timeout /t 3 >nul
    color 0B
) else (
    echo [OK] Backend accesible
    echo.
)

REM Verificar que existe el archivo principal
if not exist "main.py" (
    color 0C
    echo [ERROR] No se encuentra main.py
    echo.
    echo Asegurate de ejecutar este script desde la carpeta del proyecto
    echo.
    pause
    exit /b 1
)

REM Verificar que existe el logo
if not exist "Imagen5-Photoroom.png" (
    color 0E
    echo [ADVERTENCIA] No se encuentra el archivo de logo: Imagen5-Photoroom.png
    echo.
    echo La aplicacion funcionara pero sin logo
    echo.
    timeout /t 2 >nul
)

REM Limpiar pantalla antes de ejecutar
cls

REM Ejecutar la aplicación
echo ================================================================================
echo   INICIANDO SISTEMA DE GESTION DE TORNEOS
echo ================================================================================
echo.
echo Si ves errores relacionados con WebSocket:
echo    - Ejecuta: pip install websocket-client
echo    - Las actualizaciones en tiempo real podrian no funcionar
echo.
echo Presiona Ctrl+C para detener la aplicacion
echo.
echo ================================================================================
echo.

REM Ejecutar con python
python main.py

REM Capturar el código de salida
if errorlevel 1 (
    color 0C
    echo.
    echo ================================================================================
    echo [ERROR] La aplicacion se cerro con errores
    echo ================================================================================
    echo.
    echo Errores comunes y soluciones:
    echo.
    echo 1. "No module named 'kivy'":
    echo    Solucion: pip install kivy==2.3.0
    echo.
    echo 2. "No module named 'websocket'":
    echo    Solucion: pip install websocket-client
    echo.
    echo 3. "Connection refused" / "No se pudo conectar":
    echo    Solucion: Verifica que el backend este corriendo en http://localhost:8080
    echo.
    echo 4. Error de compilacion/DLL en Windows:
    echo    Solucion: Instala Visual C++ Redistributable
    echo    https://aka.ms/vs/17/release/vc_redist.x64.exe
    echo.
    echo 5. "Permission denied":
    echo    Solucion: Ejecuta este script como Administrador
    echo.
    echo Para mas ayuda, consulta el archivo README.txt
    echo.
) else (
    color 0A
    echo.
    echo ================================================================================
    echo La aplicacion se cerro correctamente
    echo ================================================================================
    echo.
)

echo.
pause