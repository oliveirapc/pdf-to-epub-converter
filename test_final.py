#!/usr/bin/env python3
"""
Teste simples do conversor PDF para Kindle
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pdf_to_kindle_final import PDFToKindleConverter
except ImportError:
    print("❌ Erro: Não foi possível importar o conversor")
    sys.exit(1)


def create_test_pdf():
    """Cria um PDF de teste simples"""
    try:
        import fitz
        
        # Cria PDF de teste
        doc = fitz.open()
        page = doc.new_page()
        
        # Adiciona texto
        text = """
        Teste de Conversão PDF-Kindle
        
        Este é um documento de teste para verificar se o conversor está funcionando corretamente.
        
        Recursos testados:
        • Extração de texto
        • Formatação preservada
        • Criação de EPUB
        
        O arquivo deve ser convertido para formato Kindle mantendo a formatação.
        """
        
        point = fitz.Point(50, 100)
        page.insert_text(point, text, fontsize=12)
        
        # Salva arquivo temporário
        test_file = "teste_conversor.pdf"
        doc.save(test_file)
        doc.close()
        
        return test_file
    
    except Exception as e:
        print(f"❌ Erro ao criar PDF de teste: {e}")
        return None


def test_converter():
    """Testa o conversor"""
    print("🧪 Teste do Conversor PDF-Kindle")
    print("=" * 35)
    
    # Cria PDF de teste
    test_pdf = create_test_pdf()
    if not test_pdf:
        return False
    
    print(f"📄 PDF de teste criado: {test_pdf}")
    
    try:
        # Testa conversão
        print("\n🔄 Testando conversão...")
        
        with PDFToKindleConverter("epub") as converter:
            output_file = converter.convert_pdf(test_pdf)
            
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"✅ Arquivo criado: {output_file}")
                print(f"📏 Tamanho: {size:,} bytes")
                
                # Verifica conteúdo
                try:
                    import zipfile
                    with zipfile.ZipFile(output_file, 'r') as z:
                        files = z.namelist()
                        html_files = [f for f in files if f.endswith('.xhtml')]
                        print(f"📄 Páginas HTML: {len(html_files)}")
                
                except Exception:
                    pass
                
                return True
            else:
                print("❌ Arquivo não foi criado")
                return False
    
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        return False
    
    finally:
        # Limpa arquivo de teste
        if test_pdf and os.path.exists(test_pdf):
            try:
                os.remove(test_pdf)
                print(f"\n🗑️ Arquivo de teste removido")
            except:
                pass


def main():
    """Função principal"""
    success = test_converter()
    
    if success:
        print("\n✅ Teste concluído com sucesso!")
        print("\n💡 Como usar o conversor:")
        print("  python pdf_to_kindle_final.py \"seu_arquivo.pdf\"")
    else:
        print("\n❌ Teste falhou!")
        sys.exit(1)


if __name__ == "__main__":
    main()
