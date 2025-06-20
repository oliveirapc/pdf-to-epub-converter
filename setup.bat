@echo off
echo ====================================
echo   Configurando Conversor PDF-Kindle
echo ====================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Por favor, instale Python 3.8+ antes de continuar.
    echo    Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Cria ambiente virtual se não existir
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erro ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtual criado
) else (
    echo ✅ Ambiente virtual já existe
)

echo.

REM Ativa ambiente virtual
echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualiza pip
echo 🔄 Atualizando pip...
python -m pip install --upgrade pip

REM Instala dependências
echo 📦 Instalando dependências...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)

echo.
echo ✅ Instalação concluída com sucesso!
echo.
echo 🚀 Para usar o conversor:
echo    1. Ative o ambiente virtual: venv\Scripts\activate.bat
echo    2. Execute: python pdf_to_kindle.py "caminho_do_arquivo.pdf"
echo.
echo 📖 Exemplos de uso:
echo    python pdf_to_kindle.py "documento.pdf"
echo    python pdf_to_kindle.py "documento.pdf" -o "livro.epub"
echo    python pdf_to_kindle.py "documento.pdf" -f epub -v
echo.
echo ℹ️  Para arquivos MOBI, instale também o Calibre:
echo    https://calibre-ebook.com/download
echo.
pause
