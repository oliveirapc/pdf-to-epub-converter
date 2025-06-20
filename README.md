# 📚 Conversor PDF para Kindle

Converte arquivos PDF para formato EPUB compatível com Kindle, preservando:
- ✅ **Tabelas** com formatação
- ✅ **Imagens** com posicionamento correto  
- ✅ **Texto** com formatação original
- ✅ **Layout** responsivo para e-readers

## 🚀 Instalação Rápida

```bash
# 1. Clone ou baixe o projeto
cd kindle

# 2. Execute o instalador automático
setup.bat

# 3. Teste a instalação
python test_final.py
```

## 📖 Como Usar

### Conversão Simples
```bash
python pdf_to_kindle_final.py "meu_documento.pdf"
```

### Com Opções
```bash
python pdf_to_kindle_final.py "arquivo.pdf" --output "kindle.epub" --verbose
```

## 📁 Arquivos Principais

- `pdf_to_kindle_final.py` - Conversor principal otimizado
- `requirements.txt` - Dependências necessárias  
- `setup.bat` - Instalador automático
- `test_final.py` - Teste de funcionamento

## 🔧 Dependências

- **PyMuPDF** - Processamento de PDF
- **EbookLib** - Criação de EPUB
- **Pillow** - Otimização de imagens
- **pandas** - Processamento de tabelas

## ✨ Recursos Principais

### 🖼️ Posicionamento de Imagens
- Extração com coordenadas exatas
- Posicionamento inteligente (esquerda/direita/centro)
- Otimização automática para Kindle

### 📊 Tabelas
- Extração automática com formatação
- Conversão para HTML responsivo
- Bordas e estilos preservados

### 📝 Texto
- Detecção de títulos e subtítulos
- Formatação (negrito, itálico) preservada
- Parágrafos com espaçamento correto

## 🎯 Exemplo de Uso

```python
from pdf_to_kindle_final import PDFToKindleConverter

# Conversão simples
with PDFToKindleConverter("epub") as converter:
    output_file = converter.convert_pdf("documento.pdf")
    print(f"Arquivo criado: {output_file}")
```

## 🐛 Solução de Problemas

### Erro de Dependências
```bash
pip install -r requirements.txt
```

### Erro de Permissão
- Execute como administrador
- Verifique se o arquivo PDF não está aberto

### Qualidade de Imagens
- Use PDFs com imagens em boa resolução
- Evite PDFs muito antigos ou corrompidos

## 📊 Estatísticas de Conversão

Após a conversão, você verá:
- 📄 Número de páginas processadas
- 🖼️ Quantidade de imagens incluídas  
- 📏 Tamanho do arquivo final
- ✅ Status de sucesso

## 🤝 Contribuições

Este é um projeto otimizado e finalizado. Para melhorias:
1. Faça um fork do repositório
2. Implemente suas modificações
3. Teste thoroughly
4. Envie pull request

## 📜 Licença

MIT License - Use livremente para projetos pessoais e comerciais.

---

**💡 Dica:** Para melhores resultados, use PDFs com texto pesquisável (não apenas imagens escaneadas).
