"""
PDF generation from HTML content using WeasyPrint.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional
import base64

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False


class PDFGenerator:
    """Generate PDF from HTML content."""
    
    def __init__(self):
        if not WEASYPRINT_AVAILABLE:
            raise ImportError("WeasyPrint is required for PDF generation. Install with: pip install weasyprint")
    
    def generate_pdf(self, html_content: str, output_path: str, css_content: str = "", 
                    logo_file: Optional[str] = None) -> None:
        """Generate PDF from HTML content."""
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_html = f.name
        
        try:
            # Create temporary CSS file if needed
            temp_css = None
            if css_content:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False, encoding='utf-8') as f:
                    f.write(css_content)
                    temp_css = f.name
            
            # Generate PDF
            self._create_pdf(temp_html, output_path, temp_css, logo_file)
            
        finally:
            # Clean up temporary files
            if os.path.exists(temp_html):
                os.unlink(temp_html)
            if temp_css and os.path.exists(temp_css):
                os.unlink(temp_css)
    
    def _create_pdf(self, html_file: str, output_path: str, css_file: Optional[str] = None, 
                   logo_file: Optional[str] = None) -> None:
        """Create PDF using WeasyPrint."""
        # Prepare CSS
        css_list = []
        
        if css_file:
            css_list.append(CSS(filename=css_file))
        
        # Generate PDF
        HTML(filename=html_file).write_pdf(
            output_path,
            stylesheets=css_list
        )
    
    def _image_to_base64(self, image_path: str) -> str:
        """Convert image file to base64 string."""
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
                base64_data = base64.b64encode(image_data).decode('utf-8')
                
                # Determine MIME type based on file extension
                ext = Path(image_path).suffix.lower()
                if ext == '.svg':
                    mime_type = 'image/svg+xml'
                elif ext in ['.png', '.jpg', '.jpeg', '.gif']:
                    mime_type = f'image/{ext[1:]}'
                else:
                    mime_type = 'image/png'  # default
                
                return f"data:{mime_type};base64,{base64_data}"
        except Exception as e:
            print(f"Warning: Could not convert image to base64: {e}")
            return ""
    
    def generate_pdf_from_html_file(self, html_file: str, output_path: str, 
                                   css_file: Optional[str] = None) -> None:
        """Generate PDF from existing HTML file."""
        if not os.path.exists(html_file):
            raise FileNotFoundError(f"HTML file not found: {html_file}")
        
        css_list = []
        if css_file and os.path.exists(css_file):
            css_list.append(CSS(filename=css_file))
        
        HTML(filename=html_file).write_pdf(
            output_path,
            stylesheets=css_list
        )


def check_weasyprint_available() -> bool:
    """Check if WeasyPrint is available."""
    return WEASYPRINT_AVAILABLE 