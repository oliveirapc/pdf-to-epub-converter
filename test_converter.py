"""
Script de exemplo e teste para o conversor PDF-Kindle
"""

import os
import sys
import tempfile
from pathlib import Path

# Adiciona o diretório atual ao path para importar nossos módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_to_kindle import PDFToKindleConverter
from table_extractor import AdvancedTableExtractor, ImagePreserver


def test_converter():
    """Testa as funcionalidades principais do conversor"""
    print("🧪 Testando Conversor PDF-Kindle")
    print("=" * 50)
    
    # Testa se as bibliotecas estão funcionando
    print("\n📚 Verificando bibliotecas:")
    
    try:
        import fitz
        print("✅ PyMuPDF: OK")
    except ImportError:
        print("❌ PyMuPDF: Não instalado")
        return False
    
    try:
        import ebooklib
        print("✅ EbookLib: OK")
    except ImportError:
        print("❌ EbookLib: Não instalado")
        return False
    
    try:
        import pandas
        print("✅ Pandas: OK")
    except ImportError:
        print("❌ Pandas: Não instalado")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow: OK")
    except ImportError:
        print("❌ Pillow: Não instalado")
        return False
    
    # Testa bibliotecas opcionais
    print("\n📚 Verificando bibliotecas opcionais:")
    
    try:
        import camelot
        print("✅ Camelot: OK")
    except ImportError:
        print("⚠️  Camelot: Não instalado (opcional)")
    
    try:
        import tabula
        print("✅ Tabula: OK")
    except ImportError:
        print("⚠️  Tabula: Não instalado (opcional)")
    
    try:
        import pdfplumber
        print("✅ PDFPlumber: OK")
    except ImportError:
        print("⚠️  PDFPlumber: Não instalado (opcional)")
    
    # Testa instanciação das classes
    print("\n🔧 Testando classes:")
    
    try:
        converter = PDFToKindleConverter()
        print("✅ PDFToKindleConverter: OK")
    except Exception as e:
        print(f"❌ PDFToKindleConverter: Erro - {e}")
        return False
    
    try:
        extractor = AdvancedTableExtractor()
        print("✅ AdvancedTableExtractor: OK")
        print(f"   Métodos disponíveis: {len(extractor.extraction_methods)}")
    except Exception as e:
        print(f"❌ AdvancedTableExtractor: Erro - {e}")
        return False
    
    try:
        preserver = ImagePreserver()
        print("✅ ImagePreserver: OK")
    except Exception as e:
        print(f"❌ ImagePreserver: Erro - {e}")
        return False
    
    print("\n✅ Todos os testes básicos passaram!")
    return True


def create_sample_pdf():
    """Cria um PDF de exemplo para testar o conversor"""
    print("\n📄 Criando PDF de exemplo...")
    
    try:
        import fitz
        
        # Cria um documento PDF simples
        doc = fitz.open()
        
        # Página 1: Texto formatado
        page1 = doc.new_page()
        
        # Título
        page1.insert_text(
            (50, 100), 
            "Documento de Teste para Conversão Kindle",
            fontsize=18,
            fontname="helv",
            color=(0, 0, 0)
        )
        
        # Subtítulo
        page1.insert_text(
            (50, 150),
            "Capítulo 1: Funcionalidades do Conversor",
            fontsize=14,
            fontname="helv",
            color=(0.2, 0.2, 0.2)
        )
        
        # Parágrafo normal
        texto = """Este é um documento de teste criado para demonstrar as capacidades do conversor PDF-Kindle. 
        
O conversor deve preservar:
• Formatação de texto (negrito, itálico)
• Tamanhos de fonte diferentes
• Espaçamento entre parágrafos
• Estrutura hierárquica do documento

Este parágrafo contém texto normal que deve ser convertido mantendo a formatação original."""
        
        page1.insert_text(
            (50, 200),
            texto,
            fontsize=12,
            fontname="helv"
        )
        
        # Página 2: Tabela simulada
        page2 = doc.new_page()
        
        page2.insert_text(
            (50, 100),
            "Capítulo 2: Teste de Tabelas",
            fontsize=16,
            fontname="helv"
        )
        
        # Simula uma tabela com texto
        table_text = """Produto          Preço    Quantidade
Notebook         R$ 2.500    5
Mouse            R$ 50       20
Teclado          R$ 150      15
Monitor          R$ 800      8"""
        
        page2.insert_text(
            (50, 150),
            table_text,
            fontsize=10,
            fontname="cour"  # Fonte monoespaçada para simular tabela
        )
        
        # Salva o PDF
        sample_path = "documento_teste.pdf"
        doc.save(sample_path)
        doc.close()
        
        print(f"✅ PDF de exemplo criado: {sample_path}")
        return sample_path
        
    except Exception as e:
        print(f"❌ Erro ao criar PDF de exemplo: {e}")
        return None


def demo_conversion():
    """Demonstra a conversão de um PDF"""
    print("\n🔄 Demonstração de Conversão")
    print("=" * 30)
    
    # Cria PDF de exemplo
    sample_pdf = create_sample_pdf()
    if not sample_pdf:
        print("❌ Não foi possível criar PDF de exemplo")
        return
    
    try:
        # Converte o PDF
        with PDFToKindleConverter("epub") as converter:
            output_file = converter.convert_pdf(sample_pdf)
            
            print(f"✅ Conversão concluída!")
            print(f"📖 Arquivo gerado: {output_file}")
            
            # Verifica se o arquivo foi criado
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"📏 Tamanho do arquivo: {file_size:,} bytes")
            
            return output_file
            
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        return None
    
    finally:
        # Limpa arquivo temporário
        if os.path.exists(sample_pdf):
            try:
                os.remove(sample_pdf)
                print(f"🗑️  Arquivo temporário removido: {sample_pdf}")
            except:
                pass


def show_usage_examples():
    """Mostra exemplos de uso"""
    print("\n📖 Exemplos de Uso")
    print("=" * 20)
    
    print("""
💡 Conversão básica:
   python pdf_to_kindle.py "meu_documento.pdf"

💡 Especificar arquivo de saída:
   python pdf_to_kindle.py "documento.pdf" -o "livro.epub"

💡 Modo verboso:
   python pdf_to_kindle.py "documento.pdf" -v

💡 Usar via código Python:
   from pdf_to_kindle import PDFToKindleConverter
   
   with PDFToKindleConverter("epub") as converter:
       output = converter.convert_pdf("documento.pdf")
       print(f"Arquivo gerado: {output}")

📋 Formatos suportados:
   • Entrada: PDF
   • Saída: EPUB (MOBI via Calibre)

🎯 Recursos preservados:
   • Formatação de texto (negrito, itálico, tamanhos)
   • Imagens (otimizadas para e-readers)
   • Tabelas (convertidas para HTML)
   • Estrutura hierárquica (títulos, parágrafos)
   • Espaçamento e layout

⚙️  Para melhor extração de tabelas, instale:
   pip install camelot-py[cv] tabula-py pdfplumber
""")


def main():
    """Função principal do script de teste"""
    print("🚀 Conversor PDF-Kindle - Script de Teste e Exemplo")
    print("=" * 60)
    
    # Executa testes
    if not test_converter():
        print("\n❌ Alguns testes falharam. Verifique a instalação das dependências.")
        print("💡 Execute: pip install -r requirements.txt")
        return
    
    # Demonstra conversão
    demo_conversion()
    
    # Mostra exemplos de uso
    show_usage_examples()
    
    print("\n🎉 Teste concluído com sucesso!")
    print("🔗 Para usar o conversor, execute: python pdf_to_kindle.py \"seu_arquivo.pdf\"")


if __name__ == "__main__":
    main()
