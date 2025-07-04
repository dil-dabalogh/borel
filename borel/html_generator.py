"""
HTML generation from markdown content using pandoc.
"""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional
from jinja2 import Template

try:
    import pypandoc
    PYPANDOC_AVAILABLE = True
except ImportError:
    PYPANDOC_AVAILABLE = False


class HTMLGenerator:
    """Generate HTML from markdown content."""
    
    def __init__(self):
        self.base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        {{ css_content }}
        /* Footer styling for PDF */
        @media print {
            footer.borel-footer {
                position: fixed;
                bottom: 1cm;
                left: 0;
                right: 0;
                width: 100%;
                text-align: center;
                font-size: 10pt;
                color: #666;
                z-index: 1001;
            }
        }
        footer.borel-footer {
            position: fixed;
            bottom: 1cm;
            left: 0;
            right: 0;
            width: 100%;
            text-align: center;
            font-size: 10pt;
            color: #666;
            z-index: 1001;
        }
        .title-page + footer.borel-footer {
            display: none;
        }
    </style>
</head>
<body data-company="{{ company_name }}" data-year="{{ year }}">
    {{ title_page }}
    
    {% if logo_file %}
    <img src="{{ logo_file }}" alt="Company Logo" class="letterhead">
    {% endif %}
    
    {{ content }}
    
    <footer class="borel-footer">{{ company_name }} &copy; {{ year }}</footer>
</body>
</html>
"""
    
    def generate_html(self, markdown_content: str, metadata: dict, css_content: str, 
                     logo_file: Optional[str] = None) -> str:
        """Generate complete HTML document from markdown."""
        # Convert markdown to HTML
        html_content = self._markdown_to_html(markdown_content)
        
        # Create title page
        title_page = self._create_title_page(metadata)
        
        # Render template
        template = Template(self.base_template)
        
        # Handle date extraction for year
        date_value = metadata.get('date', '')
        if isinstance(date_value, str) and date_value:
            year = date_value.split('-')[0] if '-' in date_value else str(date_value)
        else:
            year = str(date_value) if date_value else ''
        
        # Handle logo file path - convert to relative path if it's a file
        logo_path = None
        if logo_file and os.path.exists(logo_file):
            # Use absolute path for the HTML src attribute to work with WeasyPrint
            logo_path = os.path.abspath(logo_file)
        
        return template.render(
            title=metadata.get('title', 'Document'),
            css_content=css_content,
            company_name=metadata.get('company_name', 'Company Name'),
            year=year,
            logo_file=logo_path,
            title_page=title_page,
            content=html_content
        )
    
    def _markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to HTML using pandoc."""
        if PYPANDOC_AVAILABLE:
            try:
                return pypandoc.convert_text(
                    markdown_content,
                    'html',
                    format='markdown',
                    extra_args=[
                        '--standalone',
                        '--from=markdown',
                        '--to=html',
                        '--wrap=none'
                    ]
                )
            except Exception as e:
                print(f"Warning: Pandoc conversion failed: {e}")
                return self._fallback_markdown_to_html(markdown_content)
        else:
            return self._fallback_markdown_to_html(markdown_content)
    
    def _fallback_markdown_to_html(self, markdown_content: str) -> str:
        """Fallback markdown to HTML conversion using subprocess pandoc."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write(markdown_content)
                temp_file = f.name
            
            result = subprocess.run([
                'pandoc',
                '--standalone',
                '--from=markdown',
                '--to=html',
                '--wrap=none',
                temp_file
            ], capture_output=True, text=True, check=True)
            
            os.unlink(temp_file)
            return result.stdout
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Warning: Pandoc not available: {e}")
            return self._simple_markdown_to_html(markdown_content)
    
    def _simple_markdown_to_html(self, markdown_content: str) -> str:
        """Simple markdown to HTML conversion without external dependencies."""
        import re
        
        # Basic markdown to HTML conversion
        html = markdown_content
        
        # Headers
        html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Lists
        html = re.sub(r'^\- (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^(\d+)\. (.*$)', r'<li>\2</li>', html, flags=re.MULTILINE)
        
        # Paragraphs
        html = re.sub(r'^([^<].*)$', r'<p>\1</p>', html, flags=re.MULTILINE)
        
        # Remove empty paragraphs
        html = re.sub(r'<p>\s*</p>', '', html)
        
        # Wrap lists
        html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
        
        return html
    
    def _create_title_page(self, metadata: dict) -> str:
        """Create title page HTML."""
        title = metadata.get('title', 'Document Title')
        subtitle = metadata.get('subtitle', '')
        author = metadata.get('author', 'Author')
        date = metadata.get('date', '')
        
        title_html = f'<div class="title-page"><h1>{title}</h1>'
        
        if subtitle:
            title_html += f'<div class="subtitle">{subtitle}</div>'
        
        title_html += f'<div class="author">{author}</div>'
        title_html += f'<div class="date">{date}</div>'
        title_html += '</div>'
        
        return title_html
    
    def save_html(self, html_content: str, output_path: str) -> None:
        """Save HTML content to file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content) 