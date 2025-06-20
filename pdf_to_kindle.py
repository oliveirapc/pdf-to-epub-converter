#!/usr/bin/env python3
"""
ATENÇÃO: Este arquivo foi movido para pdf_to_kindle_final.py

Para usar o conversor, execute:
    python pdf_to_kindle_final.py "seu_arquivo.pdf"

Para testar:
    python test_final.py
"""

import sys
import os

def main():
    print("⚠️  ARQUIVO MOVIDO")
    print("=" * 30)
    print("Este conversor foi otimizado e movido para:")
    print("📄 pdf_to_kindle_final.py")
    print()
    print("💡 Como usar:")
    print("   python pdf_to_kindle_final.py \"seu_arquivo.pdf\"")
    print()
    print("🧪 Para testar:")
    print("   python test_final.py")
    print()
    
    # Se há argumentos, tenta executar a versão final
    if len(sys.argv) > 1:
        print("🔄 Redirecionando para versão final...")
        try:
            import subprocess
            cmd = [sys.executable, "pdf_to_kindle_final.py"] + sys.argv[1:]
            subprocess.run(cmd)
        except Exception as e:
            print(f"❌ Erro ao redirecionar: {e}")
            print("Execute manualmente: python pdf_to_kindle_final.py")

if __name__ == "__main__":
    main()
