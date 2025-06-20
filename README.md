# 📚 Conversor PDF para Kindle

Uma solução completa e robusta para converter documentos PDF para formato nativo do Kindle (EPUB/MOBI), preservando **formatação**, **imagens**, **tabelas** e **estrutura** do documento original.

## ✨ Características Principais

- 🎯 **Preservação Total da Formatação**: Mantém fontes, tamanhos, negrito, itálico
- 📊 **Tabelas Intactas**: Extração e conversão inteligente de tabelas
- 🖼️ **Imagens Otimizadas**: Preserva imagens com otimização para e-readers
- 📏 **Espaçamento Original**: Mantém parágrafos, títulos e hierarquia
- 🔄 **Múltiplos Métodos**: Usa várias bibliotecas para máxima compatibilidade
- 📱 **Compatível com Kindle**: Formato otimizado para dispositivos Kindle

## 🚀 Instalação Rápida

### 1. Executar Setup Automático
```batch
# No Windows (PowerShell ou CMD)
setup.bat
```

### 2. Instalação Manual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## 📖 Como Usar

### Conversão Básica
```bash
python pdf_to_kindle.py "meu_documento.pdf"
```

### Opções Avançadas
```bash
# Especificar arquivo de saída
python pdf_to_kindle.py "documento.pdf" -o "livro.epub"

# Modo verboso (debug)
python pdf_to_kindle.py "documento.pdf" -v

# Formato específico
python pdf_to_kindle.py "documento.pdf" -f epub
```

### Uso em Código Python
```python
from pdf_to_kindle import PDFToKindleConverter

# Conversão simples
with PDFToKindleConverter("epub") as converter:
    output_file = converter.convert_pdf("documento.pdf")
    print(f"Arquivo convertido: {output_file}")

# Com opções customizadas
with PDFToKindleConverter("epub") as converter:
    output_file = converter.convert_pdf(
        pdf_path="documento.pdf",
        output_path="meu_livro.epub"
    )
```

## 🧪 Testar a Instalação

Execute o script de teste para verificar se tudo está funcionando:

```bash
python test_converter.py
```

Este script irá:
- ✅ Verificar todas as dependências
- 🔧 Testar as funcionalidades principais
- 📄 Criar um PDF de exemplo
- 🔄 Demonstrar a conversão completa

## 📦 Dependências

### Principais (Obrigatórias)
- **PyMuPDF**: Leitura e processamento de PDFs
- **EbookLib**: Criação de arquivos EPUB
- **Pillow**: Processamento de imagens
- **Pandas**: Manipulação de tabelas
- **BeautifulSoup4**: Processamento HTML

### Opcionais (Para Melhor Extração de Tabelas)
- **Camelot**: Extração avançada de tabelas
- **Tabula-py**: Alternativa para extração de tabelas
- **PDFPlumber**: Outra opção para tabelas complexas

## 🎯 Recursos Preservados

| Elemento | Status | Descrição |
|----------|--------|-----------|
| 📝 Texto | ✅ | Formatação completa (negrito, itálico, tamanhos) |
| 🖼️ Imagens | ✅ | Extraídas e otimizadas para e-readers |
| 📊 Tabelas | ✅ | Convertidas para HTML responsivo |
| 📏 Layout | ✅ | Espaçamento e estrutura hierárquica |
| 🎨 Fontes | ✅ | Tamanhos e estilos preservados |
| 📑 Páginas | ✅ | Quebras de página mantidas |

## 🔄 Conversão para MOBI

Para gerar arquivos MOBI (formato nativo mais antigo do Kindle):

1. **Instale o Calibre**: https://calibre-ebook.com/download
2. **Converta o EPUB gerado**:
```bash
ebook-convert "livro.epub" "livro.mobi"
```

O conversor gera EPUB por padrão, que é compatível com Kindles modernos e pode ser facilmente convertido para MOBI quando necessário.

## 📋 Estrutura do Projeto

```
kindle/
├── pdf_to_kindle.py      # Conversor principal
├── table_extractor.py   # Extração avançada de tabelas
├── test_converter.py    # Scripts de teste
├── requirements.txt     # Dependências Python
├── setup.bat           # Script de instalação Windows
└── README.md           # Esta documentação
```

## 🔧 Configurações Avançadas

### Otimização de Imagens
```python
from table_extractor import ImagePreserver

# Configurar qualidade das imagens
preserver = ImagePreserver(
    max_width=800,      # Largura máxima
    max_height=1200,    # Altura máxima
    quality=85          # Qualidade JPEG (0-100)
)
```

### Extração de Tabelas Personalizada
```python
from table_extractor import AdvancedTableExtractor

extractor = AdvancedTableExtractor()
tables = extractor.extract_tables_from_page("documento.pdf", page_num=0)
```

## ❗ Solução de Problemas

### Erro: "Python não encontrado"
- Instale Python 3.8+ de https://www.python.org/downloads/
- Certifique-se de adicionar Python ao PATH durante a instalação

### Erro: "Módulo não encontrado"
```bash
# Reativar ambiente virtual
venv\Scripts\activate

# Reinstalar dependências
pip install -r requirements.txt
```

### Tabelas não estão sendo extraídas corretamente
```bash
# Instalar bibliotecas opcionais para melhor extração
pip install camelot-py[cv] tabula-py pdfplumber
```

### Imagens com qualidade ruim
- Ajuste os parâmetros de qualidade no código
- Verifique se as imagens originais têm boa resolução

## 🆘 Suporte e Contribuições

### Relatando Problemas
1. Execute `python test_converter.py` para diagnóstico
2. Inclua a saída completa do erro
3. Mencione o tipo de PDF que está tentando converter

### Melhorias Sugeridas
- Adicione novos formatos de saída
- Melhore a detecção de estruturas específicas
- Otimize a performance para PDFs grandes

## 📄 Exemplo de Saída

Para um PDF com:
- Texto formatado
- Imagens
- Tabelas
- Títulos e subtítulos

O conversor produzirá um EPUB que mantém:
```
📖 Livro.epub
├── 📄 Página 1: Título principal + texto formatado
├── 🖼️ Imagens otimizadas e responsivas
├── 📊 Tabelas em HTML com bordas e formatação
└── 📑 Estrutura navegável para Kindle
```

## 🔮 Próximas Funcionalidades

- [ ] Suporte direto para MOBI (sem Calibre)
- [ ] Interface gráfica (GUI)
- [ ] Processamento em lote
- [ ] OCR para PDFs escaneados
- [ ] Reconhecimento avançado de layout
- [ ] Suporte para PDFs com múltiplas colunas

---

💡 **Dica**: Para melhores resultados, use PDFs com texto selecionável (não escaneados) e boa qualidade de imagem.

🎯 **Meta**: Preservar 100% da formatação e estrutura original do PDF no formato Kindle.
