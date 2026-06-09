@echo off
title SecData Peru - Inicio automatico
echo =====================================
echo   SecData Peru - Tablero local
echo =====================================
echo.

IF EXIST package.json (
    echo Proyecto con Node detectado.
    IF NOT EXIST node_modules (
        echo Instalando dependencias. Esto puede tardar unos minutos...
        call npm install
    )
    echo Iniciando servidor local en http://localhost:8080...
    start http://localhost:8080
    npm run dev
) ELSE (
    echo Proyecto HTML detectado.
    echo Abriendo archivo principal...
    start docs/index.html
)

pause
