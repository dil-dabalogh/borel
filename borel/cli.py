"""
Command-line interface for Borel application.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import click

from .processor import MarkdownProcessor
from .html_generator import HTMLGenerator
from .pdf_generator import PDFGenerator, check_weasyprint_available
from .config import BorelConfig, find_config_file, get_default_css


@click.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--css', '-c', 'css_file', type=click.Path(exists=True), 
              help='Custom CSS file for styling')
@click.option('--logo', '-l', 'logo_file', type=click.Path(exists=True), 
              help='Company logo file')
@click.option('--output', '-o', 'output_file', type=click.Path(), 
              help='Output PDF file path')
@click.option('--company', help='Company name for footer')
@click.option('--author', help='Document author')
@click.option('--keep-html', is_flag=True, help='Keep intermediate HTML file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(input_file: Path, css_file: Optional[str], logo_file: Optional[str], 
         output_file: Optional[str], company: Optional[str], author: Optional[str],
         keep_html: bool, verbose: bool):
    """
    Convert Markdown file to print-ready PDF with company branding.
    
    INPUT_FILE: Path to the markdown file to process
    """
    try:
        # Validate input file
        if not input_file.exists():
            click.echo(f"Error: Input file '{input_file}' does not exist.", err=True)
            sys.exit(1)
        
        if input_file.suffix.lower() != '.md':
            click.echo(f"Warning: Input file '{input_file}' doesn't have .md extension.", err=True)
        
        # Load configuration
        config = _load_config(input_file, css_file, logo_file, company, author)
        
        if verbose:
            click.echo(f"Processing: {input_file}")
            click.echo(f"CSS: {config.css_file or 'default'}")
            click.echo(f"Logo: {config.logo_file or 'none'}")
            click.echo(f"Company: {config.company_name}")
        
        # Check dependencies
        if not check_weasyprint_available():
            click.echo("Error: WeasyPrint is required but not installed.", err=True)
            click.echo("Install with: pip install weasyprint", err=True)
            sys.exit(1)
        
        # Process markdown
        processor = MarkdownProcessor()
        # Pass config to processor for fallback
        content, metadata = processor.process_file(str(input_file), config)
        
        # Update metadata with CLI options (highest priority)
        if company:
            metadata['company_name'] = company
        if author:
            metadata['author'] = author
        
        # Load CSS
        css_content = _load_css(config.css_file)
        
        # Generate HTML
        html_generator = HTMLGenerator()
        html_content = html_generator.generate_html(
            content, metadata, css_content, config.logo_file
        )
        
        # Determine output path
        if output_file:
            output_path = Path(output_file)
        else:
            output_path = input_file.with_suffix('.pdf')
        
        # Save intermediate HTML if requested
        if keep_html:
            html_path = input_file.with_suffix('.html')
            html_generator.save_html(html_content, str(html_path))
            if verbose:
                click.echo(f"Saved HTML: {html_path}")
        
        # Generate PDF
        pdf_generator = PDFGenerator()
        pdf_generator.generate_pdf(html_content, str(output_path), css_content, config.logo_file)
        
        if verbose:
            click.echo(f"Generated PDF: {output_path}")
        else:
            click.echo(f"Generated: {output_path}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _load_config(input_file: Path, css_file: Optional[str], logo_file: Optional[str],
                company: Optional[str], author: Optional[str]) -> BorelConfig:
    """Load configuration from file and CLI options."""
    # Find config file
    config_path = find_config_file(str(input_file))
    config = BorelConfig.from_file(config_path) if config_path else BorelConfig()
    
    # Override with CLI options
    if css_file:
        config.css_file = css_file
    if logo_file:
        config.logo_file = logo_file
    if company:
        config.company_name = company
    if author:
        config.default_author = author
    
    return config


def _load_css(css_file: Optional[str]) -> str:
    """Load CSS content from file or return default."""
    if css_file and os.path.exists(css_file):
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            click.echo(f"Warning: Could not read CSS file '{css_file}': {e}", err=True)
            return get_default_css()
    else:
        return get_default_css()


if __name__ == '__main__':
    main() 