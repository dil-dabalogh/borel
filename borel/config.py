"""
Configuration management for Borel application.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class BorelConfig:
    """Configuration for Borel application."""
    
    css_file: Optional[str] = None
    logo_file: Optional[str] = None
    company_name: str = "Company Name"
    default_author: str = "Author"
    output_dir: str = "."
    
    @classmethod
    def from_file(cls, config_path: str) -> "BorelConfig":
        """Load configuration from JSON file."""
        if not os.path.exists(config_path):
            return cls()
        
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            return cls(**data)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Invalid config file {config_path}: {e}")
            return cls()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "css_file": self.css_file,
            "logo_file": self.logo_file,
            "company_name": self.company_name,
            "default_author": self.default_author,
            "output_dir": self.output_dir
        }
    
    def save(self, config_path: str) -> None:
        """Save configuration to JSON file."""
        with open(config_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


def find_config_file(input_file: str) -> Optional[str]:
    """Find configuration file in the same directory as input file."""
    input_path = Path(input_file)
    config_path = input_path.parent / "borel.config.json"
    
    if config_path.exists():
        return str(config_path)
    
    # Check parent directories
    for parent in input_path.parents:
        config_path = parent / "borel.config.json"
        if config_path.exists():
            return str(config_path)
    
    return None


def get_default_css() -> str:
    """Get default CSS styling for documents."""
    return """
    @page {
        size: A4;
        margin: 2cm;
        @top-right {
            content: "";
        }
    }
    
    /* Suppress footer and page number on the title page */
    @page :first {
        @bottom-center { content: none; }
        @bottom-right { content: none; }
    }
    
    body {
        font-family: 'Times New Roman', serif;
        font-size: 12pt;
        line-height: 1.5;
        color: #333;
    }
    
    h1 {
        font-size: 24pt;
        font-weight: bold;
        margin-top: 2em;
        margin-bottom: 1em;
        page-break-after: avoid;
    }
    
    h2 {
        font-size: 18pt;
        font-weight: bold;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        page-break-after: avoid;
    }
    
    h3 {
        font-size: 14pt;
        font-weight: bold;
        margin-top: 1em;
        margin-bottom: 0.5em;
        page-break-after: avoid;
    }
    
    p {
        margin-bottom: 1em;
        text-align: justify;
    }
    
    ul, ol {
        margin-bottom: 1em;
        padding-left: 2em;
    }
    
    li {
        margin-bottom: 0.5em;
    }
    
    .title-page {
        text-align: center;
        page-break-after: always;
        counter-reset: page 0;
    }
    
    .title-page h1 {
        font-size: 32pt;
        margin-top: 4em;
        margin-bottom: 1em;
    }
    
    .title-page .subtitle {
        font-size: 18pt;
        margin-bottom: 2em;
        color: #666;
    }
    
    .title-page .author {
        font-size: 14pt;
        margin-bottom: 1em;
    }
    
    .title-page .date {
        font-size: 12pt;
        color: #666;
    }
    
    .letterhead {
        position: fixed;
        top: 1cm;
        right: 1cm;
        width: 3cm;
        height: auto;
        z-index: 1000;
    }
    
    .page-break {
        page-break-before: always;
    }
    """ 