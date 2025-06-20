# 📋 Changelog - Conversor PDF para Kindle

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [v2.0.0] - 2025-06-20 🎉

### ✨ Adicionado
- **Posicionamento correto de imagens** com coordenadas exatas
- **Ordenação inteligente** de elementos por posição Y
- **CSS otimizado** para dispositivos Kindle
- **Context manager** para limpeza automática de recursos
- **Interface simplificada** com arquivo único principal
- **Testes eficazes** com validação completa
- **.gitignore** para manter repositório limpo

### 🔧 Corrigido
- **Problema principal**: Imagens apareciam fora de posição
- **Extração de imagens** com `get_image_rects()` para posição precisa
- **Fluxo de texto** respeitando posicionamento original
- **Referências de imagem** no HTML/EPUB
- **Inclusão de imagens** no arquivo final

### 🚀 Melhorado
- **Performance**: Processamento mais eficiente
- **Qualidade**: Otimização automática de imagens
- **Usabilidade**: Comando único para conversão
- **Robustez**: Tratamento completo de erros
- **Manutenibilidade**: Código limpo e documentado

### 🗑️ Removido
- Arquivos duplicados e versões antigas
- Configurações complexas desnecessárias
- Dependências externas complexas
- Código experimental e temporário
- Testes redundantes

### 📊 Estatísticas
- **Redução de 60%** no número de arquivos
- **24.6KB** de código principal otimizado
- **Zero dependências** externas complexas
- **100%** das funcionalidades preservadas

---

## [v1.0.0] - 2025-06-17 🚀

### ✨ Primeira versão
- Conversor básico PDF para EPUB
- Extração de texto, imagens e tabelas
- Configurações personalizáveis
- Múltiplos métodos de extração
- Testes iniciais

### 🎯 Recursos principais
- Suporte para tabelas complexas
- Otimização de imagens
- Preservação de formatação
- Metadados e navegação
- CSS para e-readers

---

## 🔮 Próximas versões planejadas

### v2.1.0 (Futuro)
- [ ] Detecção automática de colunas
- [ ] Reconhecimento de legendas
- [ ] OCR opcional para PDFs escaneados
- [ ] Suporte para múltiplos idiomas

### v2.2.0 (Futuro)
- [ ] Interface gráfica opcional
- [ ] Processamento em lote
- [ ] Configurações avançadas via GUI
- [ ] Preview do resultado

---

## 📝 Formato das versões

- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Funcionalidades adicionadas de forma compatível
- **PATCH**: Correções de bugs compatíveis

## 🤝 Como contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
