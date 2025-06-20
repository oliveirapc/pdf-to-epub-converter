#!/usr/bin/env python3
"""
Conversor PDF para Kindle (EPUB) - Versão Final Otimizada
Converte PDFs preservando tabelas, imagens, formatação e posicionamento correto.

Autor: PDF-Kindle Converter
Data: Junho 2025
Versão: 2.0 Final
"""

import os
import sys
import argparse
import logging
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
import zipfile

# Bibliotecas para processamento de PDF
import fitz  # PyMuPDF
from PIL import Image
import pandas as pd

# Bibliotecas para criação de ebooks
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup

# Configurações
IMAGE_SETTINGS = {
    'max_width': 800,
    'max_height': 1200,
    'quality': 85,
    'format': 'JPEG'
}

TEXT_SETTINGS = {
    'font_size_threshold': {
        'title': 16,
        'subtitle': 14,
        'body': 12
    }
}

EPUB_SETTINGS = {
    'language': 'pt-br',
    'creator': 'PDF-Kindle Converter'
}

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PDFToKindleConverter:
    """Conversor principal de PDF para formato Kindle com posicionamento correto de imagens"""
    
    def __init__(self, output_format: str = "epub"):
        """
        Inicializa o conversor
        
        Args:
            output_format: Formato de saída (epub)
        """
        self.output_format = output_format.lower()
        self.temp_dir = None
        self.images_dir = None
        
        if self.output_format not in ["epub"]:
            raise ValueError("Formato não suportado. Use: epub")
    
    def __enter__(self):
        """Context manager entry"""
        self.temp_dir = tempfile.mkdtemp()
        self.images_dir = os.path.join(self.temp_dir, "images")
        os.makedirs(self.images_dir, exist_ok=True)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                logger.warning(f"Erro ao limpar diretório temporário: {e}")
    
    def optimize_image(self, image_path: str) -> str:
        """Otimiza imagem para Kindle"""
        try:
            with Image.open(image_path) as img:
                # Converte para RGB se necessário
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Redimensiona se necessário
                max_width = IMAGE_SETTINGS['max_width']
                max_height = IMAGE_SETTINGS['max_height']
                
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Salva otimizada
                optimized_path = image_path.replace('.png', '_opt.jpg')
                img.save(optimized_path, 'JPEG', quality=IMAGE_SETTINGS['quality'], optimize=True)
                
                return optimized_path
        except Exception as e:
            logger.warning(f"Erro ao otimizar imagem {image_path}: {e}")
            return image_path
    
    def extract_images_with_position(self, pdf_document, page_num: int) -> List[Dict[str, Any]]:
        """
        Extrai imagens da página com informações de posição
        
        Args:
            pdf_document: Documento PDF
            page_num: Número da página
            
        Returns:
            Lista de dicionários com informações das imagens e posições
        """
        page = pdf_document[page_num]
        extracted_images = []
        
        # Obter lista de imagens da página
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                
                # Obter dados da imagem
                pix = fitz.Pixmap(pdf_document, xref)
                
                # Obter posição da imagem
                img_rects = page.get_image_rects(xref)
                if not img_rects:
                    # Fallback: usar bbox padrão
                    img_bbox = fitz.Rect(0, 0, 100, 100)
                else:
                    img_bbox = img_rects[0]
                
                # Pular imagens muito pequenas (provavelmente artefatos)
                if pix.width < 10 or pix.height < 10:
                    pix = None
                    continue
                
                # Salvar imagem
                img_name = f"page_{page_num}_img_{img_index}.png"
                img_path = os.path.join(self.images_dir, img_name)
                
                if pix.n - pix.alpha < 4:  # GRAY ou RGB
                    pix.save(img_path)
                    final_path = img_path
                else:  # CMYK: converte para RGB
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.save(img_path)
                    pix1 = None
                    final_path = img_path
                
                # Otimizar imagem
                try:
                    optimized_path = self.optimize_image(img_path)
                    if optimized_path != img_path:
                        os.remove(img_path)
                        final_path = optimized_path
                except Exception as e:
                    logger.warning(f"Erro ao otimizar imagem {img_path}: {e}")
                
                # Armazenar informações da imagem com posição
                image_info = {
                    'path': final_path,
                    'name': os.path.basename(final_path),
                    'bbox': img_bbox,
                    'y_position': img_bbox.y0,
                    'x_position': img_bbox.x0,
                    'width': img_bbox.width,
                    'height': img_bbox.height
                }
                extracted_images.append(image_info)
                logger.debug(f"Imagem extraída: {image_info['name']} em Y={img_bbox.y0:.1f}")
                
                pix = None
                
            except Exception as e:
                logger.warning(f"Erro ao extrair imagem {img_index} da página {page_num}: {e}")
                continue
        
        # Ordenar imagens por posição Y (de cima para baixo)
        extracted_images.sort(key=lambda x: x['y_position'])
        
        logger.info(f"Extraídas {len(extracted_images)} imagens da página {page_num}")
        return extracted_images
    
    def extract_tables(self, page, pdf_path: str, page_num: int) -> List[str]:
        """Extrai tabelas da página e converte para HTML"""
        tables_html = []
        
        try:
            tables = page.find_tables()
            
            for i, table in enumerate(tables):
                table_data = table.extract()
                
                if table_data and len(table_data) > 1:
                    # Converte para DataFrame pandas
                    headers = table_data[0] if table_data[0] else [f"Col_{j}" for j in range(len(table_data[1]))]
                    df = pd.DataFrame(table_data[1:], columns=headers)
                    
                    # Limpa dados
                    df = df.fillna('')
                    df = df.replace('None', '')
                    
                    if not df.empty:
                        # Converte para HTML
                        html_table = df.to_html(
                            index=False,
                            classes="kindle-table",
                            table_id=f"table_{page_num}_{i}",
                            escape=False,
                            border=1
                        )
                        
                        # Aplica CSS inline
                        html_table = html_table.replace(
                            '<table', 
                            '<table style="border-collapse: collapse; width: 100%; margin: 15px 0; font-size: 12px;"'
                        )
                        html_table = html_table.replace(
                            '<th>', 
                            '<th style="border: 1px solid #333; padding: 8px; background-color: #f0f0f0; font-weight: bold;">'
                        )
                        html_table = html_table.replace(
                            '<td>', 
                            '<td style="border: 1px solid #333; padding: 8px;">'
                        )
                        
                        tables_html.append(html_table)
                        logger.info(f"Tabela {i+1} extraída da página {page_num}")
        
        except Exception as e:
            logger.warning(f"Erro ao extrair tabelas da página {page_num}: {e}")
        
        return tables_html
    
    def create_html_content_with_positioned_images(self, text_blocks: List[dict], 
                                                  images_with_pos: List[dict], 
                                                  tables: List[str], 
                                                  page_num: int) -> str:
        """
        Cria conteúdo HTML com texto e imagens posicionadas corretamente
        
        Args:
            text_blocks: Lista de blocos de texto
            images_with_pos: Lista de imagens com informações de posição
            tables: Lista de tabelas em HTML
            page_num: Número da página
            
        Returns:
            String com conteúdo HTML
        """
        html_content = f'<div class="page" id="page_{page_num}">\n'
        
        # Combina texto e imagens em uma única lista ordenada por posição Y
        all_elements = []
        
        # Adiciona blocos de texto
        for block in text_blocks:
            if block["text"].strip():
                all_elements.append({
                    'type': 'text',
                    'y_position': block["bbox"][1],
                    'data': block
                })
        
        # Adiciona imagens
        for img in images_with_pos:
            all_elements.append({
                'type': 'image',
                'y_position': img['y_position'],
                'data': img
            })
        
        # Ordena todos os elementos por posição Y (de cima para baixo)
        all_elements.sort(key=lambda x: x['y_position'])
        
        # Processa elementos ordenados
        current_paragraph = ""
        last_y = None
        
        for element in all_elements:
            if element['type'] == 'text':
                block = element['data']
                text = block["text"].strip()
                if not text:
                    continue
                
                # Detecta quebras de parágrafo
                current_y = block["bbox"][1]
                
                if last_y is not None and abs(current_y - last_y) > block["size"] * 1.5:
                    if current_paragraph:
                        html_content += f'<p class="text-block">{current_paragraph}</p>\n'
                        current_paragraph = ""
                
                # Aplica formatação
                formatted_text = text
                if block["flags"] & 2**4:  # Bold
                    formatted_text = f"<strong>{formatted_text}</strong>"
                if block["flags"] & 2**1:  # Italic
                    formatted_text = f"<em>{formatted_text}</em>"
                
                # Aplica tamanho da fonte
                font_size = int(block["size"])
                if font_size >= TEXT_SETTINGS['font_size_threshold']['title']:
                    formatted_text = f'<h2 style="font-size: {font_size}px;">{formatted_text}</h2>'
                    if current_paragraph:
                        html_content += f'<p class="text-block">{current_paragraph}</p>\n'
                        current_paragraph = ""
                    html_content += formatted_text + '\n'
                elif font_size >= TEXT_SETTINGS['font_size_threshold']['subtitle']:
                    formatted_text = f'<h3 style="font-size: {font_size}px;">{formatted_text}</h3>'
                    if current_paragraph:
                        html_content += f'<p class="text-block">{current_paragraph}</p>\n'
                        current_paragraph = ""
                    html_content += formatted_text + '\n'
                else:
                    current_paragraph += formatted_text + " "
                
                last_y = current_y
                
            elif element['type'] == 'image':
                # Finaliza parágrafo atual antes da imagem
                if current_paragraph:
                    html_content += f'<p class="text-block">{current_paragraph}</p>\n'
                    current_paragraph = ""
                
                img = element['data']
                
                # Determina classe da imagem baseada no tamanho e posição
                img_class = "image-container"
                float_class = ""
                
                # Lógica de posicionamento inteligente
                if img['width'] < 200 and img['height'] < 200:  # Imagem pequena
                    img_class = "image-small"
                    if img['x_position'] < 300:  # Lado esquerdo
                        float_class = " float-left"
                    else:  # Lado direito
                        float_class = " float-right"
                
                html_content += f'''
                <div class="{img_class}{float_class}">
                    <img src="images/{img['name']}" alt="Imagem da página {page_num}" style="max-width: 100%; height: auto;" />
                </div>
                '''
        
        # Adiciona último parágrafo
        if current_paragraph:
            html_content += f'<p class="text-block">{current_paragraph}</p>\n'
        
        # Adiciona tabelas
        for table_html in tables:
            html_content += f'\n{table_html}\n'
        
        # Clear fix para elementos flutuantes
        html_content += '<div class="clearfix"></div>\n'
        html_content += '</div>\n'
        
        return html_content
    
    def get_epub_styles(self) -> str:
        """Retorna CSS otimizado para Kindle"""
        return '''
        body { 
            font-family: serif; 
            margin: 20px; 
            line-height: 1.4;
            color: #000;
        }
        
        .page { 
            page-break-after: always; 
            margin-bottom: 20px;
        }
        
        /* Tabelas */
        .kindle-table { 
            border-collapse: collapse; 
            width: 100%; 
            margin: 15px 0; 
            font-size: 12px;
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
        
        /* Imagens */
        .image-container { 
            text-align: center; 
            margin: 20px 0; 
            clear: both;
        }
        .image-container img { 
            max-width: 100%; 
            height: auto; 
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        .image-small {
            display: inline-block;
            margin: 10px;
            max-width: 40%;
        }
        
        .float-left {
            float: left;
            margin: 0 15px 15px 0;
        }
        
        .float-right {
            float: right;
            margin: 0 0 15px 15px;
        }
        
        /* Texto */
        .text-block {
            margin-bottom: 12px;
            text-align: justify;
        }
        
        h1, h2, h3 { 
            page-break-after: avoid; 
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        /* Clear fix */
        .clearfix::after {
            content: "";
            display: table;
            clear: both;
        }
        '''
    
    def create_epub(self, html_pages: List[str], pdf_path: str, output_path: str):
        """Cria arquivo EPUB"""
        book = epub.EpubBook()
        
        # Metadados
        book_title = Path(pdf_path).stem
        book.set_identifier(f'kindle_convert_{book_title}')
        book.set_title(book_title)
        book.set_language(EPUB_SETTINGS['language'])
        book.add_author(EPUB_SETTINGS['creator'])
        
        # CSS
        nav_css = epub.EpubItem(
            uid="nav_css",
            file_name="style/nav.css",
            media_type="text/css",
            content=self.get_epub_styles()
        )
        book.add_item(nav_css)
        
        # Páginas HTML
        chapters = []
        for i, html_content in enumerate(html_pages):
            chapter = epub.EpubHtml(
                title=f'Página {i+1}',
                file_name=f'chapter_{i+1}.xhtml',
                lang='pt-br'
            )
            chapter.content = f'<!DOCTYPE html><html><head><link rel="stylesheet" href="style/nav.css"/></head><body>{html_content}</body></html>'
            book.add_item(chapter)
            chapters.append(chapter)
        
        # Imagens
        images_added = 0
        if os.path.exists(self.images_dir):
            for img_file in os.listdir(self.images_dir):
                img_path = os.path.join(self.images_dir, img_file)
                
                if not os.path.isfile(img_path):
                    continue
                
                ext = img_file.lower().split('.')[-1]
                if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                    continue
                
                try:
                    with open(img_path, 'rb') as f:
                        img_content = f.read()
                    
                    # Tipo MIME
                    media_type = f"image/{ext}" if ext != 'jpg' else "image/jpeg"
                    
                    img_item = epub.EpubItem(
                        uid=f"img_{img_file.replace('.', '_')}",
                        file_name=f"images/{img_file}",
                        media_type=media_type,
                        content=img_content
                    )
                    book.add_item(img_item)
                    images_added += 1
                    
                except Exception as e:
                    logger.warning(f"Erro ao adicionar imagem {img_file}: {e}")
        
        logger.info(f"Imagens incluídas no EPUB: {images_added}")
        
        # Navegação
        book.toc = chapters
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        book.spine = ['nav'] + chapters
        
        # Salva
        epub.write_epub(output_path, book, {})
        logger.info(f"EPUB criado: {output_path}")
    
    def convert_pdf(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """Converte PDF para formato Kindle"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
        
        # Define saída
        if not output_path:
            base_name = Path(pdf_path).stem
            output_path = f"{base_name}.{self.output_format}"
        
        logger.info(f"🔄 Iniciando conversão de {os.path.basename(pdf_path)}...")
        
        # Abre PDF
        pdf_document = fitz.open(pdf_path)
        total_pages = len(pdf_document)
        logger.info(f"Processando {total_pages} páginas...")
        
        html_pages = []
        
        for page_num in range(total_pages):
            logger.info(f"📄 Processando página {page_num + 1}/{total_pages}...")
            page = pdf_document[page_num]
            
            # Extrai texto
            text_blocks = page.get_text("dict")["blocks"]
            text_blocks = [block for block in text_blocks if "lines" in block]
            
            # Processa blocos de texto
            processed_blocks = []
            for block in text_blocks:
                for line in block["lines"]:
                    for span in line["spans"]:
                        processed_blocks.append({
                            "text": span["text"],
                            "bbox": span["bbox"],
                            "size": span["size"],
                            "flags": span["flags"]
                        })
            
            # Extrai imagens com posição
            images_with_pos = self.extract_images_with_position(pdf_document, page_num)
            
            # Extrai tabelas
            tables = self.extract_tables(page, pdf_path, page_num)
            
            # Cria HTML com posicionamento correto
            html_content = self.create_html_content_with_positioned_images(
                processed_blocks, images_with_pos, tables, page_num + 1
            )
            html_pages.append(html_content)
        
        pdf_document.close()
        
        # Cria arquivo final
        if self.output_format == "epub":
            self.create_epub(html_pages, pdf_path, output_path)
        
        logger.info(f"✅ Conversão concluída: {output_path}")
        return output_path


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Conversor PDF para Kindle com posicionamento correto de imagens',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos:
  python pdf_to_kindle_final.py "documento.pdf"
  python pdf_to_kindle_final.py "arquivo.pdf" --output "kindle.epub" --verbose
        '''
    )
    
    parser.add_argument('input_file', help='Arquivo PDF de entrada')
    parser.add_argument('--output', '-o', help='Arquivo de saída (opcional)')
    parser.add_argument('--format', '-f', choices=['epub'], default='epub', help='Formato (padrão: epub)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')
    
    args = parser.parse_args()
    
    # Configura logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Verifica arquivo
    if not os.path.exists(args.input_file):
        print(f"❌ Arquivo não encontrado: {args.input_file}")
        sys.exit(1)
    
    print("🚀 Conversor PDF-Kindle - Versão Final")
    print("=" * 40)
    print(f"📄 Entrada: {args.input_file}")
    
    try:
        with PDFToKindleConverter(args.format) as converter:
            output_file = converter.convert_pdf(args.input_file, args.output)
            
            print(f"\n🎉 Conversão concluída!")
            print(f"📖 Arquivo: {output_file}")
            
            # Estatísticas
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"📏 Tamanho: {size:,} bytes")
                
                # Análise rápida
                try:
                    with zipfile.ZipFile(output_file, 'r') as z:
                        files = z.namelist()
                        images = [f for f in files if f.startswith('images/')]
                        pages = [f for f in files if f.endswith('.xhtml')]
                        
                        print(f"🖼️ Imagens: {len(images)}")
                        print(f"📄 Páginas: {len(pages)}")
                
                except Exception:
                    pass
                
                print(f"\n✅ Arquivo pronto para Kindle!")
    
    except KeyboardInterrupt:
        print("\n⏹️ Cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
