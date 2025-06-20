"""
Módulo especializado para extração e formatação de tabelas de PDFs
"""

import logging
import pandas as pd
from typing import List, Dict, Optional, Tuple
import fitz  # PyMuPDF

# Imports opcionais para bibliotecas avançadas de extração de tabelas
try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False

try:
    import tabula
    TABULA_AVAILABLE = True
except ImportError:
    TABULA_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

logger = logging.getLogger(__name__)


class AdvancedTableExtractor:
    """Extrator avançado de tabelas usando múltiplas bibliotecas"""
    
    def __init__(self):
        self.extraction_methods = []
        
        # Registra métodos disponíveis
        if CAMELOT_AVAILABLE:
            self.extraction_methods.append(("camelot", self._extract_with_camelot))
        if PDFPLUMBER_AVAILABLE:
            self.extraction_methods.append(("pdfplumber", self._extract_with_pdfplumber))
        if TABULA_AVAILABLE:
            self.extraction_methods.append(("tabula", self._extract_with_tabula))
        
        # Método padrão sempre disponível
        self.extraction_methods.append(("pymupdf", self._extract_with_pymupdf))
        
        logger.info(f"Métodos de extração disponíveis: {[m[0] for m in self.extraction_methods]}")
    
    def extract_tables_from_page(self, pdf_path: str, page_num: int) -> List[str]:
        """
        Extrai tabelas de uma página usando múltiplos métodos
        
        Args:
            pdf_path: Caminho do arquivo PDF
            page_num: Número da página (0-indexed)
            
        Returns:
            Lista de tabelas em formato HTML
        """
        tables_html = []
        
        for method_name, method_func in self.extraction_methods:
            try:
                logger.debug(f"Tentando extrair tabelas com {method_name}")
                method_tables = method_func(pdf_path, page_num)
                
                if method_tables:
                    logger.info(f"Encontradas {len(method_tables)} tabelas com {method_name}")
                    tables_html.extend(method_tables)
                    break  # Usa o primeiro método que encontrar tabelas
                    
            except Exception as e:
                logger.warning(f"Erro ao usar {method_name}: {e}")
                continue
        
        return tables_html
    
    def _extract_with_camelot(self, pdf_path: str, page_num: int) -> List[str]:
        """Extrai tabelas usando Camelot"""
        if not CAMELOT_AVAILABLE:
            return []
        
        try:
            # Camelot usa páginas 1-indexed
            tables = camelot.read_pdf(pdf_path, pages=str(page_num + 1))
            
            html_tables = []
            for i, table in enumerate(tables):
                if table.accuracy > 60:  # Só usa tabelas com boa precisão
                    df = table.df
                    
                    # Remove linhas/colunas vazias
                    df = df.dropna(how='all').dropna(axis=1, how='all')
                    
                    if not df.empty:
                        html_table = self._dataframe_to_html(df, f"camelot_table_{i}")
                        html_tables.append(html_table)
            
            return html_tables
            
        except Exception as e:
            logger.warning(f"Erro no Camelot: {e}")
            return []
    
    def _extract_with_pdfplumber(self, pdf_path: str, page_num: int) -> List[str]:
        """Extrai tabelas usando pdfplumber"""
        if not PDFPLUMBER_AVAILABLE:
            return []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if page_num >= len(pdf.pages):
                    return []
                
                page = pdf.pages[page_num]
                tables = page.extract_tables()
                
                html_tables = []
                for i, table_data in enumerate(tables):
                    if table_data and len(table_data) > 1:
                        # Converte para DataFrame
                        df = pd.DataFrame(table_data[1:], columns=table_data[0])
                        
                        # Remove células vazias
                        df = df.fillna('')
                        df = df.replace('None', '')
                        
                        if not df.empty:
                            html_table = self._dataframe_to_html(df, f"pdfplumber_table_{i}")
                            html_tables.append(html_table)
                
                return html_tables
                
        except Exception as e:
            logger.warning(f"Erro no pdfplumber: {e}")
            return []
    
    def _extract_with_tabula(self, pdf_path: str, page_num: int) -> List[str]:
        """Extrai tabelas usando tabula-py"""
        if not TABULA_AVAILABLE:
            return []
        
        try:
            # tabula usa páginas 1-indexed
            tables = tabula.read_pdf(
                pdf_path, 
                pages=page_num + 1, 
                multiple_tables=True,
                pandas_options={'header': 0}
            )
            
            html_tables = []
            for i, df in enumerate(tables):
                if not df.empty:
                    # Limpa dados
                    df = df.dropna(how='all').dropna(axis=1, how='all')
                    df = df.fillna('')
                    
                    if not df.empty:
                        html_table = self._dataframe_to_html(df, f"tabula_table_{i}")
                        html_tables.append(html_table)
            
            return html_tables
            
        except Exception as e:
            logger.warning(f"Erro no tabula: {e}")
            return []
    
    def _extract_with_pymupdf(self, pdf_path: str, page_num: int) -> List[str]:
        """Extrai tabelas usando PyMuPDF (método padrão)"""
        try:
            pdf_document = fitz.open(pdf_path)
            page = pdf_document[page_num]
            
            tables_html = []
            tables = page.find_tables()
            
            for i, table in enumerate(tables):
                table_data = table.extract()
                
                if table_data and len(table_data) > 1:
                    # Converte para DataFrame
                    headers = table_data[0] if table_data[0] else [f"Col_{j}" for j in range(len(table_data[1]))]
                    df = pd.DataFrame(table_data[1:], columns=headers)
                    
                    # Limpa dados
                    df = df.fillna('')
                    df = df.replace('None', '')
                    
                    if not df.empty:
                        html_table = self._dataframe_to_html(df, f"pymupdf_table_{i}")
                        tables_html.append(html_table)
            
            pdf_document.close()
            return tables_html
            
        except Exception as e:
            logger.warning(f"Erro no PyMuPDF: {e}")
            return []
    
    def _dataframe_to_html(self, df: pd.DataFrame, table_id: str) -> str:
        """
        Converte DataFrame para HTML bem formatado
        
        Args:
            df: DataFrame pandas
            table_id: ID único da tabela
            
        Returns:
            HTML da tabela
        """
        # Estilo CSS inline para compatibilidade com e-readers
        table_style = '''
        border-collapse: collapse; 
        width: 100%; 
        margin: 15px 0; 
        font-size: 12px;
        border: 2px solid #333;
        '''
        
        cell_style = '''
        border: 1px solid #666; 
        padding: 8px; 
        text-align: left;
        vertical-align: top;
        '''
        
        header_style = cell_style + '''
        background-color: #f0f0f0; 
        font-weight: bold;
        '''
        
        # Constrói HTML manualmente para melhor controle
        html = f'<table id="{table_id}" style="{table_style}">\n'
        
        # Cabeçalho
        html += '<thead>\n<tr>\n'
        for col in df.columns:
            html += f'<th style="{header_style}">{str(col).strip()}</th>\n'
        html += '</tr>\n</thead>\n'
        
        # Corpo da tabela
        html += '<tbody>\n'
        for _, row in df.iterrows():
            html += '<tr>\n'
            for cell in row:
                cell_content = str(cell).strip() if pd.notna(cell) else ''
                html += f'<td style="{cell_style}">{cell_content}</td>\n'
            html += '</tr>\n'
        html += '</tbody>\n'
        
        html += '</table>\n'
        
        return html


class ImagePreserver:
    """Classe para preservar e otimizar imagens durante a conversão"""
    
    def __init__(self, max_width: int = 800, max_height: int = 1200, quality: int = 85):
        """
        Inicializa o preservador de imagens
        
        Args:
            max_width: Largura máxima das imagens
            max_height: Altura máxima das imagens
            quality: Qualidade JPEG (0-100)
        """
        self.max_width = max_width
        self.max_height = max_height
        self.quality = quality
    
    def optimize_image(self, image_path: str) -> str:
        """
        Otimiza imagem para e-readers
        
        Args:
            image_path: Caminho da imagem
            
        Returns:
            Caminho da imagem otimizada
        """
        try:
            from PIL import Image
            
            with Image.open(image_path) as img:
                # Converte para RGB se necessário
                if img.mode in ('RGBA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = rgb_img
                
                # Redimensiona se necessário
                if img.width > self.max_width or img.height > self.max_height:
                    img.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS)
                
                # Salva com otimização
                optimized_path = image_path.replace('.png', '_opt.jpg')
                img.save(optimized_path, 'JPEG', quality=self.quality, optimize=True)
                
                return optimized_path
                
        except Exception as e:
            logger.warning(f"Erro ao otimizar imagem {image_path}: {e}")
            return image_path
        
        return image_path
