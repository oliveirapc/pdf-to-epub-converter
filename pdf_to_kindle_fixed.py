"""
Conversor de PDF para formato Kindle (MOBI/EPUB)
Mantém formatação, imagens, tabelas e estrutura do documento original
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Optional, Tuple
import tempfile
import shutil

# Bibliotecas para processamento de PDF
import fitz  # PyMuPDF
from PIL import Image
import pandas as pd

# Bibliotecas para criação de ebooks
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup

# Importa módulos locais
try:
    from config import *
    from table_extractor import AdvancedTableExtractor, ImagePreserver
except ImportError:
    # Fallback para configurações básicas se os módulos não estiverem disponíveis
    IMAGE_SETTINGS = {'max_width': 800, 'max_height': 1200, 'quality': 85}
    TEXT_SETTINGS = {'font_size_threshold': {'title': 16, 'subtitle': 14, 'body': 12}}
    EPUB_SETTINGS = {'language': 'pt-br', 'creator': 'PDF-Kindle Converter'}
    MESSAGES = {
        'start_conversion': "🔄 Iniciando conversão de {input_file}...",
        'processing_page': "📄 Processando página {current}/{total}...",
        'conversion_complete': "✅ Conversão concluída: {output_file}",
        'error_occurred': "❌ Erro durante a conversão: {error}"
    }

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PDFToKindleConverter:
    """Conversor principal de PDF para formato Kindle"""
    
    def __init__(self, output_format: str = "epub"):
        """
        Inicializa o conversor
        
        Args:
            output_format: Formato de saída ('epub' ou 'mobi')
        """
        self.output_format = output_format.lower()
        self.temp_dir = None
        self.images_dir = None
        
        # Inicializa componentes especializados
        try:
            self.table_extractor = AdvancedTableExtractor()
            self.image_preserver = ImagePreserver(**IMAGE_SETTINGS)
        except (NameError, TypeError):
            # Fallback se os módulos especializados não estiverem disponíveis
            self.table_extractor = None
            self.image_preserver = None
            logger.warning("Módulos avançados não disponíveis, usando funcionalidades básicas")
        
    def __enter__(self):
        """Context manager para gerenciar diretórios temporários"""
        self.temp_dir = tempfile.mkdtemp()
        self.images_dir = os.path.join(self.temp_dir, "images")
        os.makedirs(self.images_dir, exist_ok=True)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Limpa diretórios temporários"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def extract_text_and_formatting(self, page) -> List[dict]:
        """
        Extrai texto com informações de formatação da página
        
        Args:
            page: Página do PyMuPDF
            
        Returns:
            Lista de blocos de texto com formatação
        """
        blocks = []
        text_dict = page.get_text("dict")
        
        for block in text_dict["blocks"]:
            if "lines" in block:  # Bloco de texto
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_info = {
                            "text": span["text"],
                            "font": span["font"],
                            "size": span["size"],
                            "flags": span["flags"],  # bold, italic, etc.
                            "color": span["color"],
                            "bbox": span["bbox"]
                        }
                        blocks.append(font_info)
        
        return blocks
    
    def extract_images(self, pdf_document, page_num: int) -> List[str]:
        """
        Extrai imagens da página
        
        Args:
            pdf_document: Documento PDF
            page_num: Número da página
            
        Returns:
            Lista de caminhos para as imagens extraídas
        """
        page = pdf_document[page_num]
        image_list = page.get_images()
        extracted_images = []
        
        logger.debug(f"Encontradas {len(image_list)} imagens na página {page_num}")
        
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                pix = fitz.Pixmap(pdf_document, xref)
                
                if pix.n - pix.alpha < 4:  # GRAY ou RGB
                    img_name = f"page_{page_num}_img_{img_index}.png"
                    img_path = os.path.join(self.images_dir, img_name)
                    
                    # Salva imagem original
                    pix.save(img_path)
                    
                    # Otimiza imagem se o otimizador estiver disponível
                    if self.image_preserver:
                        try:
                            optimized_path = self.image_preserver.optimize_image(img_path)
                            if optimized_path != img_path:
                                # Remove imagem original e usa a otimizada
                                os.remove(img_path)
                                # Renomeia a otimizada para o nome original
                                final_path = img_path.replace('.png', '_opt.jpg')
                                os.rename(optimized_path, final_path)
                                extracted_images.append(final_path)
                                logger.debug(f"Imagem otimizada: {final_path}")
                            else:
                                extracted_images.append(img_path)
                        except Exception as e:
                            logger.warning(f"Erro ao otimizar imagem {img_path}: {e}")
                            extracted_images.append(img_path)
                    else:
                        extracted_images.append(img_path)
                        
                    logger.debug(f"Imagem extraída: {os.path.basename(extracted_images[-1])}")
                
                pix = None
                
            except Exception as e:
                logger.warning(f"Erro ao extrair imagem {img_index} da página {page_num}: {e}")
                continue
        
        logger.info(f"Extraídas {len(extracted_images)} imagens da página {page_num}")
        return extracted_images
    
    def extract_tables(self, page, pdf_path: str, page_num: int) -> List[str]:
        """
        Extrai tabelas da página e as converte para HTML
        
        Args:
            page: Página do PyMuPDF
            pdf_path: Caminho do arquivo PDF
            page_num: Número da página
            
        Returns:
            Lista de tabelas em formato HTML
        """
        tables_html = []
        
        # Usa extrator avançado se disponível
        if self.table_extractor:
            try:
                advanced_tables = self.table_extractor.extract_tables_from_page(pdf_path, page_num)
                if advanced_tables:
                    logger.info(f"Extraídas {len(advanced_tables)} tabelas avançadas da página {page_num}")
                    return advanced_tables
            except Exception as e:
                logger.warning(f"Erro no extrator avançado: {e}")
        
        # Fallback para método básico
        try:
            tables = page.find_tables()
            
            for i, table in enumerate(tables):
                table_data = table.extract()
                
                if table_data and len(table_data) > 1:
                    # Converte para DataFrame pandas para melhor formatação
                    headers = table_data[0] if table_data[0] else [f"Col_{j}" for j in range(len(table_data[1]))]
                    df = pd.DataFrame(table_data[1:], columns=headers)
                    
                    # Limpa dados
                    df = df.fillna('')
                    df = df.replace('None', '')
                    
                    if not df.empty:
                        # Converte para HTML mantendo estilos
                        html_table = df.to_html(
                            index=False,
                            classes="kindle-table",
                            table_id=f"table_{page_num}_{i}",
                            escape=False,
                            border=1
                        )
                        
                        # Aplica CSS inline para compatibilidade
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
                        logger.info(f"Extraída tabela básica {i} da página {page_num}")
                    
        except Exception as e:
            logger.warning(f"Erro ao extrair tabelas da página {page_num}: {e}")
        
        return tables_html
    
    def create_html_content(self, text_blocks: List[dict], images: List[str], 
                          tables: List[str], page_num: int) -> str:
        """
        Cria conteúdo HTML da página mantendo formatação
        
        Args:
            text_blocks: Blocos de texto com formatação
            images: Lista de imagens
            tables: Lista de tabelas HTML
            page_num: Número da página
            
        Returns:
            Conteúdo HTML da página
        """
        html_content = f'<div class="page" id="page_{page_num}">\n'
        
        # Adiciona estilo CSS para manter formatação (apenas na primeira página)
        if page_num == 0:
            try:
                css_style = EPUB_SETTINGS.get('css_style', '''
                <style>
                .page { margin: 20px; font-family: serif; }
                .text-block { margin: 5px 0; }
                .kindle-table { border-collapse: collapse; width: 100%; margin: 10px 0; }
                .kindle-table th, .kindle-table td { border: 1px solid #000; padding: 8px; text-align: left; }
                .kindle-table th { background-color: #f2f2f2; }
                .image-container { text-align: center; margin: 15px 0; }
                .image-container img { max-width: 100%; height: auto; }
                </style>
                ''')
                html_content += f'<style>{css_style}</style>\n'
            except NameError:
                # CSS básico se as configurações não estiverem disponíveis
                html_content += '''
                <style>
                .page { margin: 20px; font-family: serif; }
                .text-block { margin: 5px 0; }
                .kindle-table { border-collapse: collapse; width: 100%; margin: 10px 0; }
                .kindle-table th, .kindle-table td { border: 1px solid #000; padding: 8px; }
                .image-container { text-align: center; margin: 15px 0; }
                .image-container img { max-width: 100%; height: auto; }
                </style>
                '''
        
        # Processa blocos de texto
        current_paragraph = ""
        last_y = None
        
        # Configurações de tamanho de fonte
        try:
            font_thresholds = TEXT_SETTINGS['font_size_threshold']
        except NameError:
            font_thresholds = {'title': 16, 'subtitle': 14, 'body': 12}
        
        for block in text_blocks:
            text = block["text"].strip()
            if not text:
                continue
                
            # Detecta quebras de parágrafo baseado na posição Y
            current_y = block["bbox"][1]
            
            if last_y is not None and abs(current_y - last_y) > block["size"] * 1.5:
                if current_paragraph:
                    html_content += f'<p class="text-block">{current_paragraph}</p>\n'
                    current_paragraph = ""
            
            # Aplica formatação baseada nas flags
            formatted_text = text
            if block["flags"] & 2**4:  # Bold
                formatted_text = f"<strong>{formatted_text}</strong>"
            if block["flags"] & 2**1:  # Italic
                formatted_text = f"<em>{formatted_text}</em>"
            
            # Aplica tamanho da fonte
            font_size = int(block["size"])
            if font_size >= font_thresholds['title']:  # Título
                formatted_text = f'<h2 style="font-size: {font_size}px;">{formatted_text}</h2>'
                if current_paragraph:
                    html_content += f'<p class="text-block">{current_paragraph}</p>\n'
                    current_paragraph = ""
                html_content += formatted_text + '\n'
            elif font_size >= font_thresholds['subtitle']:  # Subtítulo
                formatted_text = f'<h3 style="font-size: {font_size}px;">{formatted_text}</h3>'
                if current_paragraph:
                    html_content += f'<p class="text-block">{current_paragraph}</p>\n'
                    current_paragraph = ""
                html_content += formatted_text + '\n'
            else:
                current_paragraph += formatted_text + " "
            
            last_y = current_y
        
        # Adiciona último parágrafo
        if current_paragraph:
            html_content += f'<p class="text-block">{current_paragraph}</p>\n'
        
        # Adiciona imagens
        for img_path in images:
            img_name = os.path.basename(img_path)
            html_content += f'''
            <div class="image-container">
                <img src="images/{img_name}" alt="Imagem da página {page_num}" />
            </div>
            '''
        
        # Adiciona tabelas
        for table_html in tables:
            html_content += f'\n{table_html}\n'
        
        html_content += '</div>\n'
        return html_content
    
    def create_epub(self, html_pages: List[str], pdf_path: str, output_path: str):
        """
        Cria arquivo EPUB
        
        Args:
            html_pages: Lista de páginas HTML
            pdf_path: Caminho do PDF original
            output_path: Caminho de saída do EPUB
        """
        book = epub.EpubBook()
        
        # Metadados
        book_title = Path(pdf_path).stem
        book.set_identifier(f'kindle_convert_{book_title}')
        book.set_title(book_title)
        
        try:
            book.set_language(EPUB_SETTINGS['language'])
            book.add_author(EPUB_SETTINGS['creator'])
        except NameError:
            book.set_language('pt-br')
            book.add_author('Convertido de PDF')
        
        # Adiciona CSS global
        nav_css = epub.EpubItem(
            uid="nav_css",
            file_name="style/nav.css",
            media_type="text/css",
            content="""
            body { font-family: serif; margin: 20px; }
            .page { page-break-after: always; }
            .kindle-table { border-collapse: collapse; width: 100%; margin: 10px 0; }
            .kindle-table th, .kindle-table td { border: 1px solid #000; padding: 8px; }
            .kindle-table th { background-color: #f2f2f2; }
            .image-container { text-align: center; margin: 15px 0; }
            .image-container img { max-width: 100%; height: auto; }
            """
        )
        book.add_item(nav_css)
        
        # Adiciona páginas
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
        
        # Adiciona imagens
        if os.path.exists(self.images_dir):
            for img_file in os.listdir(self.images_dir):
                img_path = os.path.join(self.images_dir, img_file)
                with open(img_path, 'rb') as f:
                    img_content = f.read()
                
                # Determina tipo MIME da imagem
                if img_file.lower().endswith('.jpg') or img_file.lower().endswith('.jpeg'):
                    media_type = "image/jpeg"
                elif img_file.lower().endswith('.png'):
                    media_type = "image/png"
                else:
                    media_type = "image/png"  # Default
                
                img_item = epub.EpubItem(
                    uid=f"img_{img_file}",
                    file_name=f"images/{img_file}",
                    media_type=media_type,
                    content=img_content
                )
                book.add_item(img_item)
        
        # Configurações de navegação
        book.toc = chapters
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # Spine (ordem de leitura)
        book.spine = ['nav'] + chapters
        
        # Salva o arquivo
        epub.write_epub(output_path, book, {})
        logger.info(f"EPUB criado com sucesso: {output_path}")
    
    def convert_pdf(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """
        Converte PDF para formato Kindle
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            output_path: Caminho de saída (opcional)
            
        Returns:
            Caminho do arquivo convertido
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")
        
        # Define caminho de saída se não fornecido
        if output_path is None:
            base_name = Path(pdf_path).stem
            output_path = os.path.join(
                os.path.dirname(pdf_path), 
                f"{base_name}.{self.output_format}"
            )
        
        try:
            message = MESSAGES['start_conversion'].format(input_file=pdf_path)
        except NameError:
            message = f"🔄 Iniciando conversão de {pdf_path}"
        logger.info(message)
        
        try:
            # Abre o PDF
            pdf_document = fitz.open(pdf_path)
            html_pages = []
            
            total_pages = len(pdf_document)
            logger.info(f"Processando {total_pages} páginas...")
            
            for page_num in range(total_pages):
                try:
                    message = MESSAGES['processing_page'].format(current=page_num + 1, total=total_pages)
                except NameError:
                    message = f"📄 Processando página {page_num + 1}/{total_pages}"
                logger.info(message)
                
                page = pdf_document[page_num]
                
                # Extrai texto e formatação
                text_blocks = self.extract_text_and_formatting(page)
                
                # Extrai imagens
                images = self.extract_images(pdf_document, page_num)
                
                # Extrai tabelas
                tables = self.extract_tables(page, pdf_path, page_num)
                
                # Cria conteúdo HTML
                html_content = self.create_html_content(
                    text_blocks, images, tables, page_num
                )
                html_pages.append(html_content)
            
            # Cria o ebook
            if self.output_format == "epub":
                self.create_epub(html_pages, pdf_path, output_path)
            else:
                raise NotImplementedError(f"Formato {self.output_format} não implementado ainda")
            
            pdf_document.close()
            
            try:
                message = MESSAGES['conversion_complete'].format(output_file=output_path)
            except NameError:
                message = f"✅ Conversão concluída: {output_path}"
            logger.info(message)
            return output_path
            
        except Exception as e:
            try:
                message = MESSAGES['error_occurred'].format(error=e)
            except NameError:
                message = f"❌ Erro durante a conversão: {e}"
            logger.error(message)
            raise


def main():
    """Função principal do programa"""
    parser = argparse.ArgumentParser(
        description="Converte PDFs para formato Kindle mantendo formatação, imagens e tabelas"
    )
    parser.add_argument("pdf_path", help="Caminho para o arquivo PDF")
    parser.add_argument("-o", "--output", help="Caminho de saída do arquivo convertido")
    parser.add_argument(
        "-f", "--format", 
        choices=["epub", "mobi"], 
        default="epub",
        help="Formato de saída (padrão: epub)"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Modo verboso"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        with PDFToKindleConverter(args.format) as converter:
            output_file = converter.convert_pdf(args.pdf_path, args.output)
            print(f"✅ Conversão concluída: {output_file}")
            
            # Se for EPUB e o usuário quiser MOBI, sugere conversão adicional
            if args.format == "mobi":
                print("ℹ️  Para gerar arquivo MOBI, use o Calibre para converter o EPUB gerado:")
                print(f"   ebook-convert \"{output_file}\" \"{output_file.replace('.epub', '.mobi')}\"")
                
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
