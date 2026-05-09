@echo off
title StockApp
color 0A
cls

echo.
echo  ==========================================
echo   StockApp - Sistema de Control de Stock
echo  ==========================================
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo  ERROR: No se encontro el entorno virtual .venv
    pause
    exit
)

echo  Activando entorno virtual...
call .venv\Scripts\activate.bat

echo  Aplicando migraciones...
python manage.py migrate --run-syncdb -v 0

echo  Verificando usuario admin...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@stockapp.com', 'admin1234')"

echo  Abriendo navegador...
timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000

echo.
echo  ==========================================
echo   StockApp corriendo en:
echo   http://127.0.0.1:8000
echo.
echo   Usuario: admin
echo   Password: admin1234
echo.
echo   Cerra esta ventana para detener
echo  ==========================================
echo.

python manage.py runserver 127.0.0.1:8000

pause