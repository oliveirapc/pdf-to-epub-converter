@echo off
title Conversor PDF para Kindle
color 0A

:menu
cls
echo.
echo ============================================
echo     CONVERSOR PDF PARA KINDLE
echo ============================================
echo.
echo 1. Converter PDF para EPUB
echo 2. Testar o conversor
echo 3. Ver exemplos de uso
echo 4. Instalar/Atualizar dependencias
echo 5. Abrir pasta de trabalho
echo 6. Sair
echo.
set /p choice="Escolha uma opcao (1-6): "

if "%choice%"=="1" goto convert
if "%choice%"=="2" goto test
if "%choice%"=="3" goto examples
if "%choice%"=="4" goto install
if "%choice%"=="5" goto opendir
if "%choice%"=="6" goto end
goto menu

:convert
cls
echo.
echo === CONVERSAO PDF PARA EPUB ===
echo.
set /p pdf_file="Digite o caminho completo do arquivo PDF: "
if not exist "%pdf_file%" (
    echo.
    echo ❌ Arquivo nao encontrado: %pdf_file%
    pause
    goto menu
)

echo.
echo Convertendo...
call venv\Scripts\activate && python pdf_to_kindle.py "%pdf_file%" -v

echo.
echo Conversao concluida!
pause
goto menu

:test
cls
echo.
echo === TESTE DO CONVERSOR ===
echo.
call venv\Scripts\activate && python test_converter.py
pause
goto menu

:examples
cls
echo.
echo === EXEMPLOS DE USO ===
echo.
echo Conversao basica:
echo   python pdf_to_kindle.py "documento.pdf"
echo.
echo Especificar arquivo de saida:
echo   python pdf_to_kindle.py "documento.pdf" -o "livro.epub"
echo.
echo Modo verboso:
echo   python pdf_to_kindle.py "documento.pdf" -v
echo.
echo Via linha de comando (ativando ambiente virtual):
echo   venv\Scripts\activate
echo   python pdf_to_kindle.py "documento.pdf"
echo.
echo Para arquivos MOBI (requer Calibre):
echo   1. Converta para EPUB primeiro
echo   2. Use: ebook-convert "livro.epub" "livro.mobi"
echo.
pause
goto menu

:install
cls
echo.
echo === INSTALACAO/ATUALIZACAO ===
echo.
echo Atualizando dependencias...
call venv\Scripts\activate && pip install --upgrade PyMuPDF EbookLib beautifulsoup4 Pillow pandas lxml pdfplumber tabula-py
echo.
echo Dependencias atualizadas!
pause
goto menu

:opendir
start explorer "%cd%"
goto menu

:end
echo.
echo Obrigado por usar o Conversor PDF-Kindle!
pause
exit
