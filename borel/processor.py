"""
Markdown processing and metadata extraction for Borel.
"""

import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, Optional


class MarkdownProcessor:
    """Process markdown files and extract metadata."""
    
    def __init__(self):
        self.metadata_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
        self.page_break_pattern = re.compile(r'\[CRLF\]', re.MULTILINE)
    
    def process_file(self, file_path: str, config=None) -> Tuple[str, Dict[str, Any]]:
        """Process markdown file and return content and metadata. Accepts optional config for fallback."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata from frontmatter
        metadata = self._extract_metadata(content)
        
        # Remove frontmatter from content
        content = self._remove_frontmatter(content)
        
        # Process page breaks
        content = self._process_page_breaks(content)
        
        # Set default metadata if not provided, using config as fallback
        metadata = self._set_default_metadata(metadata, file_path, config)
        
        return content, metadata
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract YAML metadata from frontmatter."""
        match = self.metadata_pattern.match(content)
        if not match:
            return {}
        
        try:
            metadata = yaml.safe_load(match.group(1))
            return metadata or {}
        except yaml.YAMLError as e:
            print(f"Warning: Invalid YAML in frontmatter: {e}")
            return {}
    
    def _remove_frontmatter(self, content: str) -> str:
        """Remove frontmatter from content."""
        return self.metadata_pattern.sub('', content)
    
    def _process_page_breaks(self, content: str) -> str:
        """Replace [CRLF] tokens with HTML page breaks."""
        return self.page_break_pattern.sub('<div class="page-break"></div>', content)
    
    def _set_default_metadata(self, metadata: Dict[str, Any], file_path: str, config=None) -> Dict[str, Any]:
        """Set default metadata values if not provided, using config as fallback."""
        defaults = {
            'title': Path(file_path).stem.replace('_', ' ').title(),
            'subtitle': '',
            'author': 'Author',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'company_name': 'Company Name'
        }
        # If config is provided, use its values as fallback
        if config:
            if hasattr(config, 'company_name') and config.company_name:
                defaults['company_name'] = config.company_name
            if hasattr(config, 'default_author') and config.default_author:
                defaults['author'] = config.default_author
        # Update defaults with provided metadata (from .md, highest priority)
        for key, value in metadata.items():
            if key in defaults:
                defaults[key] = value
        return defaults
    
    def extract_title_page_content(self, content: str) -> Tuple[str, str]:
        """Extract title page content and remaining content."""
        lines = content.split('\n')
        title_lines = []
        content_lines = []
        
        in_title = True
        
        for line in lines:
            if in_title and line.strip() == '':
                # Empty line after title content
                in_title = False
                continue
            
            if in_title and line.strip().startswith('#'):
                # First heading marks end of title page
                in_title = False
                content_lines.append(line)
            elif in_title:
                title_lines.append(line)
            else:
                content_lines.append(line)
        
        title_content = '\n'.join(title_lines).strip()
        main_content = '\n'.join(content_lines).strip()
        
        return title_content, main_content


def create_title_page_html(metadata: Dict[str, Any]) -> str:
    """Create HTML for title page."""
    return f"""
    <div class="title-page">
        <h1>{metadata.get('title', 'Document Title')}</h1>
        {f'<div class="subtitle">{metadata.get("subtitle", "")}</div>' if metadata.get('subtitle') else ''}
        <div class="author">{metadata.get('author', 'Author')}</div>
        <div class="date">{metadata.get('date', '')}</div>
    </div>
    """ 