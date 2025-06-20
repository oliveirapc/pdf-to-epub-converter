"""
Configurações do Conversor PDF-Kindle
"""

# Configurações de qualidade de imagem
IMAGE_SETTINGS = {
    'max_width': 800,           # Largura máxima das imagens
    'max_height': 1200,         # Altura máxima das imagens
    'quality': 85,              # Qualidade JPEG (0-100)
    'optimize': True,           # Otimizar compressão
    'format': 'JPEG'            # Formato padrão para imagens
}

# Configurações de extração de tabelas
TABLE_SETTINGS = {
    'min_confidence': 60,       # Confiança mínima para Camelot
    'edge_tol': 50,            # Tolerância para bordas da tabela
    'row_tol': 2,              # Tolerância para linhas
    'column_tol': 0,           # Tolerância para colunas
    'strip_text': '\n',        # Caracteres a remover do texto
    'split_text': False,       # Dividir texto em células
    'flag_size': True          # Marcar tabelas por tamanho
}

# Configurações de formatação de texto
TEXT_SETTINGS = {
    'font_size_threshold': {
        'title': 16,           # Tamanho mínimo para títulos principais
        'subtitle': 14,        # Tamanho mínimo para subtítulos
        'body': 12             # Tamanho padrão do corpo
    },
    'paragraph_spacing': 1.5,  # Espaçamento entre parágrafos
    'line_height': 1.4,        # Altura da linha
    'preserve_whitespace': True # Preservar espaços em branco
}

# Configurações do EPUB
EPUB_SETTINGS = {
    'language': 'pt-br',       # Idioma padrão
    'creator': 'PDF-Kindle Converter',
    'publisher': 'Convertido automaticamente',
    'add_toc': True,           # Adicionar índice
    'chapter_break': 'page',   # Quebra de capítulo (page/none)
    'css_style': '''
        body { 
            font-family: serif; 
            margin: 20px; 
            line-height: 1.4; 
        }
        .page { 
            page-break-after: always; 
            margin-bottom: 30px; 
        }
        .title { 
            font-size: 1.5em; 
            font-weight: bold; 
            margin: 20px 0; 
            text-align: center; 
        }
        .subtitle { 
            font-size: 1.2em; 
            font-weight: bold; 
            margin: 15px 0; 
        }
        .paragraph { 
            margin: 10px 0; 
            text-align: justify; 
        }
        .kindle-table { 
            border-collapse: collapse; 
            width: 100%; 
            margin: 15px 0; 
            font-size: 0.9em; 
        }
        .kindle-table th, .kindle-table td { 
            border: 1px solid #333; 
            padding: 8px; 
            text-align: left; 
        }
        .kindle-table th { 
            background-color: #f0f0f0; 
            font-weight: bold; 
        }
        .image-container { 
            text-align: center; 
            margin: 20px 0; 
        }
        .image-container img { 
            max-width: 100%; 
            height: auto; 
            border: 1px solid #ddd; 
        }
        .image-caption { 
            font-size: 0.9em; 
            font-style: italic; 
            margin-top: 5px; 
            color: #666; 
        }
    '''
}

# Configurações de logging
LOGGING_SETTINGS = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_output': False,      # Salvar logs em arquivo
    'max_log_size': '10MB'     # Tamanho máximo do arquivo de log
}

# Configurações de performance
PERFORMANCE_SETTINGS = {
    'max_pages_per_batch': 10,  # Páginas processadas por vez
    'enable_multiprocessing': False,  # Processamento paralelo (experimental)
    'memory_limit_mb': 512,     # Limite de memória por processo
    'temp_cleanup': True        # Limpar arquivos temporários automaticamente
}

# Configurações específicas por formato
FORMAT_SETTINGS = {
    'epub': {
        'compression': True,
        'embed_fonts': False,
        'split_chapters': True
    },
    'mobi': {
        'compression': True,
        'kindlegen_path': None,  # Caminho para kindlegen (se disponível)
        'cover_image': None      # Caminho para imagem de capa
    }
}

# Configurações de detecção de elementos
DETECTION_SETTINGS = {
    'detect_headers': True,     # Detectar cabeçalhos automaticamente
    'detect_footers': True,     # Detectar rodapés automaticamente
    'detect_columns': True,     # Detectar texto em colunas
    'detect_lists': True,       # Detectar listas (bullets, números)
    'merge_lines': True,        # Juntar linhas quebradas
    'remove_hyphenation': True  # Remover hifenização
}

# Mensagens do usuário
MESSAGES = {
    'start_conversion': "🔄 Iniciando conversão de {input_file}...",
    'processing_page': "📄 Processando página {current}/{total}...",
    'extracting_images': "🖼️ Extraindo imagens da página {page}...",
    'extracting_tables': "📊 Extraindo tabelas da página {page}...",
    'creating_epub': "📚 Criando arquivo EPUB...",
    'conversion_complete': "✅ Conversão concluída: {output_file}",
    'error_occurred': "❌ Erro durante a conversão: {error}",
    'file_not_found': "❌ Arquivo não encontrado: {file_path}",
    'invalid_format': "❌ Formato não suportado: {format}",
    'missing_dependency': "⚠️ Dependência opcional não encontrada: {dependency}"
}

# Validação de configurações
def validate_settings():
    """Valida se todas as configurações estão corretas"""
    errors = []
    
    # Valida configurações de imagem
    if not (0 <= IMAGE_SETTINGS['quality'] <= 100):
        errors.append("IMAGE_SETTINGS['quality'] deve estar entre 0 e 100")
    
    if IMAGE_SETTINGS['max_width'] <= 0 or IMAGE_SETTINGS['max_height'] <= 0:
        errors.append("Dimensões de imagem devem ser positivas")
    
    # Valida configurações de tabela
    if not (0 <= TABLE_SETTINGS['min_confidence'] <= 100):
        errors.append("TABLE_SETTINGS['min_confidence'] deve estar entre 0 e 100")
    
    # Valida configurações de texto
    font_sizes = TEXT_SETTINGS['font_size_threshold']
    if not (font_sizes['body'] <= font_sizes['subtitle'] <= font_sizes['title']):
        errors.append("Tamanhos de fonte devem estar em ordem crescente: body <= subtitle <= title")
    
    if errors:
        raise ValueError("Erros de configuração encontrados:\n" + "\n".join(f"- {error}" for error in errors))
    
    return True

# Função para carregar configurações de arquivo externo (se existir)
def load_user_config(config_file='config.json'):
    """Carrega configurações personalizadas do usuário"""
    import json
    import os
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            
            # Atualiza configurações globais com as do usuário
            globals().update(user_config)
            return True
            
        except Exception as e:
            print(f"Erro ao carregar configurações personalizadas: {e}")
    
    return False

# Função para salvar configurações padrão
def save_default_config(config_file='config.json'):
    """Salva as configurações atuais em um arquivo JSON"""
    import json
    
    config_data = {
        'IMAGE_SETTINGS': IMAGE_SETTINGS,
        'TABLE_SETTINGS': TABLE_SETTINGS,
        'TEXT_SETTINGS': TEXT_SETTINGS,
        'EPUB_SETTINGS': EPUB_SETTINGS,
        'LOGGING_SETTINGS': LOGGING_SETTINGS,
        'PERFORMANCE_SETTINGS': PERFORMANCE_SETTINGS,
        'FORMAT_SETTINGS': FORMAT_SETTINGS,
        'DETECTION_SETTINGS': DETECTION_SETTINGS
    }
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Configurações salvas em {config_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar configurações: {e}")
        return False

# Inicialização
if __name__ == "__main__":
    # Valida configurações na importação
    validate_settings()
    
    # Tenta carregar configurações personalizadas
    load_user_config()
    
    print("📋 Configurações carregadas com sucesso!")
    print(f"🖼️ Qualidade de imagem: {IMAGE_SETTINGS['quality']}%")
    print(f"📊 Métodos de extração de tabela disponíveis")
    print(f"📚 Formato de saída: EPUB")
    print(f"🌐 Idioma: {EPUB_SETTINGS['language']}")
