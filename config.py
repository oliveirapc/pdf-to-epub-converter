# Configurações do Conversor PDF-Kindle

# Configurações de imagem
IMAGE_SETTINGS = {
    'max_width': 800,
    'max_height': 1200,
    'quality': 85,
    'format': 'JPEG'
}

# Configurações de texto
TEXT_SETTINGS = {
    'font_size_threshold': {
        'title': 16,
        'subtitle': 14,
        'body': 12
    }
}

# Configurações do EPUB
EPUB_SETTINGS = {
    'language': 'pt-br',
    'creator': 'PDF-Kindle Converter'
}

# Mensagens
MESSAGES = {
    'start_conversion': "🔄 Iniciando conversão...",
    'processing_page': "📄 Processando página {current}/{total}...",
    'conversion_complete': "✅ Conversão concluída!",
    'error_occurred': "❌ Erro: {error}"
}
