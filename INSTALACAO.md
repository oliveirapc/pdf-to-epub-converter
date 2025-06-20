# 🚀 Guia de Instalação - Conversor PDF para Kindle

## ✅ Pré-requisitos

1. **Windows 10/11**
2. **Python 3.8 ou superior** instalado
   - Download: https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE**: Marque "Add Python to PATH" durante a instalação

## 📦 Instalação Automática

### Opção 1: Setup Completo (Recomendado)
```batch
# Execute o arquivo setup.bat
setup.bat
```

### Opção 2: Menu Interativo
```batch
# Execute o menu principal
converter_menu.bat
```

## 🔧 Instalação Manual

1. **Criar ambiente virtual**:
```batch
python -m venv venv
```

2. **Ativar ambiente virtual**:
```batch
venv\Scripts\activate
```

3. **Instalar dependências**:
```batch
pip install PyMuPDF EbookLib beautifulsoup4 Pillow pandas lxml pdfplumber tabula-py
```

## 🧪 Teste da Instalação

Execute o teste para verificar se tudo está funcionando:
```batch
venv\Scripts\activate
python test_converter.py
```

## 🎯 Como Usar

### Interface Menu (Mais Fácil)
```batch
converter_menu.bat
```

### Linha de Comando
```batch
# Ativar ambiente virtual
venv\Scripts\activate

# Conversão básica
python pdf_to_kindle.py "meu_documento.pdf"

# Com arquivo de saída específico
python pdf_to_kindle.py "documento.pdf" -o "livro.epub"

# Modo verboso (mostra detalhes)
python pdf_to_kindle.py "documento.pdf" -v
```

## 📚 Estrutura dos Arquivos

```
kindle/
├── 📄 pdf_to_kindle.py      # Conversor principal
├── 🔧 table_extractor.py   # Extração avançada de tabelas
├── ⚙️ config.py            # Configurações
├── 🧪 test_converter.py    # Scripts de teste
├── 📋 requirements.txt     # Dependências Python
├── 🖥️ setup.bat            # Instalação automática
├── 🎛️ converter_menu.bat   # Menu interativo
├── 📖 README.md            # Documentação
├── 📄 INSTALACAO.md        # Este arquivo
└── 📁 venv/                # Ambiente virtual Python
```

## 🎯 Funcionalidades Principais

### ✅ O que é preservado:
- ✅ **Formatação de texto** (negrito, itálico, tamanhos)
- ✅ **Imagens** (extraídas e otimizadas)
- ✅ **Tabelas** (convertidas para HTML)
- ✅ **Estrutura hierárquica** (títulos, subtítulos)
- ✅ **Espaçamento e parágrafos**
- ✅ **Layout original**

### 📱 Formatos Suportados:
- **Entrada**: PDF
- **Saída**: EPUB (compatível com Kindle moderno)
- **Conversão para MOBI**: Via Calibre (opcional)

## 🔄 Conversão para MOBI

Para gerar arquivos MOBI tradicionais:

1. **Instale o Calibre**: https://calibre-ebook.com/download
2. **Converta o EPUB**:
```batch
ebook-convert "livro.epub" "livro.mobi"
```

## ⚙️ Configurações Avançadas

### Qualidade de Imagem
Edite `config.py` para ajustar:
```python
IMAGE_SETTINGS = {
    'max_width': 800,      # Largura máxima
    'max_height': 1200,    # Altura máxima
    'quality': 85          # Qualidade (0-100)
}
```

### Extração de Tabelas
Para melhor detecção de tabelas, instale bibliotecas opcionais:
```batch
pip install camelot-py tabula-py pdfplumber
```

## 🆘 Solução de Problemas

### ❌ "Python não é reconhecido"
- Reinstale Python marcando "Add to PATH"
- Ou adicione manualmente ao PATH do Windows

### ❌ Erro de módulo não encontrado
```batch
# Reative o ambiente virtual
venv\Scripts\activate
# Reinstale dependências
pip install -r requirements.txt
```

### ❌ Tabelas não são detectadas
- Instale bibliotecas opcionais: `pip install camelot-py tabula-py`
- Use PDFs com tabelas bem definidas (não escaneados)

### ❌ Imagens com baixa qualidade
- Ajuste `quality` em `config.py`
- Use PDFs com imagens de alta resolução

### ❌ Texto mal formatado
- Certifique-se de que o PDF tem texto selecionável
- Para PDFs escaneados, use OCR antes da conversão

## 📞 Exemplos Práticos

### Exemplo 1: Documento Simples
```batch
python pdf_to_kindle.py "relatorio.pdf"
# Gera: relatorio.epub
```

### Exemplo 2: Livro Técnico
```batch
python pdf_to_kindle.py "manual_tecnico.pdf" -o "manual.epub" -v
# Gera: manual.epub com saída detalhada
```

### Exemplo 3: Via Python
```python
from pdf_to_kindle import PDFToKindleConverter

with PDFToKindleConverter("epub") as converter:
    output = converter.convert_pdf("documento.pdf")
    print(f"Arquivo gerado: {output}")
```

## 🎯 Dicas para Melhores Resultados

1. **Use PDFs com texto selecionável** (não escaneados)
2. **Prefira PDFs com boa qualidade** de imagem
3. **Tabelas funcionam melhor** quando bem delimitadas
4. **Para PDFs grandes**, use o modo verboso para acompanhar o progresso
5. **Para documentos técnicos**, configure qualidade de imagem mais alta

## 🔮 Próximas Funcionalidades

- [ ] Interface gráfica (GUI)
- [ ] Suporte direto para MOBI
- [ ] OCR integrado para PDFs escaneados
- [ ] Processamento em lote
- [ ] Detecção automática de capítulos

---

**💡 Dica**: Para usar regularmente, adicione a pasta do conversor ao PATH do Windows ou crie um atalho no desktop para `converter_menu.bat`.

**🎯 Objetivo**: Preservar 100% da formatação e estrutura do PDF no formato Kindle.
